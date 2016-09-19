# Scripts for downloading the iGEM registry of parts

## Motivation

The iGEM database features thousands of DNA parts gathered over the years.
Yet these parts cannot be dowloaded at once, and the database API is not awesome (for starters, there is no  list of all available parts).

This project provides scripts to download the whole iGEM database, for fun, for research, for deploying a mirror, etc.

A first script crawls the whole iGEM website and gathers part names. A second script downloads the corresponding parts. The scripts leave pauses between requests in order not to overload the iGEM website.

This project come with no warranty whatsoever, it just worked for us and we wanted to share.

## Licence

The scripts were originally written at the [Edinburgh Genome Foundry](http://genomefoundry.org/) by [Zulko](https://github.com/Zulko).
The code is released on [Github](https://github.com/Edinburgh-Genome-Foundry/SBOL-Visual-CSS) under the Public domain (Creative Commons 0) licence by the Edinburgh Genome Foundry.

If something doesn't work for you, please open an issue.

If you found this project useful, please give credit or spread the word.


## Usage

Before anything else, install the dependencies:

```
(sudo) pip install scrapy xmltodict dataset
```

 This will install `scrapy` (library used for crawling the iGEM website), `xmltodict` (to parse the xml returned by the iGEM API) and `dataset` (simple library to build a database).



Now we will crawl the iGEM website to get a list of all the parts names in the registry.
Go to the `igemcrawler` directory (containing the `scrapy.cfg` file) and run:

```
scrapy crawl igemcrawler -o igemparts.json
```

This may take 1 or 2 hours, and will output a `igemparts.json` file containing the names of all iGEM parts found in the website. Note that it crawls only until year 2015 (just change the `MAX_YEAR` variable in file `spiders/igemparts.py` if you're reading that in 2017+).

The next step is to download the data on all the part names found:

```
python parts_downloader.py
```

This downloads ~26k parts data as xml files in a `parts_xml` folder. This takes a few hours as it waits a little between the queries . If the iGEM API is capricious, some parts downloads may fail. You can retry to get these parts later by re-running the `parts_downloader.py` script, it will ignore the already-downloaded parts info and will retry the failed ones.

Once all the xml files are downloaded, you can make a database. The script `xml_to_database.py` is just there to provide an example and creates an SQLite database.

```
python xml_to_database.py
```
