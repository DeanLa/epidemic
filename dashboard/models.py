import os
from functools import lru_cache
import pandas as pd
from bokeh.models import ColumnDataSource
from dashboard.config import DISEASE_MIN_CASES
import sqlalchemy as sa

DATA_DIR = os.path.join(os.path.dirname(__file__), 'reports')
engine = sa.create_engine(os.environ['DATABASE_URL'])
conn = engine.connect()

disease_dict = (pd.read_csv(os.path.join(DATA_DIR, 'diseases.csv'))
                .set_index('disease')
                .loc[:, 'id']
                .to_dict()
                )

group_by_q = f'''
select disease_id, sum(total) total
from reports
group by disease_id
having sum(total)>{DISEASE_MIN_CASES}'''

g = (pd.read_sql(group_by_q, conn)
     .set_index('disease_id')
     .total
     )

DISEASES = sorted([k for k, v in disease_dict.items() if v in g.index.values])


def get_disease_data_by_name(name, smooth=2):
    id_ = disease_dict[name]
    return get_disease_data_by_id(id_, smooth)

def get_disease_data_by_id(id_, smooth=2):
    df = _get_disease_data(id_)
    ret = (df
           .sort_values(['date', 'disease_id'])
           .set_index('date')
           .loc['2008':, :]
           .loc[lambda df: df.disease_id == id_, ['total']]
           .resample('W').mean()
           .rolling(smooth).mean())

    cdr = ColumnDataSource(data=ret)
    return cdr


@lru_cache(maxsize=16)
def _get_disease_data(id_):
    df = pd.read_sql(f'select date, disease_id, total from reports where disease_id={id_}', conn)
    return df
