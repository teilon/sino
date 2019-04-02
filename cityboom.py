import numpy as np
import pandas as pd


def get_report_by_city(data, data_2018):
    tmp(data, data_2018)
    return
    # city = 'Шымкент'
    # city = 'Астана'
    city = 'Алматы'
    # city = 'Актобе'

    rest = get_rest(data, city)
    prognoz = get_prognoz(data_2018, city)
    result = pd.concat([rest, prognoz], axis=1, sort=True)

    result.to_csv('report/result_{}'.format(city))


def tmp(data, data_2018):
    city = 'Алматы'
    # pr = get_prognoz(data_2018, city)
    pr = data_2018[data_2018['region'] == 'Алматы']

    # df.groupby(['Animal']).mean()
    col_real =

    pr = pr.groupby(['region', 'station', 'article', 'number'])
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


def get_rest(data, city):
    data = data[data['region'] == city]
    res = pd.pivot_table(data, values=['rest'],
                          columns=['region', 'station'],
                          index=['number', 'article'],
                          aggfunc=np.sum)

    res.to_csv('report/rest_{}'.format(city))
    return res


def get_prognoz(data, city):
    data = data[data['region'] == city]

    # MEN AROMAS
    mdata = data[data['type'] == 'm']
    mdata = pd.pivot_table(mdata, values=['real', 'rest'],
                           columns=['month'],
                           index=['region', 'station', 'number'],
                           aggfunc=np.sum)
    mdata['worked'] = mdata['real'].count(axis=1)
    mdata['arg'] = mdata['real'].sum(axis=1) / mdata['worked']
    mdata['prognoz'] = np.where(mdata['arg'] < 4, 3, 6)
    # mdata = mdata[mdata['region', 'station', 'number', 'prognoz']]

    # WOMEN AROMAS
    wdata = data[data['type'] == 'w']
    wdata = pd.pivot_table(wdata, values=['real', 'rest'],
                           columns=['month'],
                           index=['region', 'station', 'number'],
                           aggfunc=np.sum)
    wdata['worked'] = wdata['real'].count(axis=1)
    wdata['arg'] = wdata['real'].sum(axis=1) / wdata['worked']
    wdata['prognoz'] = np.where(wdata['arg'] < 2.1, 2, 4)
    # wdata = wdata[wdata['region', 'station', 'number', 'prognoz']]

    # CONCAT
    result = pd.concat([mdata, wdata], sort=True)
    result = result.sort_values(['region', 'station', 'number'], ascending=True)

    # RESULT
    result = pd.pivot_table(result, values=['prognoz'],
                        columns=['region', 'station'],
                        index=['number'],
                        aggfunc=np.sum)

    result.to_csv('report/prognoz_{}'.format(city))
    return result
