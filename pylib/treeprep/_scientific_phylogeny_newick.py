import random

import dendropy as dp


def scientific_phylogeny_newick(num_taxa: int) -> str:

    ref = "(((Carcharhinus_leucas:462.40000000,((Acanthurus_leucosternon:84.83588000,Takifugu_rubripes:84.83588000):344.16412000,(Agalychnis_lemur:351.68654000,(((Osphranter_antilopinus:52.64000000,Phascolarctos_cinereus:52.64000000):107.36000000,(((Erinaceus_europaeus:86.29608000,(((((Felis_catus:11.91318000,(Panthera_tigris:5.36525000,(Panthera_leo:2.96000000,Panthera_pardus:2.96000000):3.80700000):5.14618000):43.44846000,((Vulpes_vulpes:12.24414000,Canis_lupus:11.52164000):32.85586000,(((((Enhydra_lutris:15.03982000,Meles_meles:15.03982000):13.33683000,Procyon_lotor:28.37665000):3.97745000,Mephitis_mephitis:32.35410000):7.76590000,Phoca_groenlandica:40.12000000):0.00000000,(Ailuropoda_melanoleuca:19.25625000,(Ursus_arctos:0.82000000,Ursus_maritimus:0.82000000):18.43625000):20.86375000):4.98000000):10.26164000):18.88836000,(((Equus_ferus:2.62000000,Equus_asinus:2.62000000):0.16000000,Equus_zebra:2.78000000):52.60000000,Diceros_bicornis:55.38000000):18.87000000):1.75000000,((Lama_glama:20.91703000,(Camelus_dromedarius:4.35170000,Camelus_bactrianus:4.35170000):16.56533000):43.08297000,(((((Physeter_catodon:32.70000000,Tursiops_truncatus:32.70000000):1.69650000,Balaenoptera_musculus:34.39650000):18.60350000,Hippopotamus_amphibius:53.00000000):4.78810000,(((((Bison_bison:4.30010000,Bos_taurus:4.30010000):8.75990000,Bubalus_bubalis:13.06000000):8.56563000,(Capra_hircus:7.65408000,Ovis_aries:7.65408000):13.97155000):2.06947000,(Cervus_elaphus:12.79646000,Alces_alces:12.79646000):10.89864000):3.05625000,Giraffa_reticulata:26.75135000):31.03675000):4.05455000,Sus_scrofa:61.84265000):2.15735000):12.00000000):5.02605000,Pipistrellus_pipistrellus:81.02605000):5.27003000):7.70392000,((Oryctolagus_cuniculus:78.97061000,(Tamias_striatus:70.20250000,((Cricetus_cricetus:26.17238000,(Rattus_rattus_complex_lineage_III:11.64917000,Mus_musculus:10.83617000):14.52321000):42.14518000,Castor_fiber:68.31756000):1.88494000):8.76811000):8.22939000,((Gorilla_gorilla:15.20000000,Pongo_pygmaeus:15.20000000):13.62000000,Cercopithecus_neglectus:28.82000000):58.38000000):6.80000000):5.18870000,(Loxodonta_africana:96.81920000,Bradypus_tridactylus:96.81920000):2.36950000):60.81130000):158.95000000,((Phelsuma_andamanense:189.28994000,Dendroaspis_angusticeps:189.28994000):90.54156000,((Crocodylus_niloticus:244.75907000,(((Pygoscelis_antarcticus:72.56307000,(Columba_livia:72.43484000,Phoenicopterus:72.43484000):0.12823000):2.53742000,((Asio_otus:70.41822000,Haliaeetus_leucocephalus:70.41822000):0.00000000,(Agapornis_roseicollis:66.04663000,Turdus_merula:65.80380000):4.37159000):4.68227000):15.73917000,((Anas_platyrhynchos:34.33834000,(Anser_anser:20.83000000,Cygnus_cygnus:20.83000000):13.50834000):49.03659000,(Meleagris_gallopavo:35.84266000,(Pavo_cristatus:35.49083000,Gallus_gallus:35.49083000):0.35183000):47.53227000):7.46473000):153.91941000):16.61093000,Testudo_hermanni:261.37000000):18.46150000):39.11850000):32.73654000):77.31346000):33.40000000):245.20436000,(((Latrodectus:397.00000000,Hadrurus:397.00000000):166.30898000,(((Periplaneta_americana:299.29480000,Omocestus_viridulus:299.29480000):83.85520000,((Formica_neogagates:165.45410000,Apis_mellifera:161.27810000):178.54590000,((Coccinellini:256.47434000,Cetonia_aurata:256.47434000):76.19323000,((Calliphora_vicina:240.92000000,Culex_pipiens:240.92000000):58.47011000,(Danaus_plexippus:97.33588000,Papilio_polyxenes:96.18579000):202.05423000):33.27746000):11.33243000):39.15000000):132.22000000,(Penaeus_vannamei:364.66874000,(Paralithodes_camtschaticus:329.96739000,Homarus_gammarus:329.96739000):34.70135000):150.70126000):47.93898000):128.21328000,(Lumbricus_castaneus:581.78241000,((Loligo:287.29878000,Enteroctopus_dofleini:287.29878000):256.11647000,(Helix_pomatia:424.79916000,Bellamya_crawshayi:424.79916000):118.61609000):38.36716000):109.73985000):16.08210000):7.87866000,(Aurelia_aurita:565.14101000,Corallium_rubrum:565.14101000):150.34201000);"

    tree = dp.Tree.get_from_string(ref, schema="newick")

    taxa = [leaf.taxon.label for leaf in tree.leaf_node_iter() if leaf.taxon is not None and leaf.taxon.label]
    tree.retain_taxa_with_labels(random.sample(taxa, num_taxa))

    for node in tree.preorder_node_iter():
        node.edge.length = None
        if not node.is_leaf():
            node.taxon = None

    newick_str = (
        tree.as_string(schema="newick").replace("[&]", "").replace(".", "")
    )
    return newick_str
