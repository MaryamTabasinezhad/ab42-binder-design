#!/bin/bash
#SBATCH --job-name=abeta_em
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=8G
#SBATCH --output=em_%j.log
#SBATCH --error=em_%j.err

set -eo pipefail

module load gromacs/2024.6

cd /global/project/hpcg6049/protein/alzheimer/nterm_md/prep

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-8}

echo "=== EM step 1: steepest descent ==="
gmx grompp -f em_steep.mdp -c ions.gro -p topol.top -o em_steep.tpr -maxwarn 1
gmx mdrun -v -deffnm em_steep -ntomp ${OMP_NUM_THREADS}

echo
echo "=== EM step 2: conjugate gradient ==="
gmx grompp -f em_cg.mdp -c em_steep.gro -p topol.top -o em_cg.tpr -maxwarn 1
gmx mdrun -v -deffnm em_cg -ntomp ${OMP_NUM_THREADS}

echo
echo "=== final structure ==="
echo "non-Water" | gmx trjconv -s em_cg.tpr -f em_cg.gro -o em_cg_protein.pdb -pbc mol -ur compact <<EOF || true
non-Water
EOF

# Save final outputs to starting_structure/
OUTDIR=/global/project/hpcg6049/protein/alzheimer/nterm_md/starting_structure
cp em_cg.gro "$OUTDIR/chainA_B_C_with_nterm_minimized.gro"

echo "Protein" | gmx trjconv -s em_cg.tpr -f em_cg.gro \
    -o "$OUTDIR/chainA_B_C_with_nterm_minimized.pdb" \
    -pbc mol -ur compact

echo
echo "=== DONE ==="
ls -la "$OUTDIR"
