import pandas as pd
import re


def get_data_by_report(filename):
    df = get_df_by_file(filename)

    month = re.search('/\w+', filename).group(0)[1:]
    df['month'] = month
    df['number'] = df['article'].apply(get_aromaname)
    df['type'] = df['number'].apply(lambda x: x[0])

    # groupped = df.groupby(['region', 'station'])['real'].sum()
    groupped = df[['month', 'region', 'station', 'article', 'number', 'type', 'real', 'rest']]

    return groupped


def get_data_by_report_(filename):
    df = get_df_by_file(filename)

    month = re.search('/\w+', filename).group(0)[1:]
    df['month'] = month
    df['number'] = df['article'].apply(get_aromaname)
    df['type'] = df['number'].apply(lambda x: x[0])

    # groupped = df.groupby(['region', 'station'])['real'].sum()

    REAL_COL = '{}_real'.format(month[1:])
    REST_COL = '{}_rest'.format(month[1:])
    # df.rename(columns={'real': REAL_COL})
    # df.rename(columns={'rest': REST_COL})

    groupped = df[['month', 'region', 'station', 'article', 'number', 'type', 'real', 'rest']]
    # groupped.columns = ['month', 'region', 'station', 'article', 'number', 'type', REAL_COL, REST_COL]

    return groupped


def get_rpdata_by_report(filename):
    df = get_df_by_file(filename)

    df['number'] = df['article'].apply(get_aromaname)
    df['type'] = df['number'].apply(lambda x: x[0])

    # groupped = df.groupby(['region', 'station'])['real'].sum()
    groupped = df[['station', 'date', 'number', 'type', 'add']]

    return groupped


def get_aromapdata_by_report(filename):
    df = get_df_by_file(filename)

    df['type'] = df['number'].apply(lambda x: x[0])

    # groupped = df.groupby(['region', 'station'])['real'].sum()
    groupped = df[['region', 'station', 'kind', 'number', 'type', 'delivery', 'return']]

    return groupped


def get_lost(filename):
    df = get_df_by_file(filename)
    groupped = df[['region',
                   'station',
                   'number',
                   'rest',
                   'arg',
                   'max',
                   'add',
                   'sub']]
    return groupped


def get_aromaname(article):
    names = {
        '330092830': 'man#01',
        '330092831': 'man#02',
        '330092832': 'man#03',
        '330092833': 'man#04',
        '330092834': 'man#05',
        '330092835': 'man#06',
        '330092836': 'man#07',
        '330092837': 'man#08',
        '330092838': 'man#09',
        '330092839': 'man#10',
        '330092840': 'woman#01',
        '330092841': 'woman#02',
        '330092842': 'woman#03',
        '330092843': 'woman#04',
        '330092844': 'woman#05',
        '330092845': 'woman#06',
        '330092846': 'woman#07',
        '330092847': 'woman#08',
        '330092848': 'woman#09',
        '330092849': 'woman#10'
    }
    return names[str(article)]


def get_df_by_file(filename):
    try:
        return pd.read_excel(filename)
    except FileNotFoundError:
        print('FileNotFoundError')
