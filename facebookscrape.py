"""
Webscraping of companies for extracting facebook post stats.

This module extracts:
    - Post date
    - No of likes
    - No of comments

And it returns a dataframe of companies and their posts.

All data input in this code is seperated into yaml files not included in the
repository.
"""
# %%
from facebook_scraper import get_posts
import pandas as pd
import time
from datetime import timedelta
import yaml


def dataFrameCreatorFacebook(companyname, companysite, pages=10):
    """Construct Pandas dataframe for facebook page.

    Args:
        company (string): url identifier for facebook page
        pages (int): No of pages to scroll until termination.
    Returns:
        pandas dataframe: dataframe of company, post, like and comments
    """
    data = []
    for post in get_posts(companysite, pages=pages, options={"comments": True},
                          cookies="cookies.txt"):
        try:
            data.append(
                [companyname, post['time'], post['likes'], post['comments']]
            )
        except Exception as ex:
            continue
    return pd.DataFrame(data, columns=["site", "time", "likes", "comments"])


# %%
if __name__ == '__main__':
    """Main function.

    This main function does the following:
        1. Load input data from data.yml
        2. Create a list of dataframes with list comprehension.
        3. Concatenate Dataframes.
        4. Save dataframe to csv.
    """
    data = yaml.load(open('data.yml'), Loader=yaml.FullLoader)
    sites = data['sites-wholesale']
    result = [dataFrameCreatorFacebook(
            name, site, pages=100) for name, site in sites.items()]
    parsed = pd.concat(result)
    parsed.to_csv('parsed-wholesale.csv')
