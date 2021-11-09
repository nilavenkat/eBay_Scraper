import json
import requests
from bs4 import BeautifulSoup
import urllib.parse
import ssl
import csv

def soup_of_page (url):
    #fetch page
    page = requests.get(url, verify= False)
    if not page.ok:
        print('server responded:', page.status_code)
    else:
        soup = BeautifulSoup(page.text, 'html.parser')
    return(soup)

def get_next_page(url):
    soup = soup_of_page(url)
    next_page = soup.find('a', attrs={'class':'pagination__next icon-link'})
    if(next_page == None or next_page.has_attr('aria-disabled')):
        print("can't find next page for:", url)
        next_page_link =  None
    else:
        next_page_link = next_page['href']
    return next_page_link

def scrape_ebay_items (search_term, in_csv_format, num_pages):
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        #Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        #Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context
        
    json_items = []
    dict_items = []

    #build ebay url
    ebay_url = "https://www.ebay.com/sch/i.html?&_sacat=0&_ipg=20&_nkw=" + urllib.parse.quote(search_term)
    page_num = 1
    while (ebay_url != None):
        print("items so far:{0}-page number#{1}:{2}".format(len(json_items),page_num,ebay_url))
        ebay_soup = soup_of_page(ebay_url)
        listings = ebay_soup.select("li.s-item")
        for listing in listings:
            prod_name= None
            prod_price = None
            prod_status = None
            prod_shipping_cost = None
            prod_free_returns = None
            prod_items_sold = None

            #get title
            title_block = listing.find('h3',attrs={'class':'s-item__title'})
            prod_name = str(title_block.find(text=True,recursive=True))
            if prod_name == "None":
                continue

            #get price
            price_block = listing.find('span',attrs={'class':'s-item__price'})
            price = str(price_block.find(text=True,recursive=False))
            if price != "None":
                price = price.split(" ")[0]
                price = price.split("<")[0]
                price = price.replace('$','').replace(',','').strip()
                try: 
                    prod_price = int(float(price)*100)
                except:
                    pass

            #get status
            status_block = listing.find('span', attrs={'class':'SECONDARY_INFO'})
            if status_block != None: 
                status = str(status_block.find(text=True, recursive=False))
                if status != "None" :
                    prod_status = status

            # Get shipping
            shipping_block = listing.find('span', attrs={'class':'s-item__shipping s-item__logisticsCost'})
            shipping_block2 = listing.find('span', attrs={'class':'s-item__dynamic s-item__freeXDays'})
            if shipping_block2 != None:
                prod_shipping_cost = 0
            elif shipping_block != None:             
                shipping = str(shipping_block.find(text=True, recursive=False))
                if shipping != "None":
                    if shipping == "Free shipping":
                        prod_shipping_cost = 0
                    else:
                        shipping = shipping.split(" ")[0]
                        shipping = shipping.replace('$','').replace(',', '').replace('+', '').strip()
                        try:
                            prod_shipping_cost = int(float(shipping) * 100)
                        except:
                            pass
            
            #Get Free Return
            free_return_block = listing.find('span', attrs={'class':'s-item__free-returns s-item__freeReturnsNoFee'})
            if free_return_block == None:
                prod_free_returns = False
            else:
                prod_free_returns = True

            #Get items sold
            items_sold_block = listing.find('span', attrs={'class':'s-item__hotness s-item__itemHotness'})
            if items_sold_block != None:
                items_sold = str(items_sold_block.find(text=True, recursive=True))
                if items_sold != "None":
                    items_sold = items_sold.split(" ")[0]
                    items_sold = items_sold.replace(',', '').replace('+', '').strip()
                    try:
                        prod_items_sold = int(items_sold)
                    except:
                        pass

            #creat dictionary object
            item = {}
            item['name']= prod_name
            item['price'] = prod_price
            item['status'] = prod_status
            item['shipping'] = prod_shipping_cost
            item['free_returns'] = prod_free_returns
            item ['items_sold'] = prod_items_sold
            dict_items.append(item)
            json_item = json.dumps(item)
            json_items.append(json_item)

        page_num += 1
        #if limited is provided to number of pages to scrape- use it
        if num_pages > 0: 
            if page_num > num_pages:
                break
        ebay_url = get_next_page(ebay_url)
    
    if (in_csv_format==True):
        csv_file_name = search_term + ".csv"
        header_row = ["name","price","status","shipping","free_returns","items_sold"]
        with open(csv_file_name,'w',encoding='utf-8',newline='') as cf:
            csv_writer=csv.DictWriter(cf,header_row,delimiter=',')
            csv_writer.writeheader()
            csv_writer.writerows(dict_items)
    else:
        json_filename = search_term + ".json"
        #json_filename = "GalaxyNote.json"
        with open(json_filename,"w") as jf:
            json.dump(json_items, jf, indent=6)

if __name__ == '__main__':
    # process command line arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--search_term', required=True, help="Search term is required")
    parser.add_argument('--csv', action='store_true', help="Save output in csv format")
    parser.add_argument('--page_limit',type=int, help="Limit the number of pages to scrape")
    args = parser.parse_args()
    if args.page_limit:
        num_pages = args.page_limit
    else:
        num_pages = -1
    # call the main function
    scrape_ebay_items(args.search_term,args.csv,num_pages)
    # scrape_ebay_items("Galaxy Note", True, 4)
