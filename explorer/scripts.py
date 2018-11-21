from flask import Flask
import pandas as pd
import click
import os
import json
from .models import db, Disease, Report
import sqlalchemy as sa

# sql = sa.dialects.postgresql
curdir = os.path.dirname(__file__)

def init_app(app: Flask):
    @app.cli.command(help='Populate db for the first time if empty')
    def populate_db():
        check_db_empty()
        new_data_to_db()

    @app.cli.command(help='Populate db safely')
    def new_data():
        new_data_to_db()

# sql = db.engine.dialect

diseases = json.load(open(os.path.join(curdir, 'diseases.json'), 'r'))


# def populate_first_data_file():
#     check_db_empty()
#     new_data_to_db()
#
#     path = os.environ['DATA_FILE']
#     df = load_reports_df(path)
#     put_reports_in_db(df)


def new_data_to_db():
    path = os.environ['DATA_FILE']
    df = load_reports_df(path)
    put_reports_in_db(df)


def check_db_empty():
    assert Report.query.count() == 0, 'reports table not empty'
    assert Disease.query.count() == 0, 'diseases table not empty'


def load_reports_df(path: str) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_pickle(path)
    df = (df
          .rename(columns=str.lower)
          .assign(disease_id=lambda x: x.disease.map(diseases))
          .assign(id=lambda x: x.disease_id.astype(str) + '_' + x.year.astype(str) + '_' + x.week.astype(str))
          .reset_index()
          .drop(columns=['disease'])
          )
    return df


def put_reports_in_db(df: pd.DataFrame):
    dids = pd.DataFrame(list(diseases.items()), columns=['disease', 'id'])
    _insert_df(dids, Disease)
    click.echo('Disease IDs written')
    _insert_df(df, Report)
    click.echo('All disease are in DB')
    db.session.commit()


def _insert_df(df, Orm: db.Model):
    # sql = db.engine.connect()
    sql = sa.dialects.postgresql
    records = df.to_dict(orient='records')
    click.echo(f'{len(records)} new records')
    insert_q = sql.insert(Orm).values(records)
    update_dict = {c.name: c for c in insert_q.excluded if not c.primary_key}
    upsert_q = (insert_q
                .on_conflict_do_update(index_elements=['id'],
                                       set_=update_dict)
                )
    db.session.execute(upsert_q)
    # db.session.commit()
