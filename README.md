# Project_03

## Script Overview
This python script has the ability to scrape ebay and return the data for 6 given paramaters (`name`, `price`, `status`, `free_returns`, `shipping status`, and `items sold`) in JSON and CSV format. This script automates data collection from the web and returns the data is an usable format. This script utilizes **argparse** to get information from the command line (`search_term`, `--num_pages`, and `--csv`), **requests** to download the HTML code, and **BeautifulSoup** to process the HTML. More furhter details can be found on the [project webpage](https://github.com/mikeizbicki/cmc-csci040/tree/2022fall/project_03).


## How to Use the Command Line to Generate JSON
Utilizing the command line is made easy by argparse. All you must do is enter the desired search term at the end of after the 'ebay-dl.py' file path. Enter the line as follows (_Note: some things may look different on your computer_)
```
$ python3 ebay-dl.py search_term 
```
For example, here is how I generated my cat JSON files:
```
$ python3 ebay-dl.py cat
```
If entering a search term that has a space, make sure to include quotations around the term otherwise the program won't know how to interpret what you are trying to search for. Example:
```
$ python3 ebay-dl.py 'artic fox'
```

## How to use the Command Line to Change Number of Pages Scraped
By default, this script will scrape the data from the first 10 pages on Ebay. If you desire to change this, you can add the optional argument `--num_pages` to the command line. Here is an example if you only wanted to scrape the data from the first 5 pages. 
```
$ python3 ebay-dl.py cat --num_pages=5
```

## How to Use the Command Line to Generate CSV
The final action in the command line is to use the optional `--csv` argument to convert your file to CSV format. This is important because you may want to do some action with your data that requires a csv file (or maybe working with a CSV file would make your life a  heck of a lot easier). The default code will not generate a CSV file, so in order to create one, you must set `--csv=True`. Here is an example of how to run the command line to generate a CSV file:
```
$ python3 ebay-dl.py cat  --csv=True
```

