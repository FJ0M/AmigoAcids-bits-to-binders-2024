import os
import numpy as np
import re
# ## Set paths to bins and folders
cluster = False
# #### For cluster
if cluster==True:
    path_mpnn = '/projects/cpr_sbmm/people/phr361/ProteinMPNN-1.0.1/'
    main_folder='/projects/cpr_sbmm/people/phr361/MotABC/'
    phr361 ='/projects/cpr_sbmm/people/phr361/'
    
    out_folder=main_folder+'outputs/'
    scwrl_bin = phr361+"Scwrl4/Scwrl4"
    scwrl_config = phr361+"Scwrl4/Scwrl4.ini"
    parent_span_file = main_folder+'Input_Structure/6ykm_OPM.span'
    pdb_path = main_folder+'Input_Structure/6ykm_OPM.pdb'
    rosetta = '/projects/cpr_sbmm/apps/rosetta/'
    relax_bin = rosetta+"main/source/bin/relax.static.linuxgccrelease"
    my_rosetta = '/projects/cpr_sbmm/people/phr361/rosetta/'
    plain_relax_flags   = my_rosetta+"relax.flags"
    membrane_relax_flags= my_rosetta+"membrane_relax.flags"
    mp_relax_xml = my_rosetta+'membrane_relax_FM.xml'
    rosetta_scripts_bin = rosetta+"main/source/bin/rosetta_scripts.static.linuxgccrelease"
#### For local
else:
    path_mpnn = '/Users/phr361/Documents/Coding/ProteinDesign/ProteinMPNN-1.0.1/'
    main_folder='/Users/phr361/Documents/Coding/ProteinDesign/AsymMotors/MotABC/'
    out_folder= main_folder+'outputs/'

    scwrl_bin = "/Users/phr361/Scwrl4/Scwrl4"
    scwrl_config = "/Users/phr361/Scwrl4/Scwrl4.ini"
    parent_span_file = main_folder+'Input_Structure/6ykm_OPM.span'
    pdb_path = main_folder+'Input_Structure/6ykm_OPM.pdb'

    rosetta = '/Users/phr361/rosetta_bin_mac_2021.16.61629_bundle/'
    relax_bin = rosetta+"main/source/bin/relax.static.macosclangrelease"
    plain_relax_flags   = "/Users/phr361/Documents/Coding/RosettaFiles/rosetta_relax/02_scripts/relax.flags"
    membrane_relax_flags= "/Users/phr361/Documents/Coding/RosettaFiles/Membrane/membrane_relax_100.flags"
    rosetta_scripts_bin = rosetta+"main/source/bin/rosetta_scripts.static.macosclangrelease"
    mp_relax_xml = '/Users/phr361/rosetta_bin_mac_2021.16.61629_bundle/main/demos/protocol_capture/mp_relax/membrane_relax_FM.xml'

def TM_score(pdb, parent_pdb, outfile='out.txt',TM_bin='/Users/phr361/Documents/Coding/TM/TMscore'):
    os.system(f'{TM_bin} {pdb} {parent_pdb} > {outfile}')
    tm_score = None
    with open(outfile, 'r') as file:
        for line in file:

            match = re.search(r' = (0.\d+)', line)

            if match:
                tm_score = float(match.group(1))
                return tm_score
    if tm_score==None:
        print(f'No TM found, please check the output: {outfile}') 
        return tm_score

def run_relax(pdb, outfile,flags=plain_relax_flags):
    print("Processing file:", pdb)
    rosetta_str = f"{relax_bin} -s {pdb} -out:path:all {outfile} @{flags}"
    print(rosetta_str)
    os.system(rosetta_str) # run the string command on the system
