import glob
import os
from helper import add_yearly_total
import pandas as pd

input_folder = "/Users/kim/Desktop/repos/Philippines_Visitor/data/yearly_total"

for csv_file in glob.glob(os.path.join(input_folder, "*.csv")):

    filename = os.path.basename(csv_file)

    year = int(filename[:4])

    add_yearly_total(csv_file, year)
