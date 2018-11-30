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
sess=Session()
records = pd.read_csv('info.csv').fillna("").to_dict('records')

base = "update diseases set disease_heb = '{disease_heb}', wiki_heb='{wiki_heb}', info_heb='{info_heb}' where id={id};"
for record in records[:3]:
    # for k, v in record.items():
    #     if k == 'id':
    #         continue
    #     record[k] = v.replace("'", "")
    id_ = record.pop('id')
    # q = base.format_map(record)
    q = (sa.update(Disease)
     .values(**record)
     .where(Disease.id==id_))
    engine.execute(q)
# sess.commit()
