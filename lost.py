import numpy as np
import pandas as pd
from source import get_lost


def get_report():
    get_all()
    # get_single()


def get_all():
    cities = ['shymlost',
              'aktaulost',
              'atyraulost',
              'aktobelost',
              'tarazlost',
              'kizylordalost'
              ]

    for city in cities:
        print(city)
        data = get_lost('lost/{}.xlsx'.format(city))
        result = pd.pivot_table(data, values=['add', 'sub'],
                                columns=['station'],
                                index=['number'],
                                aggfunc=np.sum
                                )

        result.to_csv('report/{}'.format(city))
    print('done')


def get_single():
    city = 'aktaulost'
    # city = 'shymlost'
    data = get_lost('lost/{}.xlsx'.format(city))
    print(city)
    result = pd.pivot_table(data, values=['add', 'sub'],
                            columns=['station'],
                            index=['number'],
                            aggfunc=np.sum
                            )

    result.to_csv('report/{}'.format(city))
