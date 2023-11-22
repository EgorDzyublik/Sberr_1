import pandas as pd
import json
from media.functions import preprocessing, hellinger_distance, check_pronouns, jaro_winkler, normalization, text_to_id
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
from media.additional import NpEncoder


#функция, которая объединяет текста по рерайт-группам
def groups_clusters(data):
    df=pd.DataFrame(data)
    df['text_vir']=df['text']
    df=preprocessing(df)
    df=df.reset_index()
    df['text']=df['text'].apply(normalization)
    tfidf_vectorizer_bigrams = TfidfVectorizer(ngram_range=(1, 2))
    tfidf_bi_text = tfidf_vectorizer_bigrams.fit_transform(df['text'].to_list())
    num_clusters = 200
    kmeans = KMeans(n_clusters=num_clusters, max_iter=1000, random_state=100)
    kmeans_text = kmeans.fit(tfidf_bi_text)
    clusters=[]
    for cluster_id in range(num_clusters):
        group=[]
        cluster_indices = np.where(kmeans_text.labels_ == cluster_id)[0]
        for id in cluster_indices:
            group.append(df['text_vir'].iloc[id])
        clusters.append(group)

    groups=[] 
    #доп. обработка
    for cluster in clusters:
        if len(cluster) == 1:
            groups.append(cluster)
        if len(cluster) == 2:
            if ((jaro_winkler(cluster[0],cluster[1])>0.8) and (check_pronouns(cluster[0], cluster[1])) and (hellinger_distance(cluster[0], cluster[1])==1)):
                groups.append(cluster)  
            else:
                groups.append([cluster[0]])
                groups.append([cluster[1]])    
        if len(cluster) > 2:
            used = [False] * len(cluster)
            for i in range(len(cluster)):
                if used[i]:
                    continue
                for j in range(i+1,len(cluster)):
                    if used[j]:
                        continue
                    if ((jaro_winkler(cluster[i],cluster[j])>0.8) and (check_pronouns(cluster[i], cluster[j])) and (hellinger_distance(cluster[i], cluster[j])==1)):
                        used[i] = True
                        used[j] = True
                        groups.append([cluster[i],cluster[j]])
            for i in range(len(cluster)):
                if not used[i]:
                    groups.append([cluster[i]])         
    return text_to_id(df, groups)
