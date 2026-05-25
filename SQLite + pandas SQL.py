import pandas as pd
import sqlite3

df = pd.read_csv("spacex_cleaned_data.csv")
df.head()

conn = sqlite3.connect(":memory:")
df.to_sql("spacex", conn, index=False, if_exists="replace")

query = """
SELECT flight_number, rocket_name, launch_site, payload_mass, success
FROM spacex
LIMIT 10;
"""

print(pd.read_sql(query, conn))
query = """
SELECT success, COUNT(*) as total
FROM spacex
GROUP BY success;
"""


print(pd.read_sql(query, conn))
query = """
SELECT launch_site,
       COUNT(*) as total_launches,
       SUM(success) as successful_launches
FROM spacex
GROUP BY launch_site
ORDER BY successful_launches DESC;
"""

print(pd.read_sql(query, conn))
query = """
SELECT 
    CASE
        WHEN payload_mass < 5000 THEN 'Low'
        WHEN payload_mass BETWEEN 5000 AND 10000 THEN 'Medium'
        ELSE 'High'
    END as payload_category,
    AVG(success) as success_rate
FROM spacex
GROUP BY payload_category;
"""

print(pd.read_sql(query, conn))
query = """
SELECT rocket_name,
       COUNT(*) as launches,
       AVG(success) as success_rate
FROM spacex
GROUP BY rocket_name
ORDER BY success_rate DESC;
"""

print(pd.read_sql(query, conn))
query = """
SELECT substr(date_utc,1,4) as year,
       AVG(success) as success_rate
FROM spacex
GROUP BY year
ORDER BY year;
"""


print(pd.read_sql(query, conn))

