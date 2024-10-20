import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse

def read_df(path):
    df = pd.read_csv(path, sep="\t", header=None)
    df.columns = ['location', 'ref_score', 'sequence', 'background_ref_score']
    df['fc'] = df['ref_score'] - df['background_ref_score']
    df['distance'] = np.tile(np.arange(23, 244, 20), len(df) // 12)
    df_fc = df.groupby('distance').agg(mean_fc=('fc', 'mean'), sd_fc=('fc', 'std')).reset_index()
    return df_fc

def main(directory, output_png):
    files = [f for f in os.listdir(directory) if f.endswith(".txt")]
    x = np.arange(23, 244, 20)
    
    plt.figure(figsize=(10, 8))
    for i, filename in enumerate(files):
        path = os.path.join(directory, filename)
        df_fc = read_df(path)
        plt.plot(x, df_fc['mean_fc'], label=f"File {i+1}: {filename}", lw=1.5)
        plt.text(x[-1] + 2, df_fc['mean_fc'].values[-1], f"{filename}", 
                 fontsize=8, va='center')
    
    plt.title("Mean log2FC for AP1 v/s all TF motifs in K562")
    plt.xlabel("Base Pairs between AP1 and Motif")
    plt.ylabel("Mean log2FC (Ap1_Motif/Background)")
    plt.xticks(x, rotation=45)
    plt.ylim(-0.5, 2)
    sns.despine()
    plt.tight_layout()
    plt.savefig(output_png)
    plt.close()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script generates a single line plot with logFCs of all TFs.Here X-axis is position of motif2 and Y-axis is the logFC between motif1 & motif2.")
    parser.add_argument("directory", help='Path to the directory with the logFC files')
    parser.add_argument("output_png", help='Path to the output .PNG file')
    
    args = parser.parse_args()
    main(args.directory, args.output_png)
