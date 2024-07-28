#!/var/www/cgi/occupation-data/env/bin/python3

import io
import os
import sys
import matplotlib.pyplot as plt
import matplotlib
import pandas
import random
import numpy
from urllib.parse import urlparse, parse_qs

CSVFILE = "TS060-2021-1.csv"

qs = parse_qs(os.environ["QUERY_STRING"])

# get location from query string, i.e., "?r=Sheffield"
LOCATION = qs.get('r', [""])[0]

df = pandas.read_csv(CSVFILE)
df.set_index('Industry (current) (88 categories)', inplace=True)
df.head()

if LOCATION not in set(df["Lower Tier Local Authorities"]):
  # print("HTTP/1.0 400 Bad Request")
  print("Status:400")
  print()
  print(f"<{LOCATION}> is not in the list of locations. Please see:")
  print("https://geoportal.statistics.gov.uk/documents/d1fab2d9fb0a4576a7e08f89ac7e0b72/about")
  print("Accepted locations follow:")
  print()
  for loc in sorted(set(df["Lower Tier Local Authorities"])):
    print(loc)
  sys.exit(1)

localdf = df[df["Lower Tier Local Authorities"] == LOCATION]
DNA_number = localdf["Observation"]["Does not apply"]
# drop DOES NOT APPLY
localdf = localdf.drop("Does not apply")
total_applies = localdf["Observation"].sum()
localdf.head()

SOME_THRESHOLD = total_applies / 100

def combine_other(row):
    if row["Observation"] < SOME_THRESHOLD:
        return 'Other (<1%)'
    return row.name

localdf.loc[:, 'combined_label'] = localdf.apply(combine_other, axis=1)

pdf = localdf.groupby('combined_label').sum(numeric_only=True)
pdf.tail()

prop_cycle = plt.rcParams['axes.prop_cycle']
colours = list(matplotlib.colors.cnames.items())
random.seed(21412562)
random.shuffle(colours)
colours = colours[:-1]


pdf = pdf.sort_values(by="Observation")

fig = plt.figure(figsize=(10, 20))
ax, ax2 = fig.subplots(2, 1)
fig.tight_layout()

obscolours = []
for i in pdf["Industry (current) (88 categories) Code"]:
    if i > len(colours):
        c = colours[0][1]
    else:
        c = colours[i % len(colours)][1]
    obscolours.append(c)

ax.pie(
    pdf["Observation"],
    labels=[f"{ind} - {pdf['Observation'][ind]}" for ind in pdf.index],
    autopct='%.1f%%',
    colors=obscolours,
    explode=[0.05 if b == "Other (<1%)" else 0 for b in pdf.index],
    pctdistance=0.8,
    labeldistance=1.05,
    startangle=-60,
    radius=1,
)

ratio = DNA_number / total_applies

ax2.pie(
    [DNA_number],
    labels=["Does not apply"],
    radius=numpy.sqrt(ratio),
    autopct=lambda pct: DNA_number,
    pctdistance=0,
)

ax.set_title(f"Industry and Occupation data for {LOCATION}\nFrom Census 2021 Data")
ax2.set_title(f"Total does not apply: {DNA_number} people")
plt.suptitle(f"Total with data: {total_applies} people")

plt.figtext(
  0.5,
  0.01,
  "https://www.ons.gov.uk/datasets/TS060/editions/2021/versions/1",
  ha="center",
  fontsize=16,
  url='https://www.ons.gov.uk/datasets/TS060/editions/2021/versions/1',
  color="blue",
)

buf = io.StringIO()

plt.savefig(
    buf,
    format="svg",
    bbox_inches="tight",
)

svg_str = buf.getvalue()

# print("Content-type: text/plain")
print("Content:type: image/svg+xml")
print()
print(svg_str)
