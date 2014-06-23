### Set up virtual env

```
virtualenv --no-site-packages --distribute -p /usr/bin/python3.4 ~/.virtualenvs/pywork3
source ~/.virtualenvs/pywork3/bin/activate
pip install -r requirements.txt
add2virtualenv .
```

### Set up database

```
psql psql -U postgres -h localhost
#  CREATE DATABASE pupa_ukraine TEMPLATE=template_postgis;
# \q
export DATABASE_URL=postgis://postgres@localhost/pupa_ukraine
pupa dbinit ua
```


### Scrape!

```
pupa update odessa_region
# use fastmode after first scraping (uses cache)
# pupa update --fastmode odessa_region
```
