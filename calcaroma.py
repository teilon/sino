import numpy as np
import pandas as pd

from source import get_aromapdata_by_report


def get_data_by_aromas_move():
    data = get_aromapdata_by_report('month/aroma_report.xlsx')

    result = get_data_frame(data)
    result.to_csv('report/aroma_report')


def get_data_frame(data):
    # df[['region', 'station', 'kind', 'number', 'type', 'delivery', 'return']]
    df = pd.pivot_table(data, values=['delivery', 'return'],
                        columns=['number'],
                        index=['region'],
                        aggfunc=np.sum)

    # df['sum'] = df['real'].sum(axis=1)

    return df


def get_all(data, data_2018):
    print('mw')
    m = get_all_m(data)
    w = get_all_w(data)
    mw = pd.concat([m, w])
    mw.sort_index(axis=0, inplace=True)
    mw.to_csv('report/mw')

    print('a')
    m = get_all_m(data_2018)
    w = get_all_w(data_2018)
    a = pd.concat([m, w])
    a.sort_index(axis=0, inplace=True)
    a.to_csv('report/a')


def get_all0(data):
    # mdata = data[data['region'] == 'Алматы']
    mdata = data
    df = pd.pivot_table(mdata, values=['real', 'rest'],
                        columns=['month'],
                        index=['region', 'station', 'number'],
                        # index=['number'],
                        aggfunc=np.sum)
    df['worked'] = df['real'].count(axis=1)
    df['arg'] = df['real'].sum(axis=1) / df['worked']

    # print('aa')
    # df.to_csv('report/all')
    return df


def get_all_m(data):
    mdata = data[data['type'] == 'm']
    mdata = mdata[mdata['region'] == 'Актобе']

    df = pd.pivot_table(mdata, values=['real', 'rest'],
                        columns=['month'],
                        index=['region', 'station', 'number'],
                        aggfunc=np.sum)
    df['worked'] = df['real'].count(axis=1)
    df['arg'] = df['real'].sum(axis=1) / df['worked']

    df['prognoz'] = np.where(df['arg'] < 9.1, 9, 12)
    df['prognoz'] = np.where(df['arg'] < 6.1, 6, 9)
    df['prognoz'] = np.where(df['arg'] < 3.1, 3, 6)

    # df.to_csv('report/all_m')
    return df


def get_all_w(data):
    wdata = data[data['type'] == 'w']
    wdata = wdata[wdata['region'] == 'Актобе']
    df = pd.pivot_table(wdata, values=['real', 'rest'],
                        columns=['month'],
                        index=['region', 'station', 'number'],
                        aggfunc=np.sum)
    df['worked'] = df['real'].count(axis=1)
    df['arg'] = df['real'].sum(axis=1) / df['worked']

    df['prognoz'] = np.where(df['arg'] < 4.1, 4, 6)
    df['prognoz'] = np.where(df['arg'] < 2.1, 2, 4)

    # df.to_csv('report/all_w')
    return df
