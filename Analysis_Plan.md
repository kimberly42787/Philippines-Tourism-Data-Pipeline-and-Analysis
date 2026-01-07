


## Analytics: 

1. top 10 countries per year. how it changes over time. 
    - I would like to do visually with a map. Cloropeth 
    - Check if there's a better way of doing this
    - Also add in the numbers to see how that differ between each year. 
        - Does this need to have its own visual?


1. Top 10 Countries per Year + Animated World Map

    Insight: Which countries dominate inbound tourism and how rankings change over time
    Visual:
        Plotly choropleth with yearly animation slider
        Bar race chart showing rank shifts

    Why it’s elite:
        Movement over time
        Maps + animation = executive-level dashboard



                SQL QUERY:

                            WITH base AS (
                                SELECT
                                    year,
                                    country,
                                    total_visitors,
                                    LAG(total_visitors) OVER (PARTITION BY country ORDER BY year) AS prev_total
                                FROM yearly_visitors
                            )

                            SELECT
                                year,
                                country,
                                CASE
                                    WHEN prev_total IS NULL OR prev_total = 0 THEN NULL
                                    ELSE ROUND((total_visitors - prev_total) * 100.0 / prev_total, 2)
                                END AS yoy_growth
                            FROM base
                            ORDER BY country, year;


import pandas as pd
import plotly.express as px
import psycopg2

conn = psycopg2.connect("dbname=philippines user=postgres password=xxx")

query = """
SELECT year, country, total_visitors
FROM yearly_visitors;
"""

df = pd.read_sql(query, conn)

fig = px.choropleth(
    df,
    locations="country",            # <-- uses names directly
    locationmode="country names",   # <-- important!!
    color="total_visitors",
    hover_name="country",
    animation_frame="year",
    color_continuous_scale="Viridis",
    title="Philippines Tourist Arrivals By Country"
)

fig.show()

import geopandas as gpd
import pandas as pd

world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

df = pd.read_sql("SELECT country, total_visitors, year FROM yearly_visitors;", conn)

merged = world.merge(df, left_on="name", right_on="country")


Time-Animated Map

Goal: Show how tourist arrivals changed over the years.

Use Plotly’s animation_frame to create a time-lapse map.

fig = px.choropleth(
    df,
    locations="country",
    locationmode="country names",
    color="total_visitors",
    animation_frame="year",
    color_continuous_scale="Viridis",
    title="Tourist Arrivals to the Philippines Over Time"
)
fig.show()




2. YoY Growth Heatmap (Country × Year)

    Insight: Detect surges, declines, and pivotal years for each country
    Visual:
        Heatmap (green = growth, red = contraction)

    Why it stands out:
        Baseline for macro insight
        Looks like something from economic forecasting research





3. Tourism Recovery Index (Pre-COVID vs Post-COVID)

    Insight: Which countries bounced back fastest? Which didn’t recover?
    Visual:
        Slope chart (lines from 2019 → 2024)
        or Bullet chart showing recovery %

    Big wow moment:
        Governments LOVE this metric

4. Rolling 12-Month Visitor Average

Insight: Smooths seasonality → shows true long-term trend
Visual:

Smoothed line chart

Ribbon band for confidence

Advanced:

Shows statistical thinking

5. Forecasting Model (Prophet or ARIMA)

Insight: Predict next 12–24 months
Visual:

Forecast line + confidence interval shading

Upgrade:

Country-level forecasting panel

Interactive region selector

📅 B. Seasonality & Monthly Trends
6. Seasonality Heatmap (Month × Country)

Insight: Which countries peak in which months?
Visual:

Calendar heatmap per country

or Small multiple heatmaps

Why it stands out:

Shows monthly behavior patterns tourism depends on

7. Peak Month Analysis (Clustered Bar or Radar Chart)

Insight: Compare monthly distributions
Visual:

Radar chart comparing “seasonal shape”

Grouped bar for months

Cool factor:

Radar charts look very impressive with 5+ countries

8. Seasonal Decomposition (STL)

Insight: Break down: trend, seasonality, residual noise
Visual:

STL decomposition panels

Expert-level:

Shows modeling & decomposition skills

🌐 C. Geographic Insights
9. Country Contribution Map (Static Choropleth)

Insight: Which regions send the most tourists?
Visual:

Choropleth map with static year selector

10. Regional Contribution Pie + Treemap

Insight: Region-level shares (Europe, Asia, NA…)
Visual:

Sunburst or Treemap

Pie for simplicity

11. Travel Corridor Analysis (Chord Diagram)

Insight: Visualize “travel flow” relationships
Visual:

Chord diagram (Tokyo ↔ Manila, Seoul ↔ Cebu…)

Extremely impressive — not many people build chord diagrams.

📊 D. Rankings & Comparisons
12. Rank Over Time (Bump Chart)

Insight: How rankings change year-to-year
Visual:

Bump chart (ranking lines cross each other)

Perfect for long-term competitive analysis.

13. Market Share Over Time (Stacked Area Chart)

Insight: Which countries take a larger share of total tourism
Visual:

Stacked area chart

Looks amazing when animated.

14. Visitor Concentration Index (H-index style)

Insight: How dependent PH tourism is on top countries
Visual:

Lorenz curve

Gini coefficient calculation

Next-level analytics.

💵 E. Economic & Impact-Related Analytics
15. Tourism Revenue Estimation (if you can add avg spend per visitor)

Visual:

Waterfall chart

Bar chart by market

16. Sensitivity Analysis (if one country drops 20% visitors)

Visual:

Scenario comparison bar chart

This impresses hiring managers.

🤖 F. Machine Learning–Driven Analytics (Very impressive)
17. Visitor Segmentation (K-Means Clustering)

Cluster countries by:

Monthly pattern

Growth behavior

Seasonality shape

Visual:

Cluster scatterplot

Radar chart per cluster

18. Anomaly Detection (Isolation Forest)

Find unusual spikes (e.g., sudden Korea surge).
Visual:

Scatter with anomaly points highlighted

19. Text Insights (If you add tourism news data)

Sentiment vs arrivals
Visual:

Sentiment timeline graph

20. Similarity Map (Country-to-Country Similarity Graph)

Using cosine similarity of seasonality vectors.
Visual:

Network graph

Super unique — perfect portfolio piece.
