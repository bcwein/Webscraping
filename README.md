# Webscraping

This is a simple webscraping tool used to collect simple metrics of social
media data.

## Facebookwebscrape

Facebookwebscrape.py is based on 
[Facebook Scraper](https://github.com/kevinzg/facebook-scraper) and uses 
Facebook Scrapers get_posts method to extract simple metrics from facebook 
posts. 

There are some things to set up before this code is fully functional. This is 
discussed in the sections below.

### Input data
The code iterates through a dictionary of facebook pages to scrape. This is stored in 
*data.yml* and extracted like this:

```python
data = yaml.load(open('data.yml'), Loader=yaml.FullLoader)
sites = data['page-dictionary-name']
result = [dataFrameCreatorFacebook(
        name, site, pages=100) for name, site in sites.items()]
```

The format of the yml file is like so:

```yml
page-dictionary-name:
  company1: page1
  company2: page2
  company3: page3
  company4: page4
  company5: page5
```

It should be stated that the items in this list is the last part of the full
url to the facebook group of interest

```
https://www.facebook.com/page1/
```

### Cookies

Due to an issue with scraping open pages as per this 
[issue](https://github.com/kevinzg/facebook-scraper/issues/28#issuecomment-793066983)
which is not resolved as of today (4th of June 2021) the cookie of your facebook
session is needed. This is stored in the NETSCAPE format and stored as
*cookies.txt*  in the root directory of the repo. 

Use a web extension for cookie extraction to do this.