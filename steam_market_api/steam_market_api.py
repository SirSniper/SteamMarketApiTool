"""
Lasted Edited on May 21, 2017
"""

import requests, urllib, locale

"""
Valid currency codes
--------------------
"""
curAbbrev = {
    'USD' : 1,
    'GBP' : 2,
    'EUR' : 3,
    'CHF' : 4,
    'RUB' : 5,
    'KRW' : 16,
    'CAD' : 20,
}

"""
Formats the varying prices from Steam's API as they are formatted based on locale and currency
Removes the currency symbol and sets the locale to convert the currency to a float
"""
def format_price(price_string, currency):
    formatted_string = price_string
    if(currency == 'USD'):
        formatted_string = formatted_string.replace('$','')
        locale.setlocale(locale.LC_NUMERIC, 'en-US')
    elif(currency == 'GBP'):
        formatted_string = formatted_string.replace('\u00a3','')
        locale.setlocale(locale.LC_NUMERIC, 'en-GB')
    elif(currency == 'EUR'):
        formatted_string = formatted_string.replace('\u20ac','')
        locale.setlocale(locale.LC_NUMERIC, 'fr-FR')
    elif(currency == 'CHF'):
        formatted_string = formatted_string.replace('CHF ','')
        locale.setlocale(locale.LC_NUMERIC, 'en-US')
    elif(currency == 'RUB'):
        formatted_string = formatted_string.replace(' p\u0443\u0431.','')
        locale.setlocale(locale.LC_NUMERIC, 'ru-RU')
    elif(currency == 'KRW'):
        formatted_string = formatted_string.replace('\u20a9 ','')
        locale.setlocale(locale.LC_NUMERIC, 'ko-KR')
    elif(currency == 'CAD'):
        formatted_string = formatted_string.replace(' p\u0443\u0431.','')
        locale.setlocale(locale.LC_NUMERIC, 'en-CA')
    return locale.atof(formatted_string)
    
"""
Gets item data from the steam market.

@param name: the full name of the steam market item
@param appid: the steam id for the game you are utilizing (for instance Counter Strike: Global Offensive is 730)
@param currency: the currency code for the item you are requesting from the following list: USD, GBP, EUR, CHF, RUB, KRW, CAD

get_lowest_price
@return: the lowest price of the item

get_volume
@return: the number of item listings

get_median_price
@return: the average price of the item listings
"""
class MarketItem:
    def __init__(self, name, appid, currency):
        self.name = name
        self.appid = appid
        self.currency = currency
        self.get_item(appid, currency, name)
        
    def get_item(self, app_id, currency, name):
        url = 'http://steamcommunity.com/market/priceoverview/?'
        #Checks to see if the currency is valid and raises and exception if not
        if(not(curAbbrev.__contains__(currency))):
            raise NameError('Invalid Currency Code, should be one of: USD, GBP, EUR, CHF, RUB, KRW, CAD')
        #Payload for http get request
        data = { 'appid' : self.appid,
            'currency' : curAbbrev[self.currency],
            'market_hash_name' : self.name
        }
        encoded_data = urllib.parse.urlencode(data)
        encoded_data = encoded_data.encode("utf-8")
        resp_json = requests.get(url, encoded_data).json()
        #Checks to see if the request succeeded and fills with obviously false data
        if(resp_json.__getitem__('success') == 'False'):
            self.lowest_price = -9999
            self.volume = 0
            self.median_price = -9999
            raise "Query Failed, ensure that the name and app id are correct"
        else:
            self.lowest_price = format_price(resp_json.__getitem__('lowest_price'),currency)
            self.volume = int(resp_json.__getitem__('volume'))
            self.median_price = format_price(resp_json.__getitem__('median_price'),currency)

    #Allows user to get the different information for an item
    def get_lowest_price(self):
        return self.lowest_price
    
    def get_volume(self):
        return self.volume
    
    def get_median_price(self):
        return self.median_price

"""
Takes an array of item names from the same app id

Returns a dictionary with the keys as item names and the values as prices in the specified currency

Will run through all the names and will fill failed names with -9999 as the value
"""    
def get_lowest_of_each(names, appid, currency):
    price_dict = {}
    try:
        if(len(names) == 0):
            raise TypeError('Names should contain at least 1 name in list')
    except Exception as e:
        raise TypeError('Names should be a list')
    for name in names:
        try:
            item = MarketItem(name, appid, currency)
            price_dict[name] = item.get_lowest_price()
        except Exception as e:
            print('Error getting item')
    return price_dict
