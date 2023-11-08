import pandas as pd
import json
from media.functions import is_rewrite, preprocessing
from media.additional import NpEncoder

#функция, которая объединяет текста по рерайт-группам
def groups(data):
    df=pd.DataFrame(data)
    df=preprocessing(df)
    mas=[i for i in df['id'].values]
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
            if ((ind2 not in deleted) and (is_rewrite(df[df['id']==ind1]['text'].values[0], df[df['id']==ind2]['text'].values[0])==True)):
                result_dict['ids'][counter-1].append(ind2)
                deleted.append(ind2)
        counter+=1
    result_list=[]
    result_list.append(result_dict['num'])
    result_list.append(result_dict['ids'])
    return result_list
