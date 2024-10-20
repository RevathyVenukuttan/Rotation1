import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
from matplotlib.backends.backend_pdf import PdfPages

def read_df(path):
    # Read the file into a pandas DataFrame
    df = pd.read_csv(path, sep="\t", header=None)
    df.columns = ['location', 'ref_score', 'sequence', 'background_ref_score']
    df['fc'] = df['ref_score'] - df['background_ref_score']
    df['distance'] = np.tile(np.arange(23, 244, 20), len(df) // 12)
    df_fc = df.groupby('distance').agg(
        mean_fc=('fc', 'mean'),
        sd_fc=('fc', 'std')
    ).reset_index()
    
    return df_fc

def main(directory, output_pdf, plots_per_page=16):
    files = [f for f in os.listdir(directory) if f.endswith(".txt")]
    num_files = len(files)
    cols = 4  
    rows = plots_per_page // cols
    with PdfPages(output_pdf) as pdf:
        for page_start in range(0, num_files, plots_per_page):
            fig, axes = plt.subplots(rows, cols, figsize=(16, 16))  # Adjust figsize as needed
            axes = axes.flatten()
            for i in range(plots_per_page):
                file_idx = page_start + i
                if file_idx >= num_files:
                    axes[i].axis('off')
                else:
                    path = os.path.join(directory, files[file_idx])
                    df_fc = read_df(path)
                    x = np.arange(23, 244, 20)
#                     axes[i].plot(x, df_fc['mean_fc'], '-o', lw=1.5)
                    axes[i].errorbar(x, df_fc['mean_fc'], yerr=df_fc['sd_fc'], fmt='-o', capsize=5, lw=1.5)
                    axes[i].set_title(f"{files[file_idx]}", fontsize=8)
                    axes[i].set_ylim(-0.5, 1.5)
                    axes[i].set_xticks(x)
                    axes[i].tick_params(axis='x', rotation=45, labelsize=6)
                    axes[i].tick_params(axis='y', labelsize=6)
                    axes[i].grid(False)
                    
            plt.tight_layout()
            pdf.savefig(fig)
            plt.close(fig) 
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script boxplots of logFCs for each TF with the X-axis as the position of motif2 and Y-axis represents the logFC between motif1 & motif2.")
    parser.add_argument("directory", help='Path to the directory with the logFC files')
    parser.add_argument("output_pdf", help='Path to the output .pdf file')
    parser.add_argument("plots_per_page", help='Number of plots in a single page of the .pdf file', type=int)
    
    args = parser.parse_args()
    main(args.directory, args.output_pdf, args.plots_per_page)
