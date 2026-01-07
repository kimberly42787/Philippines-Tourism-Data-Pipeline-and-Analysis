from sqlalchemy import create_engine
import pandas as pd
import os

password = os.getenv("DB_PASSWORD")

engine = create_engine (
    f"postgresql+psycopg2://postgres:{password}@localhost:5432/philippines_tourism_db"
)

unique_countries = pd.read_csv(
    "/Users/kim/Desktop/repos/Philippines_Visitor/src/Unique_Countries_List/unique_countries.csv"
)

countries_df = pd.DataFrame(unique_countries)

countries_df.rename(columns={'Country': 'country'}, inplace=True)

countries_df.to_sql("countries_list", engine, if_exists="append", index=False)
print("Data is added to the countries_list table")