import time
import urllib.request
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup


def all_currencies():
    """Get List of all Currencies

    Returns:
        [List] -- [List of all Currencies]
    """
    coins = []
    url = 'https://coinmarketcap.com/all/views/all/'

    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, features="lxml")
    all_links = [a.get('href') for a in soup.find_all('a', href=True)]

    for link in list(set(all_links)):
        if '/currencies/' in link:
            coins.append(link.split('/')[2])

    return coins

def download_data(currency, start_date, end_date):
    """Download Historical Data to File

    Arguments:
        currency {[str]} -- [currency of crypto]
        start_date {[str]} -- [date yyyymmdd]
        end_date {[str]} -- [date yyyymmdd]
    """

    print("Running " + currency)

    try:
        # Get Html to DF
        url = 'https://coinmarketcap.com/currencies/' + currency + '/historical-data/' + '?start=' \
            + start_date + '&end=' + end_date
        df = pd.read_html(url, attrs={'class': 'table'})[0]

        # Clean data
        df.columns = ['Date', 'Open', 'High',
                      'Low', 'Close', 'Volume', 'Market Cap']
        df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')

        # Save to CSV
        df.to_csv('data/' + currency + '.csv', index=False)
    except Exception as e:
        print("Error : Could not Download - " + currency)
        print(e)


if __name__ == "__main__":

    # Download all Historical Data
    currencies = all_currencies()

    today = pd.to_datetime('today').strftime('%Y%m%d')

    for currency in currencies:

        my_file = Path('data/' + currency + '.csv')

        if my_file.is_file() == False:
            time.sleep(2)
            download_data(currency, '20000101', today)
