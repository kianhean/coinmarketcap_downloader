import pandas as pd


def all_currencies():
    """Get List of all Currencies
    
    Returns:
        [List] -- [List of all Currencies]
    """

    url = 'https://coinmarketcap.com/all/views/all/'
    df = pd.read_html(url, attrs = {'id': 'currencies-all'})[0]

    coins = []
    for name in df['Name']:
        coin_name = (name.lower().split(' ')[1:])
        final = ''
        for x in coin_name:
            final += x + '-'
        coins.append(final[:-1])
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
        df = pd.read_html(url, attrs = {'class': 'table'})[0]
        
        # Clean data
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market Cap']
        df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')

        # Save to CSV
        df.to_csv('data/' + currency + '.csv', index=False)
    except:
        print("Error : Could not Download - " + currency)


if __name__ == "__main__":

    # Download all Historical Data
    currencies = all_currencies()

    for currency in currencies:
        download_data(currency, '20000101', '20181231')
