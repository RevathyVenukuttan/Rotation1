#!/bin/sh
#
#SBATCH --get-user-env
#SBATCH -J boxplot
#SBATCH --mail-user=rv103@duke.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --gres=gpu:1
#SBATCH -p majoroslab-gpu,scavenger-gpu
#SBATCH --nice=100
#SBATCH --mem=102400
#SBATCH --cpus-per-task=1
#SBATCH -o /hpc/home/rv103/revathy/BlueSTARR/test/logs/K562_plot_boxplots.out
#SBATCH -e /hpc/home/rv103/revathy/BlueSTARR/test/logs/K562_plot_boxplots.err
#
python /hpc/home/rv103/revathy/BlueSTARR/test/scripts/plot_boxplots.py \
/hpc/home/rv103/revathy/BlueSTARR/test/data/K562/all_motifs/logfc \
/hpc/home/rv103/revathy/BlueSTARR/test/data/K562/all_motifs/K562_AP1_all_motifs_boxplot.pdf 16
