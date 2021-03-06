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
import yaml


def dataFrameCreatorFacebook(companyname, companysite, pages=10, timeout=30,
                             group=False):
    """Construct Pandas dataframe for facebook page.

    Args:
        companyname (string): url identifier for facebook page
        companysite (string or int):
        pages (int): No of pages to scroll until termination.
        timeout (int): Waiting time for post until timout.
        group (boolean): used for conditional parser function.

    Returns:
        pandas dataframe: dataframe of company, post, like and comments
    """
    data = []

    # Conditionally use group argument to parse group or pages.
    if group:
        parsefunc = get_posts(
            group=companysite,
            pages=pages, options={"comments": True},
            cookies="cookies-bcw.txt"
        )
    else:
        parsefunc = get_posts(
            companysite,
            pages=pages, options={"comments": True},
            cookies="cookies-bcw.txt"
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
        2. Use multithreaded map to apply dataframecreation for all elements in
        list.
        3. Concatenate Dataframes.
        4. Save dataframe to csv.
    """
    with open('data.yml', 'rt', encoding='utf8') as yml:
        data = yaml.load(yml, yaml.FullLoader)

    sites = data['groups']
    pages = data['pages']
    csv = data['csv']

    result = []

    for name, site in sites.items():
        try:
            result.append(dataFrameCreatorFacebook(
                        name, site, pages=pages, group=True
                    ))
        except Exception:
            parsed = pd.concat(result)
            parsed.to_csv(csv, index=False)

    parsed = pd.concat(result)
    parsed.to_csv(csv, index=False)
