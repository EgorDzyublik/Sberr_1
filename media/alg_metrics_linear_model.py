import pandas as pd
import json
from media.functions import preprocessing, is_rewrite_metrics
from media.additional import NpEncoder



#функция, которая объединяет текста по рерайт-группам с помощью различных метрик
def groups_metrics(data):
    df=pd.DataFrame(data)
    df=preprocessing(df)
    mas=[i for i in df['id'].values]
    result_ids=[]
    counter=1
    deleted=[]
    for ind1 in mas:
        if ind1 in deleted:
            continue
        result_ids.append([ind1])
        deleted.append(ind1)
        for ind2 in mas:
            if ((ind2 not in deleted) and (is_rewrite_metrics(df[df['id']==ind1]['text'].values[0], df[df['id']==ind2]['text'].values[0])==True)):
                result_ids[counter-1].append(ind2)
                deleted.append(ind2)
        counter+=1
    return result_ids
