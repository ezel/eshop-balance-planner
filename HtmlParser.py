# coding: utf-8
from bs4 import BeautifulSoup
import pandas as pd


def parse_file(filename):
    with open(filename) as f:
        s1 = BeautifulSoup(f.read(), 'lxml')

    c_all = s1.find_all('div', class_='cell')
    #len(c_all)

    df = pd.DataFrame(columns=['name',
                               'full_price',
                               'discount_price',
                               'discount_end_str'])
    for cell in c_all:
        # name part
        name_div = cell.find('div', class_='name')
        name_str = name_div.get_text().strip()

        # price part
        price_div = cell.find('div', class_='card-badge')
        full_price = price_div.s.get_text()[1:].replace(',','')
        discount_price = price_div.find('strong').get_text()[1:].replace(',','')

        # discount date
        end_str = cell.find('small').get_text()
        df.loc[len(df.index)] = [name_str,
                                 float(full_price),
                                 float(discount_price),
                                 end_str]
    return df


if __name__ == "__main__":
    fn = input('please input the file name >')
    d1 = parse_file(fn)
    d1.to_csv('%s.csv' % fn)
