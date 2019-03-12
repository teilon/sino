import numpy as np
import pandas as pd
import re

from source import get_rpdata_by_report


def use_rp_aroma():
    get_rp_aroma()


def get_rp_aroma():
    data = get_rpdata_by_report('month/jan_rp.xlsx')

    get_report(data)
    print('done')


def get_report(data):
    # 'station', 'date', 'number', 'type', 'add'
    df = pd.pivot_table(data, values=['add'],
                        columns=['number'],
                        index=['station'],
                        aggfunc=np.sum)

    df.to_csv('report/rp_rest')
