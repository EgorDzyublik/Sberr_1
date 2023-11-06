import pandas as pd
import json
from myblog.progr.functions import is_rewrite
with open('sample.json', encoding="utf-8") as sber_file:
    f = json.load(sber_file)

def func(data):
    df=pd.DataFrame(data)
    df=df[df['id']!=314]
    mas=[i for i in range(1, len(df))]
    result_dict={'num': [], 'ids': []}
    counter=1
    deleted=[]
    for ind1 in mas:
        if ind1 in deleted:
            continue
        result_dict['num'].append(counter)
        result_dict['ids'].append([ind1])
        deleted.append(ind1)
        for ind2 in mas:
            if ((ind2 not in deleted) and (is_rewrite(df.iloc[ind1-1]['text'], df.iloc[ind2-1]['text'])==True)):
                result_dict['ids'][counter-1].append(ind2)
                deleted.append(ind2)
        counter+=1
    result_json=json.dumps(result_dict, indent=9)
    return result_json
result_file = func(f)
print(result_file)