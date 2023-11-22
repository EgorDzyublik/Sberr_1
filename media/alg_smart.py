import pandas as pd
import json
from media.functions import is_rewrite_smart, preprocessing
from media.additional import NpEncoder


with open('media/dictionary.json', encoding="utf-8") as file1:
    sin_dict = json.load(file1)
sin_dict=list(sin_dict.items())
sin_dict_df=pd.DataFrame(sin_dict[3][1])

sin_dict_df=sin_dict_df.drop(columns=['antonyms', 'definition'])
sin_dict_df=sin_dict_df.dropna()
sin_dict_df['name']=sin_dict_df['name'].apply(lambda x: x.lower())


#функция, которая объединяет текста по рерайт-группам
def groups_alg_smart(data, sin_dict_df):
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
            if ((ind2 not in deleted) and (is_rewrite_smart(df[df['id']==ind1]['text'].values[0], df[df['id']==ind2]['text'].values[0], sin_dict_df)==True)):
                result_ids[counter-1].append(ind2)
                deleted.append(ind2)
        counter+=1
    return result_ids
