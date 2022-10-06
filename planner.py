from unicodedata import name
import HtmlParser
import pandas as pd
from numpy import ceil
import logging

COIN_TO_CURRENCY = {
    'MXN' : 0.2,
    'BRL' : 0.05,
    'AUD' : 0.01
}

logging.basicConfig(format='%(asctime)s: %(message)s',
                    level=logging.DEBUG
                    #,filename='plan.log'
                    )

class Account:
    def __init__(self, currency='MXN'):
        assert(currency in COIN_TO_CURRENCY)
        # private members
        self.__rate = COIN_TO_CURRENCY[currency]
        self.__balance = {'money': 0,
                          'coins': 0}
        self.__cart = []
        self.__name = "nameless"

    def set_name(self, new_name):
        self.__name = new_name

    def set_balance(self, money=0, coins=0):
        self.__balance['money'] = money
        self.__balance['coins'] = coins

    def add_balance(self, money=0, coins=0):
        self.__balance['money'] = round(money+self.__balance['money'],2)
        self.__balance['coins'] += coins

    def max(self):
        return round(self.__balance['money'] + self.__balance['coins'] * self.__rate, 2)

    def can_smuggle(self):
        if self.__balance['money'] == 0:
            return True
        elif (self.__balance['money'] < 0):
            if (self.max() >= 0) and ((self.max() *100) % (self.__rate *100)== 0):
                return True
        return False

    def buy(self, price, coins=-1):
        #print('buying...%s' % price)
        if (coins < 0):
            coins = self.get_coins_by_price(price)
        self.add_balance(-price, coins)
        self.__cart.append({"price": price, "coins": coins})

    def refund(self, price, coins=-1):
        #print('refund...%s' % price)
        if (coins < 0):
            coins = self.get_coins_by_price(price)
        self.add_balance(price, -coins)
        self.__cart.remove({"price": price, "coins": coins})

    def display(self):
        print("The balance of %s:" % self.__name)
        print(self.__balance)
        print("The cart of %s:" % self.__name)
        print(self.__cart)
        print(self.max())
        print(self.can_smuggle())

    def get_coins_by_price(self, price):
        coins = ceil(price*0.05/self.__rate)
        return int(coins)


class Planner:
    def __init__(self, data_path='data.csv', price_column='discount_price'):
        self.df = pd.read_csv(data_path)
        self.df = self.df[self.df[price_column] > 0]
        self.price_column = price_column
        self.plans = []
        self.shopping_list = []
        self.sort_prices = sorted(self.df[price_column].unique())
        self.sort_items = self.df[price_column].value_counts().sort_index().to_dict()
        self.sort_items_keys = list(self.sort_items.keys())

    def get_shopping_list(self, name_column='name'):
        self.name_column = name_column
        for plan in self.plans:
            current_list = [round(sum(plan), 2)]
            for price in plan:
                price_to_names = self.df[self.df[self.price_column] == price][name_column].to_list()
                if len(price_to_names) == 1:
                    current_list.append(price_to_names[0])
                else:
                    current_list.append("|".join(price_to_names))
            self.shopping_list.append(current_list)
        return self.shopping_list

    def get_price_plans(self, account, method=1):
        #logging.info("planning for shopping list[%d]" % len(self.sort_prices))
        if (method == 0):
            self.backtrack_price_list(account, 0, [])
        elif (method ==1):
            self.backtrack_item_count_dict(account, 0, [])
        logging.info("found %d plans." % len(self.plans))
        return len(self.plans)

    def backtrack_item_count_dict(self, acc, price_start_idx, current_plan=[]):
        #logging.debug("current-plan=%s" % current_plan)
        if acc.can_smuggle():
            self.plans.append(current_plan.copy())
            return
        else:
            # search in the accept items
            for i in range(price_start_idx, len(self.sort_items_keys)):
                # try add
                price = self.sort_items_keys[i]
                item_left = self.sort_items[price]
                if (item_left > 0):
                    # check price
                    if (price <= acc.max()):
                        acc.buy(price)
                        self.sort_items[price] -= 1
                        current_plan.append(price)
                        self.backtrack_item_count_dict(acc, i, current_plan)
                        acc.refund(price)
                        self.sort_items[price] += 1
                        current_plan.remove(price)
                    else:
                        return


    def backtrack_price_list(self, acc, price_start_idx, current_plan=[]):
        #print("current-plan=%s" % current_plan)
        if acc.can_smuggle():
            self.plans.append(current_plan.copy())
            return
        else:
            # search in the accept items
            for i in range(price_start_idx, len(self.sort_prices)):
                # try add
                price = self.sort_prices[i]
                if (price <= acc.max()):
                    acc.buy(price)
                    current_plan.append(price)
                    self.backtrack_price_list(acc, i, current_plan)
                    acc.refund(price)
                    current_plan.remove(price)
                else:
                    # cut the other 
                    return


    def result_plans(self):
        print(self.plans)

