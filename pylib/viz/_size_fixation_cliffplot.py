import typing

from matplotlib import ticker as mpl_ticker
import pandas as pd
import seaborn as sns

from ._fill_above_linesx import fill_above_linesx
from ._fill_under_linesx import fill_under_linesx


def size_fixation_cliffplot(
    fixprobs_df: pd.DataFrame,
    x: str,
    y: str,
    col: str,
    hue: str,
    hue_order: typing.List[str],
    errorbar: str,
    **kwargs: dict,
) -> sns.FacetGrid:
    g = sns.relplot(
        data=fixprobs_df[fixprobs_df[hue] == hue_order[1]],
        x=x,
        y=y,
        col=col,
        hue=hue,
        hue_order=hue_order,
        aspect=0.2,
        errorbar=errorbar,
        err_kws={"alpha": 0.5},
        height=3,
        kind="line",
        markers=True,
        orient="y",
        **kwargs,
    )

    sns.move_legend(
        g,
        "lower center",
        bbox_to_anchor=(0.4, -0.05),
        frameon=False,
        ncol=2,
        title=None,
    )

    # g.figure.suptitle("n={apn} agents per node", x=0.63, y=1.02)
    g.figure.subplots_adjust(wspace=0.12)

    for i, ax in enumerate(g.axes.flat):
        fill_above_linesx(ax, color=sns.color_palette("tab10")[0])
        fill_under_linesx(ax)
        ax.set_title("")
        if i + 1 != (len(g.axes.flat) + 1) // 2:  # leave one xlabel
            ax.set_xlabel("")
        ax.axvline(0.5, color="white", lw=1, ls="--")
        ax.set_xticks([0, 0.5, 1])
        ax.set_xticklabels(["", "0.5", ""])

    # Create a new dummy axis above the plot
    g.figure.subplots_adjust(top=0.85)
    delta = 0.001  # Small height for the dummy axis
    pos = g.axes.flat[0].get_position()
    dummy_ax = ax.figure.add_axes(
        [
            pos.x0,
            0.88,
            pos.width * fixprobs_df[col].nunique() * 1.1,
            delta,
        ],
    )
    xvals = fixprobs_df[col]
    dummy_ax.set_xlim(xvals.min(), xvals.max())

    dummy_ax.set_xscale("log")
    dummy_ax.xaxis.set_ticks_position("top")
    dummy_ax.xaxis.set_major_locator(mpl_ticker.LogLocator(base=10))
    formatter = mpl_ticker.LogFormatterMathtext(base=10)
    dummy_ax.xaxis.set_major_formatter(formatter)

    # Hide unwanted spines
    dummy_ax.get_yaxis().set_visible(False)
    dummy_ax.spines[["right", "bottom", "left"]].set_visible(False)

    # Add axis label
    g.figure.text(
        0.02,
        0.97,
        col.replace(" ", "\n"),
        ha="left",
        va="top",
    )

    return g