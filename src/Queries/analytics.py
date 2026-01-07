import pandas as pd
from db_conn import get_engine

query = """
SELECT *
FROM (
    SELECT 
        c.country,
        y.year,
        y.total_visitors,
        RANK() OVER (
            PARTITION BY y.year 
            ORDER BY y.total_visitors DESC
        ) AS rank
    from yearly_visitors y
    JOIN countries_list c
        ON y.country_id = c.country_id
) AS ranked
WHERE rank <= 10
ORDER BY year, rank;
"""

def get_top10_per_year():
    engine = get_engine()
    df = pd.read_sql(query, engine)
    return df


print(get_top10_per_year())