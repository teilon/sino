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

    REAL_COL = '{}_real'.format(month[1:])
    REST_COL = '{}_rest'.format(month[1:])

    groupped = df[['region', 'station', 'article', 'number', 'type', 'real', 'rest']]
    groupped.columns = ['region', 'station', 'article', 'number', 'type', REAL_COL, REST_COL]

    return groupped.fillna(0)


def tmp():
    apr = get_data('month/9apr.xlsx')
    mar = get_data('month/8mar.xlsx')
    feb = get_data('month/7feb.xlsx')
    jan = get_data('month/6jan.xlsx')
    dec = get_data('month/5dec.xlsx')
    nov = get_data('month/4nov.xlsx')
    oct = get_data('month/3oct.xlsx')
    sep = get_data('month/2sep.xlsx')
    aug = get_data('month/1aug.xlsx')
    jul = get_data('month/0jul.xlsx')

    dfs = [aug, sep, oct, nov, dec, apr]
    dfss = [aug, sep, oct, nov, dec, jan, feb, mar, apr]

    d18 = reduce(
        lambda left, right: pd.merge(left,
                                     right,
                                     how='outer',
                                     on=['region', 'station', 'article', 'number', 'type']),
        dfss)
    d18['apr_rest'].fillna(0, inplace=True)

    reals = ['aug_real', 'sep_real', 'oct_real', 'nov_real', 'dec_real', 'jan_real', 'feb_real', 'apr_real']
    rests = ['aug_rest', 'sep_rest', 'oct_rest', 'nov_rest', 'dec_rest', 'jan_rest', 'feb_rest', 'apr_rest']
    view18 = ['aug_real', 'sep_real', 'oct_real',
              'nov_real', 'dec_real', 'apr_real']

    view1819 = ['aug_real', 'sep_real', 'oct_real',
                'nov_real', 'dec_real', 'jan_real',
                'feb_real', 'mar_real', 'apr_real']

    apr_view = ['region', 'station', 'number', 'arg', 'apr_real', 'apr_rest', 'needfull']
    # arg0 = ['region', 'station', 'number',
    #        'aug_real', 'aug_rest', 'sep_real', 'sep_rest', 'oct_real', 'oct_rest',
    #        'nov_real', 'nov_rest', 'dec_real', 'dec_rest', 'jan_real', 'jan_rest',
    #        'feb_real', 'feb_rest', 'mar_real', 'mar_rest', 'apr_real', 'apr_rest',
    #        'arg'
    #         ]

    mar_view = ['region', 'station', 'article', 'number', 'mar_real', 'mar_rest', 'needfull']
    nov_view = ['region', 'station', 'article', 'number', 'nov_real', 'nov_rest', 'needfull']

    #
    d18['worked'] = d18[view18].count(axis=1)
    d18['total'] = d18[view18].sum(axis=1)
    d18['arg'] = d18['total']/d18['worked']

    d18['prognoz'] = d18.apply(lambda row: get_prognoz(row), axis=1)
    d18['needfull'] = d18.apply(lambda row: get_needfull(row), axis=1)

    # res = d18[d18['region'] == 'Актобе']
    # res = d18[apr_view]

    arg = ['region', 'station',  # 'number',
           'aug_real', 'sep_real', 'oct_real',
           'nov_real', 'dec_real', 'jan_real',
           'feb_real', 'mar_real', 'apr_real',
           'worked', 'total']

    # d18 = d18[d18['region'] == 'Шымкент']
    d18 = d18[arg]
    d18 = d18.groupby(['region', 'station']).sum()
    # d18.to_csv('report/tmp_group')

    # print(res.head())
    # res.to_csv('report/tmp_akt')
    # d18[arg0].to_csv('report/tmp')
    # d18[arg].to_csv('report/tmp_arg')
    d18.to_csv('report/tmp_arg')


def get_report(data):
    # apr_view = ['region', 'station', 'article', 'number', 'apr_real', 'apr_rest', 'needfull']

    data = pd.pivot_table(data, values=['arg'],
                           # columns=['month'],
                           index=['region', 'station'],
                           aggfunc=np.sum)
    data.to_csv('report/tmp_11')


def get_needfull(row):
    return row['prognoz'] - row['apr_rest'] if row['prognoz'] > row['apr_rest'] else 0


def get_prognoz(row):
    if row['type'] == 'm':
        if (row['arg'] > 2.9) and (row['arg'] < 6):
            return 6
        if row['arg'] > 5.9:
            return 9
        return 3
    if (row['arg'] > 1.9) and (row['arg'] < 4):
        return 4
    if row['arg'] > 3.9:
        return 6
    return 2
