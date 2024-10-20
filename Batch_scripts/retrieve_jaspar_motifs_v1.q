#!/bin/sh
#
#SBATCH --get-user-env
#SBATCH -J jaspar_motifs
#SBATCH --mail-user=rv103@duke.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --gres=gpu:1
#SBATCH -p majoroslab-gpu,scavenger-gpu
#SBATCH --nice=100
#SBATCH --mem=102400
#SBATCH --cpus-per-task=1
#SBATCH -o /hpc/home/rv103/revathy/BlueSTARR/test/logs/jaspar_motifs_v1.out
#SBATCH -e /hpc/home/rv103/revathy/BlueSTARR/test/logs/jaspar_motifs_v1.err
#
python /hpc/home/rv103/revathy/BlueSTARR/test/scripts/retrieve_jaspar_motifs_v1.py \
/hpc/home/rv103/revathy/BlueSTARR/test/data/K562/all_motifs/human_tf_pwm_consensus_sequences_v1.csv
