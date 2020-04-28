import requests
import json
from bs4 import BeautifulSoup

def ListOfShares():
    hrefs = dict()
    for i in range(65, 91):
        page = requests.Session().get('https://www.moneycontrol.com/india/stockpricequote/'+chr(i))
        parsedpage = BeautifulSoup(page.text, 'html.parser')
        tags = parsedpage.find_all(class_='bl_12')

        for tag in tags:
            try:
                if tag['href'].startswith('http'):
                    hrefs[tag.text] = {'key': tag['href'].rsplit('/', 1)[-1], 'url': tag['href']}
            except Exception:
                pass

    return hrefs

def getvalues(key):
    BSE = lambda: float(json.loads(requests.Session().get('http://priceapi-aws.moneycontrol.com/pricefeed/bse/equitycash/'+key).text)['data']['pricecurrent']) if int(json.loads(requests.Session().get('http://priceapi-aws.moneycontrol.com/pricefeed/bse/equitycash/'+key).text)['code']) == 200 else 'NA'
    NSE = lambda: float(json.loads(requests.Session().get('http://priceapi-aws.moneycontrol.com/pricefeed/nse/equitycash/'+key).text)['data']['pricecurrent']) if int(json.loads(requests.Session().get('http://priceapi-aws.moneycontrol.com/pricefeed/nse/equitycash/'+key).text)['code']) == 200 else 'NA'

    return BSE(), NSE()