#!/bin/bash

set -e

cd "$(dirname "$0")"

echo "configuration ==========================================================="
JOBDATE="$(date '+%Y-%m-%d')"
echo "JOBDATE ${JOBDATE}"

JOBNAME="$(basename -s .sh "$0")"
echo "JOBNAME ${JOBNAME}"

JOBPROJECT="$(basename -s .git "$(git remote get-url origin)")"
echo "JOBPROJECT ${JOBPROJECT}"

HSTRAT_REVISION="469fdb71a01923629243d9828bbe69b022aa8ebe"
echo "HSTRAT_REVISION ${HSTRAT_REVISION}"
HSTRAT_REMOTE_URL="https://github.com/mmore500/hstrat.git"
echo "HSTRAT_REMOTE_URL ${HSTRAT_REMOTE_URL}"

SOURCE_REVISION="$(git rev-parse HEAD)"
echo "SOURCE_REVISION ${SOURCE_REVISION}"
SOURCE_REMOTE_URL="$(git config --get remote.origin.url)"
echo "SOURCE_REMOTE_URL ${SOURCE_REMOTE_URL}"

echo "initialization telemetry ==============================================="
echo "date $(date)"
echo "hostname $(hostname)"
echo "PWD ${PWD}"
echo "SLURM_JOB_ID ${SLURM_JOB_ID:-nojid}"
echo "SLURM_ARRAY_TASK_ID ${SLURM_ARRAY_TASK_ID:-notid}"
module purge || :
module load Python/3.10.8 || :
echo "python3.10 $(which python3.10)"
echo "python3.10 --version $(python3.10 --version)"

echo "setup HOME dirs ========================================================"
mkdir -p "${HOME}/joblatest"
mkdir -p "${HOME}/joblog"
mkdir -p "${HOME}/jobscript"
if ! [ -e "${HOME}/scratch" ]; then
    if [ -e "/mnt/scratch/${USER}" ]; then
        ln -s "/mnt/scratch/${USER}" "${HOME}/scratch" || :
    else
        mkdir -p "${HOME}/scratch" || :
    fi
fi

echo "setup BATCHDIR =========================================================="
BATCHDIR="${HOME}/scratch/${JOBPROJECT}/${JOBNAME}/${JOBDATE}"
if [ -e "${BATCHDIR}" ]; then
    echo "BATCHDIR ${BATCHDIR} exists, clearing it"
fi
rm -rf "${BATCHDIR}"
mkdir -p "${BATCHDIR}"
echo "BATCHDIR ${BATCHDIR}"

ln -sfn "${BATCHDIR}" "${HOME}/scratch/${JOBPROJECT}/${JOBNAME}/latest"

BATCHDIR_JOBLOG="${BATCHDIR}/joblog"
echo "BATCHDIR_JOBLOG ${BATCHDIR_JOBLOG}"
mkdir -p "${BATCHDIR_JOBLOG}"

BATCHDIR_JOBRESULT="${BATCHDIR}/jobresult"
echo "BATCHDIR_JOBRESULT ${BATCHDIR_JOBRESULT}"
mkdir -p "${BATCHDIR_JOBRESULT}"

BATCHDIR_JOBSCRIPT="${BATCHDIR}/jobscript"
echo "BATCHDIR_JOBSCRIPT ${BATCHDIR_JOBSCRIPT}"
mkdir -p "${BATCHDIR_JOBSCRIPT}"

BATCHDIR_JOBSOURCE="${BATCHDIR}/_jobsource"
echo "BATCHDIR_JOBSOURCE ${BATCHDIR_JOBSOURCE}"
if [[ $* == *--dirty* ]]; then
    cp -r "$(git rev-parse --show-toplevel)" "${BATCHDIR_JOBSOURCE}"
else
    mkdir -p "${BATCHDIR_JOBSOURCE}"
    for attempt in {1..5}; do
        rm -rf "${BATCHDIR_JOBSOURCE}/.git"
        git -C "${BATCHDIR_JOBSOURCE}" init \
        && git -C "${BATCHDIR_JOBSOURCE}" remote add origin "${SOURCE_REMOTE_URL}" \
        && git -C "${BATCHDIR_JOBSOURCE}" fetch origin "${SOURCE_REVISION}" --depth=1 \
        && git -C "${BATCHDIR_JOBSOURCE}" reset --hard FETCH_HEAD \
        && break || echo "failed to clone, retrying..."
        if [ $attempt -eq 5 ]; then
            echo "failed to clone, failing"
            exit 1
        fi
        sleep 5
    done
fi

BATCHDIR_ENV="${BATCHDIR}/_jobenv"
python3.10 -m venv --system-site-packages "${BATCHDIR_ENV}"
source "${BATCHDIR_ENV}/bin/activate"
echo "python3.10 $(which python3.10)"
echo "python3.10 --version $(python3.10 --version)"
for attempt in {1..5}; do
    python3.10 -m pip install --upgrade pip setuptools wheel || :
    python3.10 -m pip install --upgrade uv \
    && python3.10 -m uv pip install -r "${BATCHDIR_JOBSOURCE}/requirements.txt" \
    && python3.10 -m uv pip install "${BATCHDIR_JOBSOURCE}"\
    && break || echo "pip install attempt ${attempt} failed"
    if [ ${attempt} -eq 3 ]; then
        echo "pip install failed"
        exit 1
    fi
done

echo "setup dependencies ========================================== \${SECONDS}"
source "${BATCHDIR_ENV}/bin/activate"
python3.10 -m uv pip freeze

echo "sbatch preamble ========================================================="
JOB_PREAMBLE=$(cat << EOF
set -e
shopt -s globstar

# adapted from https://unix.stackexchange.com/a/504829
handlefail() {
    echo ">>>error<<<" || :
    awk 'NR>L-4 && NR<L+4 { printf "%-5d%3s%s\n",NR,(NR==L?">>>":""),\$0 }' L=\$1 \$0 || :
    ln -sfn "\${JOBSCRIPT}" "\${HOME}/joblatest/jobscript.failed" || :
    ln -sfn "\${JOBLOG}" "\${HOME}/joblatest/joblog.failed" || :
    $(which scontrol || which echo) requeuehold "${SLURM_JOBID:-nojid}"
}
trap 'handlefail $LINENO' ERR

echo "initialization telemetry ------------------------------------ \${SECONDS}"
echo "HSTRAT_REVISION ${HSTRAT_REVISION}"
echo "SOURCE_REVISION ${SOURCE_REVISION}"
echo "BATCHDIR ${BATCHDIR}"

echo "cc SLURM script --------------------------------------------- \${SECONDS}"
JOBSCRIPT="\${HOME}/jobscript/\${SLURM_JOB_ID:-nojid}"
echo "JOBSCRIPT \${JOBSCRIPT}"
cp "\${0}" "\${JOBSCRIPT}"
chmod +x "\${JOBSCRIPT}"
cp "\${JOBSCRIPT}" "${BATCHDIR_JOBSCRIPT}/\${SLURM_JOB_ID:-nojid}"
ln -sfn "\${JOBSCRIPT}" "${HOME}/joblatest/jobscript.launched"

echo "cc job log -------------------------------------------------- \${SECONDS}"
JOBLOG="\${HOME}/joblog/\${SLURM_JOB_ID:-nojid}"
echo "JOBLOG \${JOBLOG}"
touch "\${JOBLOG}"
ln -sfn "\${JOBLOG}" "${BATCHDIR_JOBLOG}/\${SLURM_JOB_ID:-nojid}"
ln -sfn "\${JOBLOG}" "\${HOME}/joblatest/joblog.launched"

echo "setup JOBDIR ------------------------------------------------ \${SECONDS}"
JOBDIR="${BATCHDIR}/__\${SLURM_ARRAY_TASK_ID:-\${SLURM_JOB_ID:-\${RANDOM}}}"
echo "JOBDIR \${JOBDIR}"
if [ -e "\${JOBDIR}" ]; then
    echo "JOBDIR \${JOBDIR} exists, clearing it"
fi
rm -rf "\${JOBDIR}"
mkdir -p "\${JOBDIR}"
cd "\${JOBDIR}"
echo "PWD \${PWD}"

echo "job telemetry ----------------------------------------------- \${SECONDS}"
echo "source SLURM_JOB_ID ${SLURM_JOB_ID:-nojid}"
echo "current SLURM_JOB_ID \${SLURM_JOB_ID:-nojid}"
echo "SLURM_ARRAY_TASK_ID \${SLURM_ARRAY_TASK_ID:-notid}"
echo "hostname \$(hostname)"
echo "date \$(date)"

echo "module setup ------------------------------------------------ \${SECONDS}"
module purge || :
module load Python/3.10.8 || :
echo "python3.10 \$(which python3.10)"
echo "python3.10 --version \$(python3.10 --version)"

echo "setup dependencies ------------------------------------------ \${SECONDS}"
source "${BATCHDIR_ENV}/bin/activate"
python3.10 -m uv pip freeze

echo "load secrets ------------------------------------------------ \${SECONDS}"
source "${HOME}/.OPENAI_API_KEY" || :

EOF
)

echo "create sbatch file: work ==============================================="

SBATCH_FILE="$(mktemp)"
echo "SBATCH_FILE ${SBATCH_FILE}"

###############################################################################
# WORK ---------------------------------------------------------------------- #
###############################################################################
cat > "${SBATCH_FILE}" << EOF
#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --time=4:00:00
#SBATCH --output="/mnt/home/%u/joblog/%j"
#SBATCH --mail-user=mawni4ah2o@pomail.net
#SBATCH --mail-type=FAIL,TIME_LIMIT
#SBATCH --account=beacon
#SBATCH --requeue
#SBATCH --array=0-3

${JOB_PREAMBLE}

echo "lscpu ------------------------------------------------------- \${SECONDS}"
lscpu || :

echo "lshw -------------------------------------------------------- \${SECONDS}"
lshw || :

echo "cpuinfo ----------------------------------------------------- \${SECONDS}"
cat /proc/cpuinfo || :

echo "do work ----------------------------------------------------- \${SECONDS}"
python3 << EOF_
import itertools as it
import os
import random

import pandas as pd
from tqdm import tqdm

from pylib.prompt._build_prompt import build_prompt
from pylib.prompt._question_equivalence_identical import (
    question_equivalence_identical,
)
from pylib.prompt._question_equivalence_rotate_tree import (
    question_equivalence_rotate_tree,
)
from pylib.prompt._question_equivalence_shufflerotate_tree import (
    question_equivalence_shufflerotate_tree,
)
from pylib.prompt._question_equivalence_swap_taxa import (
    question_equivalence_swap_taxa,
)
from pylib.prompt._question_most_related import question_identify_most_related
from pylib.prompt._question_most_related_to_x import question_most_related_to_x
from pylib.query._query_openai import query_openai
from pylib.treeprep._sample_phylogeny_newick import sample_phylogeny_newick
from pylib.treeprep._scientific_phylogeny_newick import scientific_phylogeny_newick
from pylib.treerepr._make_json_from_newick import make_json_from_newick


job = \${SLURM_ARRAY_TASK_ID:-0}
random.seed(job)
print(f"{job=}")

records = []
for replicate, num_taxa, question_, model, tree_source in tqdm(
    it.product(
        range(9),
        [3, 4, 5, 8, 12, 18, 25],
        (
            question_equivalence_identical,
            question_equivalence_rotate_tree,
            question_equivalence_shufflerotate_tree,
            question_equivalence_swap_taxa,
            question_identify_most_related,
            question_most_related_to_x,
        ),
        ("gpt-4o-mini", "gpt-4o"),
        (sample_phylogeny_newick, scientific_phylogeny_newick),
    ),
):
    newick_tree = tree_source(num_taxa)
    question, choices, true_answer, trees = question_(
        newick_tree,
    )

    prompt = build_prompt(trees, question, choices)
    print("prompt:", prompt)
    result = query_openai(prompt, choices, true_answer, model=model)
    result["job"] = job
    result["replicate"] = replicate
    result["question"] = question_.__name__
    result["num_taxa"] = num_taxa
    result["tree representation"] = "newick"
    result["tree source"] = tree_source.__name__
    result["model"] = model
    records.append(result)

    newick_tree = tree_source(num_taxa)
    question, choices, true_answer, trees = question_(
        newick_tree,
    )

    json_trees = [make_json_from_newick(tree) for tree in trees]
    prompt = build_prompt(json_trees, question, choices)
    print("prompt:", prompt)
    result = query_openai(prompt, choices, true_answer, model=model)
    result["job"] = job
    result["replicate"] = replicate
    result["question"] = question_.__name__
    result["num_taxa"] = num_taxa
    result["tree representation"] = "json"
    result["tree source"] = tree_source.__name__
    result["model"] = model
    records.append(result)

    newick_tree = tree_source(num_taxa)
    question, choices, true_answer, trees = question_(
        newick_tree,
    )

    prompt = build_prompt([], question, choices)
    print("prompt:", prompt)
    result = query_openai(prompt, choices, true_answer, model=model)
    result["job"] = job
    result["replicate"] = replicate
    result["question"] = question_.__name__
    result["num_taxa"] = num_taxa
    result["tree representation"] = "none"
    result["tree source"] = tree_source.__name__
    result["model"] = model
    records.append(result)

    if "CI" in os.environ:
        break

df = pd.DataFrame.from_records(records)
print(df.describe())
print(df.head())
print(df.tail())

outpath = f"\${JOBDIR}/a=result+ext=.csv"
print(f"writing {outpath}")
df.to_csv(outpath, index=False)

print("python heredoc complete")

EOF_

echo "finalization telemetry -------------------------------------- \${SECONDS}"
ls -l \${JOBDIR}
du -h \${JOBDIR}
ln -sfn "\${JOBSCRIPT}" "${HOME}/joblatest/jobscript.finished"
ln -sfn "\${JOBLOG}" "${HOME}/joblatest/joblog.finished"
echo "SECONDS \${SECONDS}"
echo '>>>complete<<<'

EOF
###############################################################################
# --------------------------------------------------------------------------- #
###############################################################################


echo "submit sbatch file ====================================================="
# $(which sbatch && echo --job-name="${JOBNAME}" || which bash) "${SBATCH_FILE}"
for replicate in {0..9}; do
    export SLURM_ARRAY_TASK_ID=${replicate}
    bash "${SBATCH_FILE}" &
done

echo "waiting"
wait
echo "done waiting"

echo "create sbatch file: collate ============================================"

SBATCH_FILE="$(mktemp)"
echo "SBATCH_FILE ${SBATCH_FILE}"

###############################################################################
# COLLATE ------------------------------------------------------------------- #
###############################################################################
cat > "${SBATCH_FILE}" << EOF
#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --time=4:00:00
#SBATCH --output="/mnt/home/%u/joblog/%j"
#SBATCH --mail-user=mawni4ah2o@pomail.net
#SBATCH --mail-type=ALL
#SBATCH --account=beacon
#SBATCH --requeue

${JOB_PREAMBLE}

echo "BATCHDIR ${BATCHDIR}"
ls -l "${BATCHDIR}"

echo "finalize ---------------------------------------------------- \${SECONDS}"
echo "   - archive job dir"
pushd "${BATCHDIR}/.."
    tar czvf \
    "${BATCHDIR_JOBRESULT}/a=jobarchive+date=${JOBDATE}+job=${JOBNAME}+ext=.tar.gz" \
    "$(basename "${BATCHDIR}")"/__*
popd

echo "   - join result"
ls -1 "${BATCHDIR}"/__*/**/a=result+* \
    | tee /dev/stderr \
    | python3.10 -m joinem --progress \
        "${BATCHDIR_JOBRESULT}/a=result+date=${JOBDATE}+job=${JOBNAME}+ext=.csv"
ls -l "${BATCHDIR_JOBRESULT}"
du -h "${BATCHDIR_JOBRESULT}"

echo "   - archive joblog"
pushd "${BATCHDIR}"
    tar czf \
    "${BATCHDIR_JOBRESULT}/a=joblog+date=${JOBDATE}+job=${JOBNAME}+ext=.tar.gz" \
    -h "$(basename "${BATCHDIR_JOBLOG}")"
popd

echo "   - archive jobscript"
pushd "${BATCHDIR}"
    tar czfv \
    "$(basename "${BATCHDIR_JOBRESULT}")/a=jobscript+date=${JOBDATE}+job=${JOBNAME}+ext=.tar.gz" \
    -h "$(basename ${BATCHDIR_JOBSCRIPT})"
popd

ls -l "${BATCHDIR}"

echo "cleanup ----------------------------------------------------- \${SECONDS}"
cd "${BATCHDIR}"
for f in _*; do
    echo "tar and rm \$f"
    tar cf "\${f}.tar" -h "\${f}"
    rm -rf "\${f}"
done
cd
ls -l "${BATCHDIR}"

echo "finalization telemetry -------------------------------------- \${SECONDS}"
ln -sfn "\${JOBSCRIPT}" "\${HOME}/joblatest/jobscript.completed"
ln -sfn "\${JOBLOG}" "\${HOME}/joblatest/joblog.completed"
ln -sfn "${BATCHDIR_JOBRESULT}" "\${HOME}/joblatest/jobresult.completed"
echo "SECONDS \${SECONDS}"
echo '>>>complete<<<'

EOF
###############################################################################
# --------------------------------------------------------------------------- #
###############################################################################

echo "submit sbatch file ====================================================="
$(which sbatch && echo --job-name="${JOBNAME}" --dependency=singleton || which bash) "${SBATCH_FILE}"

echo "finalization telemetry ================================================="
echo "BATCHDIR ${BATCHDIR}"
echo "SECONDS ${SECONDS}"
echo '>>>complete<<<'
