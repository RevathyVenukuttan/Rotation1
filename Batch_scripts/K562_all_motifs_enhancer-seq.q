#!/bin/sh
#
#SBATCH --get-user-env
#SBATCH -J enhancer_seq
#SBATCH --mail-user=rv103@duke.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --gres=gpu:1
#SBATCH -p majoroslab-gpu,scavenger-gpu
#SBATCH --nice=100
#SBATCH --mem=102400
#SBATCH --cpus-per-task=1
#SBATCH -o /hpc/home/rv103/revathy/BlueSTARR/test/logs/K562_all_motifs_enhancer_seq.out
#SBATCH -e /hpc/home/rv103/revathy/BlueSTARR/test/logs/K562_all_motifs_enhancer_seq.err
#
python /hpc/home/rv103/revathy/BlueSTARR/test/scripts/K562_enhancer_seq_all_motifs.py \
/hpc/home/rv103/revathy/BlueSTARR/test/data/K562/ref_score \
/hpc/home/rv103/revathy/BlueSTARR/test/data/K562/all_motifs/human_tf_consensus_seq_modified.txt \
/hpc/home/rv103/revathy/BlueSTARR/test/data/K562/all_motifs/enhancer_sequenes 50 10 
