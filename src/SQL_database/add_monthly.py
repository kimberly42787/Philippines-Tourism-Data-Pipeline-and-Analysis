
import glob
from helper import add_monthly_to_db
import os
import pandas as pd

input_folder = "/Users/kim/Desktop/repos/Philippines_Visitor/data/monthly_visitors"

for csv_file in glob.glob(os.path.join(input_folder, "*.csv")):
    
    filename = os.path.basename(csv_file)

    print("Reading:", csv_file, type(csv_file))

    year = int(filename[:4])

    add_monthly_to_db(csv_file, year)

    print("Inserted:", filename, " Year:", year)


