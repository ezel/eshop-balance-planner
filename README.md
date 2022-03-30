# eshop-balance-planner
fina a solution to spend the balance in eshop

# Usage
## get the basic price data
can fetch it from https://www.dekudeals.com/
1. search for a result
2. show all on one page (e.g. 200 items), and save the result html file 
3. run the HtmlParser.py to get the data (.csv)
## run the planner
1. rename the data file to 'data.csv'
2. set your balance in planner.py
3. run the planner.py to get a plan list
4. pay great ATTENTION to the usage of coin, the coin paid is no change

# todo
- generate the purchase order
- speed up the backtrack
- support for vary currency (current in MXN)
