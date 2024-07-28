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

<form action="/occupation-data/pie.cgi">
<label for="r">Authority</label>
<select id="r" name="r">
<option value="Choose..." selected>Choose...</option>
{"".join(f"<option value='{a}'>{a}</option>" for a in authorities)}
</select>
<button type="Submit">See data</button>
</form>

</body>
</html>
""")

