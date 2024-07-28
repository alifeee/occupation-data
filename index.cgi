#!/var/www/cgi/occupation-data/env/bin/python3

import csv

CSVFILE = "TS060-2021-1.csv"
with open(CSVFILE, 'r', encoding="utf-8") as file:
  reader = csv.DictReader(file)
  data = list(reader)

authorities = sorted(set(d["Lower Tier Local Authorities"] for d in data))

print("Content-type: text/html")
print()
print(f"""<!DOCTYPE html>
<html lang="en">
<head>
<style>
body {{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}}
</style>
</head>
<body>

<h1>Occupation data from the UK Census 2021</h1>

<p>
  <a href="https://github.com/alifeee/occupation-data">more context</a>
</p>

<h2>As Graph</h2>

<form action="/occupation-data/pie.cgi">
<label for="r">Authority</label>
<select id="r" name="r">
<option value="Choose..." selected>Choose...</option>
{"".join(f"<option value='{a}'>{a}</option>" for a in authorities)}
</select>
<button type="Submit">See graph</button>
</form>

<h2>As List</h2>

<form action="/occupation-data/list.cgi">
<label for="r">Authority</label>
<select id="r" name="r">
<option value="Choose..." selected>Choose...</option>
{"".join(f"<option value='{a}'>{a}</option>" for a in authorities)}
</select>
<button type="Submit">See entire list</button>
</form>

</body>
</html>
""")

