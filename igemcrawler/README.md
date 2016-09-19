# iGEM spider crawler


## Usage
In a terminal type:

```
scrapy crawl igemparts -o igemparts.json
```

This will last 1 or 2 hours.
You can tune some crawling parameters in files `igem/spiders/igemparts.py` and `igem/settings.py`.
Then you can get the full list of parts names in Python as follows:

```
with open("./igemparts.json") as fp:
    parts_names = [
        part["name"]
        for part in json.load(fp)
    ]
```
