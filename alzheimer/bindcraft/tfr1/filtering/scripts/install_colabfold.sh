#!/bin/bash
# Install ColabFold environment on Nibi for TfR1 counter-screen
set -eo pipefail

echo "=== Installing ColabFold on Nibi ==="
echo "Started: $(date)"

module load python/3.11 cuda/12.6

ENVDIR=/home/ghaedi/envs/colabfold

if [ ! -d "$ENVDIR" ]; then
    echo "Creating virtualenv at $ENVDIR ..."
    python3 -m venv "$ENVDIR"
fi

source "$ENVDIR/bin/activate"
pip install --upgrade pip

# Install ColabFold without the [alphafold] extra to avoid tensorflow-cpu conflict
# Then install alphafold-colabfold and JAX separately
echo "Installing ColabFold base ..."
pip install colabfold

echo "Installing JAX with CUDA 12 support ..."
pip install "jax[cuda12]"

echo "Installing alphafold-colabfold (without tensorflow) ..."
pip install alphafold-colabfold --no-deps
pip install dm-haiku==0.0.10 dm-tree ml-collections

echo "Verifying installation ..."
python3 -c "import colabfold; print('ColabFold version:', colabfold.__version__)"
python3 -c "import jax; print('JAX version:', jax.__version__); print('Devices:', jax.devices())"
which colabfold_batch

echo "=== Done: $(date) ==="
