##
##from walmart_api_client import WalmartApiClient
##walmart = WalmartApiClient('7e7vuju342knmhsjnqz7grbe')
##
##walmart.search()

# https://docs.google.com/spreadsheets/d/1tMPJCTxO_eysx3CnSdeq-dhY_1wyBdrCy-UjO-pKvFU/edit#gid=0

from __future__ import print_function
import httplib2
import os

from wapy.api import Wapy
from wapy.api import WalmartProduct


wapy = Wapy('7e7vuju342knmhsjnqz7grbe')

def fromWalmart(productID):
    # products = wapy.search('Lays')
    
    #for productID in productIDs:
        
        # print(product.name)
        # ID = product.item_id
        # print(ID)
        
    prices = wapy.product_lookup(str(productID))
    return prices.sale_price

    



from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    # https://www.googleapis.com/auth/spreadsheets
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1tMPJCTxO_eysx3CnSdeq-dhY_1wyBdrCy-UjO-pKvFU'
    rangeName = 'Sheet1!B2:B8'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Product ID:')
        productIDs = values
        for column in values:
            print('%s' % (column[0]))
            prices = fromWalmart(column[0])
            print(prices)
            
            values = [[prices],]
            body = {'values': values}
            value_input_option = 'USER_ENTERED'
            result = service.spreadsheets().values().update(
                spreadsheetId=spreadsheetId, range='Sheet1!D2',
                valueInputOption=value_input_option, body=body).execute()


if __name__ == '__main__':
    main()
