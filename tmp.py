import numpy as np
import pandas as pd
from functools import reduce
import re

from source import get_df_by_file
from source import get_aromaname


def get_data(filename):
    df = get_df_by_file(filename)

    month = re.search('/\w+', filename).group(0)[1:]
    df['month'] = month
    df['number'] = df['article'].apply(get_aromaname)
    df['type'] = df['number'].apply(lambda x: x[0])
    df['itype'] = df['number'].apply(lambda x: 1 if x[0] == 'm' else 0)

    REAL_COL = '{}_real'.format(month[1:])
    REST_COL = '{}_rest'.format(month[1:])

    groupped = df[['region', 'station', 'article', 'number', 'type', 'itype', 'real', 'rest']]
    groupped.columns = ['region', 'station', 'article', 'number', 'type', 'itype', REAL_COL, REST_COL]

    return groupped.fillna(0)


def tmp():
    mar = get_data('month/8mar.xlsx')
    feb = get_data('month/7feb.xlsx')
    jan = get_data('month/6jan.xlsx')
    dec = get_data('month/5dec.xlsx')
    nov = get_data('month/4nov.xlsx')
    oct = get_data('month/3oct.xlsx')
    sep = get_data('month/2sep.xlsx')
    aug = get_data('month/1aug.xlsx')

    dfs = [aug, sep, oct, nov, dec, mar]
    dfss = [aug, sep, oct, nov, dec, jan, feb, mar]

    d18 = reduce(
        lambda left, right: pd.merge(left,
                                     right,
                                     how='outer',
                                     on=['region', 'station', 'article', 'number', 'type']),
        dfss)

    reals = ['aug_real', 'sep_real', 'oct_real', 'nov_real', 'dec_real', 'jan_real', 'feb_real', 'mar_real']
    rests = ['aug_rest', 'sep_rest', 'oct_rest', 'nov_rest', 'dec_rest', 'jan_rest', 'feb_rest', 'mar_rest']
    view18 = ['aug_real', 'sep_real', 'oct_real', 'nov_real', 'dec_real']
    mar_view = ['mar_rest', 'arg']

    d18['worked'] = d18[view18].count(axis=1)
    d18['arg'] = d18[view18].sum(axis=1)/d18['worked']

    # d18 = d18.groupby(['region', 'station', 'article'])['mar_rest', 'arg'].sum()
    # d18 = d18.groupby(['region', 'station', 'article']).sum()

    # d18_mar['prognoz'] = get_prognoz(d18_mar['mar_rest'], d18_mar['arg'])

    print(d18.head())
    try:
        d18 = d18[d18['itype_x'] > 0]
        print(d18.head())
    except Exception as ex:
        print(str(ex))

    # d18_mar_w['prognoz'] = 0 if d18['mar_rest'] > d18['arg'] else 1
    #
    # d18_mar_m = d18[d18['itype_x'] == 1]
    # d18_mar_m['prognoz'] = 0 if d18['mar_rest'] > d18['arg'] else 1
    #
    # d18 = pd.concat([d18_mar_w, d18_mar_m], sort=True)

    # d18_mar = d18[mar_view]
    # print(d18_mar.head())

    # d18[d18['region'] == 'Шымкент'].to_csv('report/tmp')
    # d18_mar.to_csv('report/tmp')


def get_prognoz(rest, arg):
    print(rest)
    if rest > arg:
        return 0
    if rest < 3:
        return 3
    if rest > 6:
        return 9
    return 6

def get_group(data, data_2018):
    city = 'Алматы'
    # pr = get_prognoz(data_2018, city)
    pr = data_2018[data_2018['region'] == 'Алматы']

    # df.groupby(['Animal']).mean()
    # col_real =

    pr.groupby(['region', 'station', 'article', 'number'])
    pr.to_csv('report/tmp_{}'.format(city))

    # month = re.search('/\w+', filename).group(0)[1:]
    # df['month'] = month
    # df['number'] = df['article'].apply(get_aromaname)
    # df['type'] = df['number'].apply(lambda x: x[0])
    #
    # groupped = df[[
    #     'month', 'region',
    #     'station', 'article',
    #     'number', 'type',
    #     'real', 'rest']]