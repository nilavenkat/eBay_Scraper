# eBay Product Scraper

This program takes the search term from the user and scrapes the eBay website for:

* the items
* their prices
* product status
* shipping costs
* free returns
* and how many items sold

Program saves items in json format in a file named \<search term>.json
The user has an option to save this file in a csv format.
The program also does pagination, and takes a variable from the user to limit the number of pagination.

Here are the arguments the program takes:
--search\_term : the search term you want to use
--csv : flag if you want the output to be saved in a csv format
--page\_limit : number of pages to limit in pagination

I executed the program for: Galaxy Note, Bicycle, and Skateboard, and saved them as both json and csv.
This is the code that I used:
<br>
```
python3 ebay-dl.py --search_term="Bicycle" --page_limit=10

python3 ebay-dl.py --search_term="Bicycle" --page_limit=10 --csv

python3 ebay-dl.py --search_term="Galaxy Note" --page_limit=10

python3 ebay-dl.py --search_term="Galaxy Note" --page_limit=10 --csv

python3 ebay-dl.py --search_term="Skateboard" --page_limit=10

python3 ebay-dl.py --search_term="Skateboard" --page_limit=10 --csv
```

The description for this homework is [here](https://github.com/mikeizbicki/cmc-csci040/tree/2021fall/hw_03)