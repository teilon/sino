import numpy as np
import pandas as pd
import re

from source import get_data_by_report, get_df_by_file, get_aromaname, get_data_by_report_
from calcaroma import get_all
from cityboom import get_report_by_city


def use_best_stations():
    merge_docs()
    tmp()


def tmp():
    mar = get_data_by_report_('month/8mar.xlsx')
    aug = get_data_by_reporтt('month/1aug.xlsx')

    data_2018 = pd.concat([aug, mar
                           ], sort=True)

    mar.to_csv('report/tmp')


def merge_docs():
    feb_shym = get_data_by_report('month/7feb_shym.xlsx')
    mar = get_data_by_report('month/8mar.xlsx')
    feb = get_data_by_report('month/7feb.xlsx')
    jan = get_data_by_report('month/6jan.xlsx')
    dec = get_data_by_report('month/5dec.xlsx')
    nov = get_data_by_report('month/4nov.xlsx')
    oct = get_data_by_report('month/3oct.xlsx')
    sep = get_data_by_report('month/2sep.xlsx')
    aug = get_data_by_report('month/1aug.xlsx')
    data_2018 = pd.concat([aug, sep, oct, nov, dec], sort=True)
    data_mar = pd.concat([mar], sort=True)

    get_report_by_city(data_mar, data_2018)

    # good_stations = get_good_station(data)
    # bad_stations = get_bad_station(data)

    # good_list = get_station_list(good_stations)
    # bad_list = get_station_list(bad_stations)

    # get_product_by_good(data, good_list, 'good')
    # get_product_by_good(jan, good_list, 'good')
    # get_product_by_good(data, bad_list, 'bad')

    # get_all(data, data_2018)

    # get_by_number(jan, bad_list, 'bad')
    # get_full_report(data)
    # get_product_by_good(data_2018, {}, 'shym')


    print('done')


def get_full_report(data):
    # cities = ['Астана', 'Алматы', 'Усть-Каменогорск']
    # cities = ['Астана', 'Усть-Каменогорск',
    #           'Актобе', 'Атырау', 'Актау',
    #           'Кызылорда', 'Тараз', 'Шымкент']

    # data = data.set_index('region')

    # data = data.drop(cities)

    # print(data.head())

    data = data[data['region'] == 'Шымкент']
    df = pd.pivot_table(data, values=['rest'],
                        columns=['region', 'station'],
                        index=['number'],
                        aggfunc=np.sum)
    df.to_csv('report/shym')


def get_all_return():
    dec = get_data_by_report('month/5dec.xlsx')
    nov = get_data_by_report('month/4nov.xlsx')
    oct = get_data_by_report('month/3oct.xlsx')
    sep = get_data_by_report('month/2sep.xlsx')
    aug = get_data_by_report('month/1aug.xlsx')
    data = pd.concat([aug, sep, oct, nov, dec], sort=True)

    bad_stations = get_bad_station(data)
    bad_list = get_station_list(bad_stations)

    get_all_return_number(dec, bad_list)


def get_station_list(df):
    ind = df.index
    count = len(ind.labels[0])

    res = []
    for n in range(count):
        city_label = ind.labels[0][n]
        city = ind.levels[0][city_label]

        station_label = ind.labels[1][n]
        station = ind.levels[1][station_label]

        tmp = True
        for r in res:
            if r['city'] == city:
                if tmp:
                    item['station'].append(station)
                    tmp = False
                    break
        if tmp:
            item = {}
            item['city'] = city
            item['station'] = []
            item['station'].append(station)
            res.append(item)

    return res


def get_good_station(df):
    df = pd.pivot_table(df, values=['real'],
                          columns=['month'],
                          index=['region', 'station'],
                          aggfunc=np.sum)

    df['worked'] = df['real'].count(axis=1)
    df['arg'] = df['real'].sum(axis=1)/df['worked']
    df = df[df['arg'] > 14]
    df['sum'] = df['real'].sum(axis=1)

    return df


def get_bad_station(df):
    df = pd.pivot_table(df, values=['real'],
                          columns=['month'],
                          index=['region', 'station'],
                          aggfunc=np.sum)

    df['worked'] = df['real'].count(axis=1)
    df['arg'] = df['real'].sum(axis=1)/df['worked']
    df = df[df['arg'] < 20]
    df['sum'] = df['real'].sum(axis=1)

    return df


def get_product_by_good(data, stations, sep):
    mdata = data[data['type'] == 'm']
    get_product_by_good_h(mdata, stations, sep, 'm')

    wdata = data[data['type'] == 'w']
    get_product_by_good_h(wdata, stations, sep, 'w')


def get_product_by_good_h(data, stations, sep, gender):
    cities = ('Актау', 'Актобе', 'Атырау', 'Кызылорда', 'Тараз', 'Шымкент')
    # no_selected_cities = ('Астана', 'Алматы', 'Усть-Каменогорск')

    group = ['Шымкент']
    # for station in stations:
    #     if station['city'] not in no_selected_cities:
    #         group.append(station)

    # print(group)


    for item in group:

        idata = data[data['region'] == item['city']]
        idata = idata[idata['station'].isin(item['station'])]

        idata = pd.pivot_table(idata, values=['real', 'rest'],
                            columns=['month'],
                            index=['region', 'station', 'number'],
                            aggfunc=np.sum)
        idata['worked'] = idata['real'].count(axis=1)
        idata['arg'] = idata['real'].sum(axis=1) / idata['worked']
        if gender == 'm':
            idata['prognoz'] = np.where(idata['arg'] < 4, 3, 6)
        if gender == 'w':
            idata['prognoz'] = np.where(idata['arg'] < 2.1, 2, 4)

        # toadd = idata['prognoz'] - idata['rest']
        # tosub = idata['rest'] - idata['prognoz']
        # idata['add'] = np.where(toadd > 0, toadd, 0)
        # idata['sub'] = np.where(tosub > 0, tosub, 0)
        # idata['add'] = np.where(idata['rest'] < idata['prognoz'], idata['prognoz'] - idata['rest'], 0)
        # idata['sub'] = np.where(idata['rest'] > idata['prognoz'], idata['rest'] - idata['prognoz'], 0)

        # pd['irr'] = np.where(pd['cs'] * 0.63 > pd['irr'], 1.0, 0.0)

        idata.to_csv('report/{}_{}_{}'.format(item['city'], gender, sep))

    # print(data.head())
    return data


def get_by_number(data, stations, sep):
    # no_selected_cities = ('Астана', 'Алматы', 'Усть-Каменогорск')

    print(stations)

    # group = stations[~stations['city'].isin(no_selected_cities)]
    # group = []
    # for station in stations:
    #     if station['city'] not in no_selected_cities:
    #         group.append(station)

    for item in stations:
        idata = data[data['region'] == item['city']]
        idata = idata[idata['station'].isin(item['station'])]

        idata = pd.pivot_table(idata, values=['rest'],
                            columns=['station'],
                            index=['region', 'number'],
                            aggfunc=np.sum)

        idata.to_csv('report/sub_{}_{}'.format(item['city'], sep))


def get_all_return_number(data, stations):
    # no_selected_cities = ('Астана', 'Алматы', 'Усть-Каменогорск')

    print(stations)

    # group = stations[~stations['city'].isin(no_selected_cities)]
    # group = []
    # for station in stations:
    #     if station['city'] not in no_selected_cities:
    #         group.append(station)

    dfs = []
    for item in stations:
        idata = data[data['region'] == item['city']]
        idata = idata[idata['station'].isin(item['station'])]

        idata = pd.pivot_table(idata, values=['rest'],
                            columns=['region', 'station'],
                            index=['number'],
                            aggfunc=np.sum)

        dfs.append(idata)
        # idata.to_csv('report/sub_{}_{}'.format(item['city'], sep))

    rdata = pd.concat(dfs, axis=1)
    # rdata['sum'] = rdata.sum(rdata['rest'])
    rdata.to_csv('report/return')
    print('save')


# def get_by_counts(filename):
#     month = re.search('/\w+', filename).group(0)[1:]
#     print(month)
#
#     try:
#         select = pd.read_excel(filename)
#     except FileNotFoundError:
#         print('FileNotFoundError')
#
#     select['common'] = select['real'] + select['rest']
#     select['month'] = month
#     select['number'] = select['article'].apply(get_aromaname)
#     select['type'] = select['number'].apply(lambda x: x[0])
#
#     # new_select = select[select['number'] == 'man#10']
#
#     groupped = select.groupby(['region', 'station'])['real'].sum()
#     return groupped


# def get_by_month(filename):
#     month = re.search('/\w+', filename).group(0)[1:]
#     print(month)
#     try:
#         select = pd.read_excel(filename)
#     except FileNotFoundError:
#         print('FileNotFoundError')
#
#     select['common'] = select['real'] + select['rest']
#     select['month'] = month
#     select['number'] = select['article'].apply(get_aromaname)
#     select['type'] = select['number'].apply(lambda x: x[0])
#
#     table = pd.pivot_table(select, values=['real'],
#                            columns=['month'],
#                            index=['region'],
#                            aggfunc=np.sum
#                            )
#     return table
