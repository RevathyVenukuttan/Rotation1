import pandas as pd
import numpy as np
import sys
import os

## generate enhancer sequence by chromosome and save as the format of test-variant.py input file

forward_ap1 = 'TGAGTCAT'
backward_ap1 = 'ATGACTCA'

step = 20
distance = np.arange(23, 244, step)


def gen_seq(ap1,motif2,df,start):
    ls_loc = []
    ls_score = []
    ls_distance = []
    ls_seq = []
    ls_ref = []
    ls_allele = []

    for i in range(len(df)):
        seq = df.loc[i,'sequence']

        for j in range(len(distance)):
            ls_loc.append(df.loc[i,'location'])
            ls_score.append(df.loc[i,'refScore'])
            ls_distance.append(distance[j])
            
            ### fix ap1, move 2nd motif
            seq_tmp = seq[:start-1]+ap1+seq[start+len(ap1)-1:start+distance[j]-1]+motif2+seq[start+distance[j]-1+len(motif2):]
            if len(seq_tmp)!=300:
                raise Exception('length error')
            ls_seq.append(seq_tmp)
            ls_ref.append('ref='+seq_tmp[150])
            ls_allele.append(seq_tmp[150])


    return pd.DataFrame({'location':ls_loc,
                         'ref':ls_ref,
                         'allele':ls_allele,
                         'sequence':ls_seq,
                         'distance':ls_distance,
                         'ref_score':ls_score
                         })



def main(ref_seq_dir,motif_sequence_file,output_dir,num_seq,start):

    ref_seq_files = [f for f in os.listdir(ref_seq_dir) if f.endswith('.txt')]
    motif_file = pd.read_csv(motif_sequence_file, sep='\t')
    
    for ref_seq in ref_seq_files:
        for i in range(len(motif_file['TF'])):
            
            forward_motif = motif_file['motif_sequence'][i]
            reverse_motif = motif_file['reverse_sequence'][i]
            motif_name = motif_file['TF'][i]
            
            chromosome = ref_seq.split('.')[0]
            df = pd.read_csv(ref_seq_dir+'/'+ref_seq, sep='\t', header=None)
            df.columns = ['location','refScore','sequence']
            df = df.sort_values(by = 'refScore')
            df = df.reset_index(drop = True)
            df = df.iloc[:num_seq,:]

            gen_seq(forward_ap1,forward_motif,df,start).to_csv(output_dir+'/'+chromosome+'-f-ap1-f-'+motif_name+'.txt', sep = '\t', header = None, index = False)
            gen_seq(forward_ap1,reverse_motif,df,start).to_csv(output_dir+'/'+chromosome+'-f-ap1-b-'+motif_name+'.txt', sep = '\t', header = None, index = False)
            gen_seq(backward_ap1,forward_motif,df,start).to_csv(output_dir+'/'+chromosome+'-b-ap1-f-'+motif_name+'.txt', sep = '\t', header = None, index = False)
            gen_seq(backward_ap1,reverse_motif,df,start).to_csv(output_dir+'/'+chromosome+'-b-ap1-b-'+motif_name+'.txt', sep = '\t', header = None, index = False)

if(len(sys.argv)!=6):
    exit(ProgramName.get()+" <ref_seq_score_dir> <motif_sequence> <output_dir> <num_seq> <start_pos_ap1>\n")
(ref_seq_dir, motif_sequence, output_dir, num_seq, start)=sys.argv[1:]
main(ref_seq_dir, motif_sequence, output_dir, int(num_seq), int(start))
