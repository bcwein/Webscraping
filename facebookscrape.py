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
from datetime import timedelta
import yaml
import datetime
import concurrent.futures


def dataFrameCreatorFacebook(companyname, companysite, pages=10, timeout=30,
                             group=False):
    """Construct Pandas dataframe for facebook page.

    Args:
        company (string): url identifier for facebook page
        pages (int): No of pages to scroll until termination.
    Returns:
        pandas dataframe: dataframe of company, post, like and comments
    """
    data = []

    if group:
        parsefunc = get_posts(
            group=companysite,
            pages=pages, options={"comments": True},
            cookies="cookies.txt"
        )
    else:
        parsefunc = get_posts(
            companysite,
            pages=pages, options={"comments": True},
            cookies="cookies.txt"
        )

    for post in parsefunc:
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
    with open('data.yml', 'rt', encoding='utf8') as yml:
        data = yaml.load(yml, yaml.FullLoader)

    sites = data['groups']
    pages = data['pages']
    MAX_THREADS = data['max-threads']
    threads = min(MAX_THREADS, len(sites))

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=threads
    ) as executor:
        result = executor.map(
            lambda x: dataFrameCreatorFacebook(
                    x[0],
                    x[1],
                    pages,
                    group=True
            ),
            sites.items()
        )

    parsed = pd.concat(result)
    parsed.to_csv('parsed-groups.csv', index=False)
