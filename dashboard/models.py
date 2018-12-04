import os
from functools import lru_cache
import pandas as pd
from bokeh.models import ColumnDataSource
from dashboard.config import DISEASE_MIN_CASES, REGIONS
import sqlalchemy as sa

DATA_DIR = os.path.join(os.path.dirname(__file__), 'reports')
engine = sa.create_engine(os.environ['DATABASE_URL'])
conn = engine.connect()


def normalize_name(s):
    ret = s.lower()
    for ch in [' ', '-', '/']:
        ret = ret.replace(ch, '_')
    return ret


diseases_q = 'select * from diseases'
# disease_dict = (pd.read_csv(os.path.join(DATA_DIR, 'diseases2.csv'))
disease_dict = (pd.read_sql(diseases_q, conn)
                .assign(key=lambda x: x.disease.apply(normalize_name))
                .set_index('key')
                # .loc[:, 'id']
                .to_dict('index')
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

DISEASES = sorted([v['disease'] for k, v in disease_dict.items() if v['id'] in g.index.values])
DISEASES_HEB = sorted([v['disease_heb'] for k, v in disease_dict.items() if v['id'] in g.index.values])
DISEASE_DROPDOWN = sorted(
    [(v['disease_heb'], v['disease']) for k, v in disease_dict.items() if v['id'] in g.index.values])


def get_heb_name(disease):
    disease = normalize_name(disease)
    return disease_dict[disease]['disease_heb']


def get_disease_totals_by_name(name, smooth=2):
    name = normalize_name(name)
    id_ = disease_dict[name]['id']
    return get_disease_totals_by_id(id_, smooth)


def get_disease_totals_by_id(id_, smooth=2):
    df = _get_disease_totals(id_)
    ret = (df
           .sort_values(['date', 'disease_id'])
           .assign(date=lambda x: x.date + pd.DateOffset(days=6))
           .set_index('date')
           # .loc['2003':, :]
           .loc[lambda df: df.disease_id == id_, ['total']]
           .resample('W').mean()
           .assign(total_smooth=lambda x: x.total.rolling(smooth).mean())
           )

    cds = ColumnDataSource(data=ret)
    return cds


@lru_cache(maxsize=16)
def _get_disease_totals(id_):
    df = pd.read_sql(f'select date, disease_id, total from reports where disease_id={id_}', conn)
    return df


def get_disease_split_by_name(name, smooth=2):
    name = normalize_name(name)
    id_ = disease_dict[name]['id']
    return get_disease_split_by_id(id_, smooth)


def get_disease_split_by_id(id_, smooth=2):
    df = (_get_disease_split(id_)
          .sort_values(['date', 'disease_id'])
          .assign(date=lambda x: x.date + pd.DateOffset(days=6))
          .set_index('date')
          .loc['2008':, :]
          .loc[lambda df: df.disease_id == id_, :]
          .resample('W').mean()
          )
    roll = (df
            .drop(columns=['disease_id'])
           .rolling(smooth).mean()
           .rename(columns=lambda x: x + '_smooth')
           )
    ret = pd.concat((df,roll))

    # Concat rolling and non rolling
    cds = ColumnDataSource(data=ret)
    return cds


@lru_cache(maxsize=16)
def _get_disease_split(id_):
    cols = ','.join(REGIONS)
    df = pd.read_sql(f'select date, disease_id, total, {cols} from reports where disease_id={id_}', conn)
    return df


def get_disease_sums_by_name(name):
    name = normalize_name(name)
    id_ = disease_dict[name]['id']
    return get_disease_sums_by_id(id_)


def get_disease_sums_by_id(id_):
    df = (_get_disease_sums(id_)
          .rename(columns=lambda x: x.replace('_', ' ').capitalize()))

    cds = ColumnDataSource(data=df)
    return cds


@lru_cache(maxsize=16)
def _get_disease_sums(id_):
    cols = REGIONS + ['total']
    sum_cols = [f'sum ({col}) as {col}' for col in cols]
    q = f'''select year, {','.join(sum_cols)}
    from reports
    where disease_id={id_}
    group by year
    order by year;'''
    return pd.read_sql(q, conn)


def get_heb_info_by_name(name):
    name = normalize_name(name)
    id_ = disease_dict[name]['id']
    return get_heb_info_by_id(id_)


def get_heb_info_by_id(id_):
    df = _get_heb_info(id_)
    info = df.info_heb.values[0]
    wiki = df.wiki_heb.values[0]
    return info, wiki


@lru_cache(maxsize=16)
def _get_heb_info(id_):
    q = f'''select info_heb, wiki_heb from diseases where id = {id_}'''
    return pd.read_sql(q, conn)
