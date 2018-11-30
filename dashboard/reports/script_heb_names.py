import pandas as pd

records = pd.read_csv('info.csv').fillna("").to_dict('records')

base = "update diseases set disease_heb = '{disease_heb}', wiki_heb='{wiki_heb}', info_heb='{info_heb}' where id={id};"
for record in records[:]:
    for k,v in record.items():
        if k=='id':
            continue
        record[k] = v.replace("'","")
    print (base.format_map(record))