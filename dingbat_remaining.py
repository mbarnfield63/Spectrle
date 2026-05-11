# dingbats_remaining.py - A python script for outputting the remaining dingbats

import pandas as pd

# Confirmed done
done = [22, 193, 219]

# Load the dingbats data from the CSV file
main_df = pd.read_csv("ExoTea_Master.csv")
dingbats = main_df["Dingbat"].unique()
full = set(range(1, 225))
remaining_dingbats = full - set(dingbats) - set(done)
remaining_dingbats = sorted(list(remaining_dingbats))
# Output the remaining dingbats
print("Remaining Dingbats:")
for dingbat in remaining_dingbats:
    print(dingbat)
