import os

import dotenv
import pandas as pd
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from explorer.models import Disease

dotenv.load_dotenv()
engine = sa.create_engine(os.environ['DATABASE_URL'])
conn = engine.connect()
Session = sessionmaker(bind=engine)
sess = Session()

path = os.path.join(os.path.dirname(__file__), 'info.csv')
records = pd.read_csv(path).fillna("").to_dict('records')

base = "update diseases set disease_heb = '{disease_heb}', wiki_heb='{wiki_heb}', info_heb='{info_heb}' where id={id};"
for record in records[:]:
    id_ = record.pop('id')
    q = (sa.update(Disease)
         .values(**record)
         .where(Disease.id == id_))
    engine.execute(q)
    print (f'updated {id_}')
