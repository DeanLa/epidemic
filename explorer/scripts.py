from flask import Flask
import pandas as pd
import click
import os
import json
from .models import db, Disease, Report
import sqlalchemy as sa

sql = sa.dialects.postgresql
curdir = os.path.dirname(__file__)


def init_app(app: Flask):
    @app.cli.command(help='Populate db for the first time if empty')
    def populate_db():
        _check_db_empty()
        put_diseases_in_db()
        put_reports_in_db()

    @app.cli.command(help='Populate db safely')
    def new_reports():
        put_reports_in_db()


diseases = json.load(open(os.path.join(curdir, 'diseases.json'), 'r'))


def put_diseases_in_db():
    dids = pd.DataFrame(list(diseases.items()), columns=['disease', 'id'])
    _insert_df(dids, Disease)
    click.echo('Disease IDs written')


def put_reports_in_db():
    path = os.environ['DATA_FILE']
    df = _load_reports_df(path)
    try:
        _insert_df(df, Report)
    except Exception as e:
        print (e)
    click.echo('All disease are in DB')
    click.echo('Fixing HIV reports')
    hotfix_aids()
    click.echo('HIV fixed')
    db.session.commit()


def _check_db_empty():
    assert Report.query.count() == 0, 'reports table not empty'
    assert Disease.query.count() == 0, 'diseases table not empty'


def _load_reports_df(path: str) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_pickle(path)
    df = (df
          .rename(columns=str.lower)
          .assign(disease_id=lambda x: x.disease.map(diseases))
          .assign(id=lambda x: x.disease_id.astype(str) + '_' + x.year.astype(str) + '_' + x.week.astype(str))
          .reset_index()
          .drop(columns=['disease'])
          )
    return df


def _insert_df(df, Orm: db.Model):
    # sql = db.engine.connect()
    records = df.to_dict(orient='records')
    click.echo(f'{len(records)} new records')
    insert_q = sql.insert(Orm).values(records)
    update_dict = {c.name: c for c in insert_q.excluded if not c.primary_key}
    upsert_q = (insert_q
                .on_conflict_do_update(index_elements=['id'],
                                       set_=update_dict)
                )
    db.session.execute(upsert_q)


def hotfix_aids():
    """HIV has only sum total data, this requires a personal fix. Disease id is 105"""
    pd.options.mode.chained_assignment = None
    q = 'select * from reports where disease_id=105 order by date'
    df = pd.read_sql(q, db.engine)
    df['total'] = (df
                   .groupby('year')
                   .sumtotal.diff()
                   .fillna(df.sumtotal)
                   .clip_lower(0))
    df.loc[:, 'total'].iloc[0] = 26

    records = df.to_dict(orient='records')
    insert_q = sql.insert(Report).values(records)
    update_dict = {c.name: c for c in insert_q.excluded if not c.primary_key}
    upsert_q = (insert_q
                .on_conflict_do_update(index_elements=['id'],
                                       set_=update_dict)
                )
    db.session.execute(upsert_q)
