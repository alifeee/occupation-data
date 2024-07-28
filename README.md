# Occupation data

Plotting Industry and occupation data from the ONS 2021 census.

See example on <http://server.alifeee.co.uk/occupation-data/region.cgi?r=Sheffield> or in [`plot.ipynb`](./plot.ipynb)

Dataset: <https://www.ons.gov.uk/datasets/TS060/editions/2021/versions/1>

## Use

Install required Python modules

```bash
python -m venv env
. ./env/bin/activate
pip install -r requirements.txt
```

## With Jupyter Notebook

Open `plot.ipynb`.

## As a CGI script

Install to location

```bash
mkdir -p /var/www/cgi/
cd /var/www/cgi/
git clone git@github.com:alifeee/occupation-data
cd occupation-data
python -m venv env
. ./env/bin/activate
pip install -r requirements.txt
```

Install fastcgi

```bash
sudo apt-get install fastcgi
```

Add the following to nginx config

```nginx
                location /occupation-data/ {
                        fastcgi_intercept_errors on;
                        include fastcgi_params;
                        fastcgi_param SCRIPT_FILENAME /var/www/cgi/$fastcgi_script_name;
                        fastcgi_pass unix:/var/run/fcgiwrap.socket;
                }
```
