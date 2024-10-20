import requests
import csv
import time
import argparse

def get_motifs(base_url,params,page): 
    all_motifs = []
    while True:
        params['page'] = page
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            motif_info = response.json()
            motifs_data = motif_info.get('results')
            if not motifs_data:
                break
            print(f"Page {page} completed")
            all_motifs.extend(motifs_data)
            page += 1  # Move to the next page
        else:
            print(f"Error fetching motifs: {response.status_code}")
            break
    return all_motifs

def pwm_to_consensus(pwm):
    consensus = ""
    positions = range(len(pwm['A']))
    for i in positions:  
        max_val = -1
        max_base = ""
        for base in "ACGT":
            if pwm[base][i] > max_val:
                max_val = pwm[base][i]
                max_base = base
        consensus += max_base
    return consensus

def rev_comp(seq):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    return "".join(complement[n] for n in reversed(seq))

def main(output_file):
    base_url = "https://jaspar.genereg.net/api/v1/matrix/"
    params = {'tax_id': 9606, 'page_size': 1000}
    page = 1
    processed_data = []

    all_motifs = get_motifs(base_url, params, page)

    for motif in all_motifs:
        motif_id = motif.get('matrix_id')
        motif_name = motif.get('name')
        
        pwm_url = f"https://jaspar.genereg.net/api/v1/matrix/{motif_id}/"
        pwm_response = requests.get(pwm_url)
        if pwm_response.status_code == 200:
            motif_details = pwm_response.json()
            print(f"Got motif details for {motif_id}")
            pwm = motif_details.get('pfm')  
            if pwm:
                consensus_sequence = pwm_to_consensus(pwm)
                processed_data.append([motif_id, motif_name, consensus_sequence])
            else:
                print(f"PWM missing for motif {motif_id}")
                processed_data.append([motif_id, motif_name, "N/A"])
        else:
            print(f"Error fetching PWM for motif {motif_id}: {pwm_response.status_code}")
            processed_data.append([motif_id, motif_name, "N/A"])


    df = pd.DataFrame(processed_data, columns=["MotifID", "TF", "motif_sequence"])

    # Step 2: Add suffixes to duplicate TF names and compute reverse complement
    df['TF_suffix'] = df.groupby('TF').cumcount() + 1
    df['TF'] = df.apply(lambda x: f"{x['TF']}_{x['TF_suffix']}" if x['TF_suffix'] > 1 else x['TF'], axis=1)
    df['reverse_sequence'] = df['motif_sequence'].apply(rev_comp)
    df[['TF', 'motif_sequence', 'reverse_sequence']].to_csv(output_file, sep='\t', index=False, header=False)
    print(f"Processed data saved to '{output_file}'.")

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script uses the JASPAR API to retrieve all motifs reported for Homo sapiens. The script converts the Position Weighted Matrix (PWM) scores into consensus sequence for each motif.")
    parser.add_argument("output_file", help='Path to the output .txt file')
    args = parser.parse_args()
    main(args.output_file)
