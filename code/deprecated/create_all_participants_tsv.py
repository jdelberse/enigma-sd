### Author: JD Elberse
### Date: 12/06/24
### This code takes all TSVs and stores them in one central TSV

import os, glob
import pandas as pd

all_tsv = pd.DataFrame()

# Loop over datasets
for dataset in glob.glob("*-bids"):
    print(f"Scanning {dataset}")
    filename = f"{dataset}/derivatives/participants_with_indices.tsv"
    
    if os.path.exists(filename):
        tsv = pd.read_csv(filename, sep='\t')
        print(f"TSV found")
    else:
        print(f"No TSV found")
        continue

    if all_tsv.shape == (0, 0):
        all_tsv = tsv
    else:
        all_tsv = pd.concat([all_tsv, tsv], ignore_index=True)

outname = "all_participants_with_indices.tsv"    
all_tsv.to_csv(outname, sep='\t')
print(f"Saved as {outname}")