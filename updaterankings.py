import numpy as np
import pandas as pd
import os

print()
filename = input("Filename for new rankings (e.g., updated_rankings.csv): ")
if not os.path.exists(filename):
    raise FileNotFoundError(f"File {filename} does not exist. Please check the file path.")

new_rankings = pd.read_csv(filename)
new_rankings.drop(columns=["Rank"], inplace=True)  # Remove the old Rank column
new_rankings.rename(columns={"Personal Rank": "Rank"}, inplace=True)  # Rename Personal Rank to Rank
new_rankings = new_rankings[["Rank", "Player", "Pos", "Team", "ADP", "Pos Rank", "Bye", "Notes"]]  # Reorder columns

new_rankings.to_csv(filename, index=False)  # Save the updated rankings