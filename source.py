import pandas as pd
import re


def get_data_by_report(filename):
    df = get_df_by_file(filename)

    month = re.search('/\w+', filename).group(0)[1:]
    df['month'] = month
    df['number'] = df['article'].apply(get_aromaname)
    df['type'] = df['number'].apply(lambda x: x[0])

    # groupped = df.groupby(['region', 'station'])['real'].sum()
    groupped = df[['month', 'region', 'station', 'number', 'type', 'real', 'rest']]

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
        '330092830': 'man#1',
        '330092831': 'man#2',
        '330092832': 'man#3',
        '330092833': 'man#4',
        '330092834': 'man#5',
        '330092835': 'man#6',
        '330092836': 'man#7',
        '330092837': 'man#8',
        '330092838': 'man#9',
        '330092839': 'man#10',
        '330092840': 'woman#1',
        '330092841': 'woman#2',
        '330092842': 'woman#3',
        '330092843': 'woman#4',
        '330092844': 'woman#5',
        '330092845': 'woman#6',
        '330092846': 'woman#7',
        '330092847': 'woman#8',
        '330092848': 'woman#9',
        '330092849': 'woman#10'
    }
    return names[str(article)]


def get_df_by_file(filename):
    try:
        return pd.read_excel(filename)
    except FileNotFoundError:
        print('FileNotFoundError')
