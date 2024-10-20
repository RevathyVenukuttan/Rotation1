#!/bin/sh
#
#SBATCH --get-user-env
#SBATCH -J logfc
#SBATCH --mail-user=rv103@duke.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --gres=gpu:1
#SBATCH -p majoroslab-gpu,scavenger-gpu
#SBATCH --nice=100
#SBATCH --mem=102400
#SBATCH --cpus-per-task=1
#SBATCH --array=0-7           
#SBATCH -o /hpc/home/rv103/revathy/BlueSTARR/test/logs/K562_all_motifs_logfc_%A_%a.out
#SBATCH -e /hpc/home/rv103/revathy/BlueSTARR/test/logs/K562_all_motifs_logfc_%A_%a.err
#
mkdir -p /hpc/home/rv103/revathy/BlueSTARR/test/data/K562/all_motifs/logfc
cd /hpc/home/rv103/revathy/BlueSTARR/test/data/K562/all_motifs/enhancer_sequenes/
files=($(ls *-f-ap1-f*.txt))
total_files=${#files[@]}
files_per_node=$((total_files / 8))
start_index=$((SLURM_ARRAY_TASK_ID * files_per_node))
end_index=$((start_index + files_per_node - 1))
for ((i=start_index; i<=end_index && i<total_files; i++)); do
    file=${files[i]}
    python /hpc/home/rv103/revathy/BlueSTARR/test/scripts/K562_test-variants-fc.py \
    /datacommons/igvf-pm/K562/full-set/K562 \
    /hpc/home/rv103/revathy/BlueSTARR/test/data/K562/all_motifs/enhancer_sequenes/${file} \
    /hpc/home/rv103/revathy/BlueSTARR/test/data/K562/all_motifs/logfc/${file/.txt/-logfc.txt}
done
