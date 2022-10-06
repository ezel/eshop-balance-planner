# coding: utf-8
from tracemalloc import start
from bs4 import BeautifulSoup
import pandas as pd


def parse_file(filename):
    with open(filename) as f:
        s1 = BeautifulSoup(f.read(), 'lxml')

    c_all = s1.find_all('div', class_='cell')

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
        if price_div:
            full_price = price_div.s.get_text()[1:].replace(',','')
            discount_price = price_div.find('strong').get_text()[1:].replace(',','')
        else:
            # no discount
            start_div = cell.find('a', class_='main-link')
            full_price = ""
            while len(full_price) < 1:
                if type(start_div).__name__ == 'NavigableString':
                    price_text = start_div.strip()
                    if price_text.startswith('$'):
                        full_price = price_text[1:]
                    if price_text.startswith('Free'):
                        full_price = "0"
                start_div = start_div.next
            discount_price = full_price

        # discount date
        end_str = cell.find('small').get_text() if cell.find('small') else ''
        df.loc[len(df.index)] = [name_str,
                                 float(full_price),
                                 float(discount_price),
                                 end_str]
    return df


def parse_file_by_spliter(filename, spliter='.', ignore=','):
    with open(filename) as f:
        s1 = BeautifulSoup(f.read(), 'lxml')

    c_all = s1.find_all('div', class_='cell')

    df = pd.DataFrame(columns=['name',
                               'full_price',
                               'discount_price',
                               'discount_end_str'])
    for cell in c_all:
        # name part
        name_div = cell.find('div', class_='name')
        name_str = name_div.get_text().strip()

        # price part
        replace_spliter = spliter
        ignore_spliter = ignore
        price_div = cell.find('div', class_='card-badge')
        if price_div:
            full_price_text = price_div.s.get_text()
            if full_price_text.startswith('$'):
                skip_char_count = 1
            elif full_price_text.startswith('R$'):
                skip_char_count = 2
            full_price = full_price_text[skip_char_count:].replace(ignore_spliter,'')
            full_price = full_price.replace(replace_spliter, '.')
            discount_price = price_div.find('strong').get_text()[skip_char_count:].replace(ignore_spliter,'')
            discount_price = discount_price.replace(replace_spliter, '.')
        else:
            # no discount
            start_div = cell.find('a', class_='main-link')
            full_price = ""
            while len(full_price) < 1:
                if type(start_div).__name__ == 'NavigableString':
                    price_text = start_div.strip()
                    if price_text.startswith('$'):
                        full_price = price_text[1:]
                    elif price_text.startswith('R$'):
                        full_price = price_text[2:]
                    if price_text.startswith('Free'):
                        full_price = "0"
                start_div = start_div.next
            discount_price = full_price

        # discount date
        end_str = cell.find('small').get_text() if cell.find('small') else ''
        df.loc[len(df.index)] = [name_str,
                                 float(full_price),
                                 float(discount_price),
                                 end_str]
    return df


if __name__ == "__main__":
    fn = input('please input the file name >')
    spliter = input("input spliter and ignore, default='. ,''>")
    if len(spliter) > 0:
        d1 = parse_file_by_spliter(fn, *spliter.split(' '))
    else:
        d1 = parse_file(fn)
    d1.to_csv('%s.csv' % fn)
