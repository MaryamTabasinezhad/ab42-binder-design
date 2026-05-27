#!/bin/bash
set -eo pipefail

module load python/3.11 cuda/12.6

source /home/ghaedi/envs/colabfold/bin/activate

echo "Installing JAX..."
pip install "jax[cuda12]>=0.4.30"

echo "Installing alphafold-colabfold..."
pip install alphafold-colabfold --no-deps

echo "Installing alphafold extra deps..."
pip install dm-haiku dm-tree ml-collections

echo "Verifying..."
python3 -c "import jax; print('JAX:', jax.__version__); print('Devices:', jax.devices())"
python3 -c "import alphafold; print('AlphaFold imported OK')"
colabfold_batch --help 2>&1 | head -3

echo "Done: $(date)"
