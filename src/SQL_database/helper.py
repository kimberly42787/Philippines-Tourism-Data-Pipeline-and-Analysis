import pandas as pd
from sqlalchemy import create_engine
import os
import re

# --- Database Connection ---
password = os.getenv("DB_PASSWORD")
engine = create_engine(
    f"postgresql+psycopg2://postgres:{password}@localhost:5432/philippines_tourism_db"
)

# --- Constants ---
MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

EXCLUDE_WORDS = [
    "grand total",
    "overseas filipino",
    "total foreign"
]

# --- Helpers ---
def get_months(df):
    """Return ordered list of existing month columns."""
    return [m for m in MONTH_ORDER if m in df.columns]


def normalize_country(name: str):
    """Standardize country name formatting before filtering & mapping."""
    name = str(name)

    # Remove SAR suffix or anything after a dash
    name = re.sub(r"\s*-\s*.*", "", name)

    # Remove symbols/parentheses
    name = re.sub(r"[^A-Za-z\s]", "", name)

    return name.strip().title()


def normalize_for_exclude(name: str):
    """Normalize for exclusion filtering only."""
    name = re.sub(r"[^a-z\s]", "", str(name).lower())
    return name.strip()


# --- Load Country List for Mapping ---
country_list = pd.read_sql("SELECT country_id, country FROM public.countries_list", engine)
country_mapping = dict(zip(country_list['country'].str.title(), country_list['country_id']))

# --- Main Function ---
def add_monthly_to_db(csv_file, year):
    """Load, clean, transform, and insert monthly CSV visitor data into SQL."""

    # Load CSV
    df = pd.read_csv(csv_file)

    # Work on a copy
    df_copy = df.copy()
    df_copy.rename(columns={'Country': 'country'}, inplace=True)

    # Clean up country names
    df_copy['country'] = df_copy['country'].apply(normalize_country)

    # Extract existing month columns
    months = get_months(df_copy)
    df_copy = df_copy[['country'] + months]

    # Melt to (country, month, visitors)
    melted_df = df_copy.melt(id_vars=['country'], var_name='month', value_name='visitors')

    # Clean visitors column
    melted_df['visitors'] = (
        melted_df['visitors']
        .replace('-', 0)
        .replace(',', '', regex=True)
    )

    melted_df['visitors'] = pd.to_numeric(melted_df['visitors'], errors='coerce')

    # Map country → country_id
    melted_df['country_id'] = melted_df['country'].map(country_mapping)

    # Show unmatched
    unmatched = melted_df.loc[melted_df['country_id'].isna(), 'country'].unique()
    print("\nUnmatched countries:", unmatched, "\n")

    # Fill required columns
    melted_df['year'] = year
    melted_df['visitors'] = melted_df['visitors'].fillna(0).astype(int)

    # Final format for SQL
    final_df = melted_df[['country_id', 'month', 'visitors', 'year']]

    # Write to SQL
    final_df.to_sql("monthly_visitors", engine, if_exists="append", index=False)

    print(f"Successfully added data for {year}!")


def add_special_cat(csv_file, year):

    df = pd.read_csv(csv_file)

    df_copy = df.copy()

    df_copy.rename(columns={"Country": "category"}, inplace=True)

    # Extract existing month columns
    months = get_months(df_copy)

    df_copy = df_copy[['category'] + months]

    # Melt to (country, month, visitors)
    melted = df_copy.melt(
        id_vars=["category"],
        var_name="month",
        value_name="visitors"
    )

    melted['year'] = year

    melted['visitors'] = pd.to_numeric(melted['visitors'].str.replace(',', '', regex=True), errors='coerce').fillna(0).astype(int)

    final_df = melted[['category', 'year', 'month', 'visitors']]

    final_df.to_sql("special_categories", engine, if_exists="append", index=False)

    print(f"Successfully added data for {year}!")


def add_yearly_total(csv_file, year):

    df = pd.read_csv(csv_file)

    df_copy = df.copy()
    
    df_copy.rename(columns={
                    'Total' : 'total_visitors',
                    'Percentage' : 'percentage',
                    'Previous Total' : 'previous_year_total',
                    'Growth Rate' : 'growth_rate'}, inplace=True)

    # Map country → country_id
    df_copy['country_id'] = df_copy['Country'].map(country_mapping)

    # Fill required columns
    df_copy['year'] = year

    # Final format for SQL
    final_df = df_copy[['country_id', 'year', 'total_visitors', 'percentage', 'previous_year_total', 'growth_rate']]

    final_df.to_sql("yearly_visitors", engine, if_exists="append", index=False)

    print(f"Successfully added data for {year}!")