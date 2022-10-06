from planner import *

if __name__ == "__main__":
    print('testing...')
    acc = Account('AUD')
    acc.set_balance(15, 106)
    acc.buy(2.99)  # boomerang fu
    #acc.buy(1.50)  # shipped

    # todo
    #acc.buy(7.02) # a short hike
    #acc.buy(1.50) # little bug
    acc.buy(2.70) # tools up
    acc.buy(11.25) # tools up dlc
    acc.display()
    p1 = Planner('data.csv')
    plan_count = p1.get_price_plans(acc, 1)
    pd.DataFrame(p1.get_shopping_list('name')).to_csv('plan_%s.csv' % plan_count)
