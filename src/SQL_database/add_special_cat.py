import glob
import os
from helper import add_special_cat
import pandas as pd

input_folder = "/Users/kim/Desktop/repos/Philippines_Visitor/data/special_category"

for csv_file in glob.glob(os.path.join(input_folder, "*.csv")):

    filename = os.path.basename(csv_file)

    year = int(filename[:4])

    add_special_cat(csv_file, year)

    

