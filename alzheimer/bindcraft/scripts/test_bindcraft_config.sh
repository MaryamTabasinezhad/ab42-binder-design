#!/bin/bash
#SBATCH --job-name=bc_test
#SBATCH --output=/global/project/hpcg6049/protein/alzheimer/bindcraft/logs/bc_test_%j.out
#SBATCH --error=/global/project/hpcg6049/protein/alzheimer/bindcraft/logs/bc_test_%j.err
#SBATCH --account=def-hpcg6049_gpu
#SBATCH --gres=gpu:a100:1
#SBATCH --time=00:20:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=42G

set -eo pipefail

echo "Job $SLURM_JOB_ID on $(hostname), partition=$SLURM_JOB_PARTITION"
echo "GPU: CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
nvidia-smi -L | head -1

eval "$(conda shell.bash hook)"
conda activate BindCraft

REPO=/global/project/hpcg6049/protein/alzheimer/bindcraft/repo
SETTINGS=/global/project/hpcg6049/protein/alzheimer/bindcraft/settings

echo "=== Testing config parse and first trajectory init ==="
python -u -c "
import sys, os, json
sys.path.insert(0, '$REPO')
from functions import *

# Test settings load
settings_path = '$SETTINGS/ab42_CEG.json'
filters_path = '$REPO/settings_filters/default_filters.json'
advanced_path = '$SETTINGS/advanced_ab42.json'

target_settings, advanced_settings, filters = load_json_settings(settings_path, filters_path, advanced_path)
print('Target settings:', json.dumps(target_settings, indent=2))
print()
print('Hotspots:', target_settings['target_hotspot_residues'])
print('Chains:', target_settings['chains'])
print('Lengths:', target_settings['lengths'])
print('Num final designs:', target_settings['number_of_final_designs'])

# Test advanced settings check
bindcraft_folder = '$REPO'
advanced_settings = perform_advanced_settings_check(advanced_settings, bindcraft_folder)
print()
print('AF2 params dir:', advanced_settings['af_params_dir'])
print('DSSP path:', advanced_settings['dssp_path'])
print('DAlphaBall path:', advanced_settings['dalphaball_path'])

# Verify params exist
import glob
params = glob.glob(os.path.join(advanced_settings['af_params_dir'], 'params', 'params_model_*.npz'))
print(f'Found {len(params)} AF2 param files')

# Test AF2 model loading
print()
print('Loading AF2 models...')
design_models, prediction_models, multimer_validation = load_af2_models(advanced_settings['use_multimer_design'])
print('Design models:', design_models)
print('Prediction models:', prediction_models)
print('Multimer validation:', multimer_validation)

# Test model init + prep_inputs with our PDB
print()
print('Initializing AF2 design model...')
from colabdesign.af import mk_afdesign_model
af_model = mk_afdesign_model(protocol='binder', debug=False, data_dir=advanced_settings['af_params_dir'],
                              use_multimer=advanced_settings['use_multimer_design'], num_recycles=1, best_metric='loss')
print('Model created successfully')

print('Prepping inputs with target PDB and hotspots...')
hotspot = target_settings['target_hotspot_residues']
if hotspot == '': hotspot = None
af_model.prep_inputs(pdb_filename=target_settings['starting_pdb'],
                     chain=target_settings['chains'],
                     binder_len=75,
                     hotspot=hotspot,
                     seed=42,
                     rm_aa=advanced_settings['omit_AAs'])
print(f'Target length: {af_model._target_len}')
print(f'Binder length: {af_model._binder_len}')
print(f'Total length: {af_model._target_len + af_model._binder_len}')
print(f'Hotspot positions: {af_model.opt.get(\"hotspot\", \"not set\")}')
print()
print('=== CONFIG TEST PASSED ===')" 2>&1

echo "Test completed at $(date)"
