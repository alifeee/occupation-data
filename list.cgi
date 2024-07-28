#!/var/www/cgi/occupation-data/env/bin/python3

import csv
import os
import sys
from urllib.parse import parse_qs
import pandas

qs = parse_qs(os.environ["QUERY_STRING"])
LOCATION = qs.get('r', [""])[0]

CSVFILE = "TS060-2021-1.csv"
df = pandas.read_csv(CSVFILE)
df.set_index("Industry (current) (88 categories)", inplace=True)

if LOCATION == "ALL":
  localdf = df.groupby(df.index).agg({"Observation": "sum", 'Industry (current) (88 categories) Code': "min"})
elif LOCATION in set(df["Lower Tier Local Authorities"]):
  localdf = df[df["Lower Tier Local Authorities"] == LOCATION]
else:
  print("Status:400")
  print()
  print(f"<{LOCATION}> is not in the list of locations.")
  print("Select location with query string, e.g., /occupation-data/list.cgi?r=Sheffield")
  print("Please see:")
  print("https://geoportal.statistics.gov.uk/documents/d1fab2d9fb0a4576a7e08f89ac7e0b72/about")
  print("Accepted locations follow:")
  print()
  for loc in sorted(set(df["Lower Tier Local Authorities"])):
    print(loc)
  sys.exit(1)

localdf = localdf.sort_values("Observation", ascending=False)

print("Content-type: text/html")
print()
print(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
h1 {{
  text-align: center;
}}
table td {{
  max-width: 25rem;
}}
</style>
</head>
<body>

<h1>Occupation data for {LOCATION}</h1>

<a href="/occupation-data/">back to main page</a>

<table>
  <tr>
    <th>
      Industry (current) (88 categories)
    </th>
    <th>
      Observation (I think number of people), total={localdf["Observation"].sum():,}
    </th>
  </tr>
""")

for key, row in localdf.iterrows():
  print("<tr>")
  print(f'<td>{key}')
  print(f'<td>{row["Observation"]:,}')
  print("</tr>")

print("""
</table>

</body>
</html>
""")

