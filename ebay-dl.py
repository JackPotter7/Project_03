### IMPORTS  ###
import argparse
import requests
from bs4 import BeautifulSoup
import json
import csv


def parse_itemssold(text):
    '''
    Takes as input a string and returns the numer of itmes sold, as specified in the string.
    
    >>> parse_itemssold('38 sold')
    38
    >>> parse_itemssold('14 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0
    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numbers)
    else:
        return 0
  
    '''
    How I wrote the code before Mike wrote it: 

    if 'sold' in text.lower():
        text = text.split()
        return int(text[0])
    else:
        return 0
    '''

def parse_dollaramount(text):
    '''
    Takes as input a string and returns the value in cents as an integer (removing the $ and the period) 
    >>> parse_dollaramount('$4.99')
    499
    >>> parse_dollaramount('$500.00')
    50000
    >>> parse_dollaramount('$0.79')
    79
    '''
    text = text.replace('$','')
    text = text.replace('.','')
    text = text.replace(',','')
    text = text.split()
    return (int(text[0]))

def parse_shipping(text):
    '''
    Takes as input a string and returns the value in cents of shipping. If free shipping return 0
    '''
    if 'free' in text.lower():
        return 0
    else:
        text = text.replace('$','')
        text = text.replace('.','')
        text = text.replace('+','')
        text = text.split()
        return int(text[0])
    
    


# This statement says only run the code below if 
# normaly running the code, where normmally means not doctests
if __name__  == '__main__':

    ## USING ARGPARSE TO GET COMMAND LINE ARGUMENTS ##
    parser = argparse.ArgumentParser(description='Download information from ebay and conert it to JSON')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default=10)
    parser.add_argument('--csv',default=False)
    args = parser.parse_args()

    # Replacing space with + #
    if ' ' in args.search_term:
        args.search_term = args.search_term.replace(' ', '+')
    

    #Need to double check the URL  

    ## BUILD THE URL ##

    # List of all items found in all ebay webpages #
    items = []

    # Loop over all ebay webpages #
    for page_number in range(1,int(args.num_pages)+1):
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + args.search_term + '&_sacat=0&_pgn=' + str(page_number)

        ## DOWNLOAD THE HTML USING REQUESTS ##
        #Double check that this is working #
        r = requests.get(url)
        status = r.status_code

        html = r.text
        

        ## PROCESS THE HTML USING BEAUTIFULSOUP ##
        
        soup = BeautifulSoup(html, 'html.parser')
        tags_items = soup.select('.s-item')
        # Loops over items in the page #
        for tag_item in tags_items:
            
            name = None
            tags_name = tag_item.select('.s-item__title')
            for tag in tags_name:
                name = tag.text

            freereturns = False
            tags_freereturns = tag_item.select('.s-item__free-returns,.s-item__freeReturnsNoFee')
            for tag in tags_freereturns:
                freereturns = True

            items_sold = None
            tags_itemssold = tag_item.select('.s-item__hotness,.s-item__additionalItemHotness,.s-item__itemHotness')
            for  tag in tags_itemssold:
                items_sold = parse_itemssold(tag.text)
            
            price = None
            tags_price = tag_item.select('.s-item__price')
            for tag in tags_price:
                price = parse_dollaramount(tag.text)
            
            item_status = None
            tags_status = tag_item.select('.s-item__subtitle')
            for tag in tags_status:
                item_status = tag.text
            
            shipping_status = None
            tags_shipping = tag_item.select('.s-item__shipping, .s-item__logisticsCost')
            for tag in tags_shipping:
                shipping_status = parse_shipping(tag.text)
            
            item = {
                'name': name,
                'free_returns': freereturns,
                'items_sold': items_sold,
                'price': price,
                'status': item_status,
                'shipping': shipping_status
            }

            if 'Shop on eBay' in item['name']:
                continue
            else:
                items.append(item)


    args.search_term = args.search_term.replace('+',' ')
    ## WRITING TO JSON FILE ##
    filename = args.search_term + '.json'
    with open(filename, 'w', encoding='ascii')  as f:
        f.write(json.dumps(items))

    ## WRITING TO CSV

    if args.csv: 
        keys = list(items[0].keys())
        filename_csv = args.search_term + '.csv'
        with open(filename_csv, 'w', encoding = 'utf-8', newline = '') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(items)





