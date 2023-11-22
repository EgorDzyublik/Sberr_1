#функция которая проверяет 2 строки на отличие лишь в опечатках
def difference_is_only_typos(str1, str2):
    punct='''!"#$%&'()*+,./:;<=>?@[\]^_`{|}~'''
    for i in range(len(punct)):
        str1=str1.replace(punct[i], ' ')
        str2=str2.replace(punct[i], ' ')
    mas1=(str1.lower().split())
    mas2=(str2.lower().split())
    if len(mas1)!=len(mas2):
        return False
    typos=[]
    for i in range(len(mas1)):
        if mas1[i]!=mas2[i]:
            typos.append(mas1[i])
            typos.append(mas2[i])

    for i in range(0, len(typos), 2):
        k=0
        if (len(typos[i])==len(typos[i+1])):
            for j in range(len(typos[i])):
                if (typos[i][j]!=typos[i+1][j]):
                    k+=1
        else:
            return False
        if k<=1:
            return True
    return False


#Равенство мешка слов
def set_equal(str1, str2):
    mas1=str1.split()
    mas2=str2.split()
    if set(mas1)==set(mas2):
        return 1
    return 0




#ФУНКЦИЯ ЛЕВЕНШТЕЙНА
def levenstein(str_1, str_2):
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

#функция, которая проверяет являются ли строки рерайтами друг к другу
def is_rewrite(str1, str2):
    if str1[-1]!=str2[-1]:
        return False
    punct='''!"#$%&'()*+,./:;<=>?@[\]^_`{|}~'''
    for i in range(len(punct)):
        str1=str1.replace(punct[i], ' ')
        str2=str2.replace(punct[i], ' ')
    mas1=(str1.lower().split())
    mas2=(str2.lower().split())
    mas1.sort()
    mas2.sort()
    if (mas1==mas2):
        return True
    word1=[a for a in mas1 if a not in mas2]
    word2=[a for a in mas2 if a not in mas1]
    if (len(word1)!=1 or len(word2)!=1):
        return False
    if levenstein(word1[0], word2[0])==1 and len(word1[0])==len(word2[0]):
        return True
    return False


#функция, которая проверяет являются ли строки дубликатами
#дубликатами также назовём строки, которые отличаются друг от друга наличием опечатки
#например, "Я никогда там не был" и "Я никогда там не бнл" 
def is_dupls(str1, str2):
    punct='''!"#$%&'()*+,./:;<=>?@[\]^_`{|}~'''
    for i in range(len(punct)):
        str1_=str1.replace(punct[i], ' ')
        str2_=str2.replace(punct[i], ' ')
    mas1=(str1_.lower().split())
    mas2=(str2_.lower().split())

    if (len(mas1)!=len(mas2)):
        return False
    if mas1==mas2:
        return True
    

    return difference_is_only_typos(str1, str2)


#ОБРАБОТКА DATAFRAME
def preprocessing(df):
    mas=[i for i in df['id'].values]
    deleted=[]
    dupls=[]
    for ind1 in mas:
        if ind1 in deleted:
            continue
        deleted.append(ind1)
        for ind2 in mas:
            if ((ind2 not in deleted) and (is_dupls(df[df['id']==ind1]['text'].values[0], df[df['id']==ind2]['text'].values[0])==True)):
                dupls.append(ind2)
                deleted.append(ind2)
    for d in dupls:
        df=df[df['id']!=d]
    return df


#КЛАСТЕРИЗАЦИЯ
from pymorphy3 import MorphAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd

def normalization(string):
    string=string[:len(string)-1].lower()
    punct='''!"#$%&'()*+,./:;<=>?@[\]^_`{|}~'''
    for i in range(len(punct)):
        string=string.replace(punct[i], ' ')
    mas=string.split()
    morph=MorphAnalyzer()
    for i in range(len(mas)):
        mas[i]=morph.parse(mas[i])[0].normal_form
    string=' '.join(mas)
    return string

def text_to_id(data, groups):
    mas=[]
    for i in range(len(groups)):
        gr=[]
        for j in range(len(groups[i])):
            gr.append(int(data[data['text_vir']==groups[i][j]]['id'].values))
        mas.append(gr)
    return mas


#Проверка множества местоимений 2 строк на равенство
def check_pronouns(str1, str2):
    pronouns=["я", "мы", "ты", "вы", "он", "она", "оно", "они", "себя", "мой", "твой", "ваш", "наш", "свой", "его", "ее", "их", "то", "это", "тот", "этот", "такой", "таков", "столько", "весь", "всякий", "сам", "самый", "каждый", "любой", "иной", "другой", "кто", "что", "какой", "каков", "чей", "сколько", "кто", "что", "какой", "каков", "чей", "сколько", "никто", "ничто", "некого", "нечего", "никакой", "ничей", "нисколько", "кто-то", "кое-кто", "кто-нибудь", "кто-либо", "что-то", "кое-что", "что-нибудь", "что-либо", "какой-то", "какой-либо", "какой-нибудь", "некто", "нечто", "некоторый", "некий", "я", "ты", "он, оно", "она", "мы", "вы", "они", "меня", "тебя", "его", "её", "нас", "вас", "их", "мне", "тебе", "ему", "ей", "нам", "вам", "им", "меня", "тебя", "его", "её", "нас", "вас", "их", "мной", "мною", "тобой", "тобою", "им", "ею", "нами", "вами", "ими", "мне", "тебе", "нем", "ней", "нас", "вас", "них", "мой", "моя", "моё", "мои", "моего", "моей", "моего", "моих",  "моему", "моей", "моему", "моим", "мой", "моего", "мою", "мой", "моего", "мои", "моих", "моим", "моей", "моим", "моими", "моём", "моей", "моём", "моих"]
    mas1=(str1[:len(str1)-1].lower()).split()
    mas2=(str2[:len(str2)-1].lower()).split()
    prons1=[]
    prons2=[]
    for i in range(len(mas1)):
        if mas1[i] in pronouns:
            prons1.append(mas1[i])
    for i in range(len(mas2)):
        if mas2[i] in pronouns:
            prons2.append(mas2[i])
    return (set(prons1)==set(prons2))    


#РАССТОЯНИЕ ХЕЛЛИНГЕРА
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from math import sqrt
## Векторизация с помощью подсчета слов
def countVectorize(str1, str2):
    countVectorizer = CountVectorizer()
    countVector = countVectorizer.fit_transform([str1,str2])
    return countVector.toarray()
def hellinger_distance(str1, str2):
    vec = countVectorize(str1,str2)
    s = 0
    for p_i, q_i in zip(vec[0], vec[1]):
        s = (np.sqrt(p_i) - np.sqrt(q_i)) ** 2
    return 1 - np.sqrt(s / 2)


#ДЖАРО-ВИНКЛЕР
from math import floor
#Джаро
def jaro_distance(str1, str2):
    if (str1 == str2):
        return 1.0
    len1 = len(str1)
    len2 = len(str2)
    max_dist = floor(max(len1, len2) / 2) - 1
    match = 0
    hash1 = [0] * len(str1)
    hash2 = [0] * len(str2)
    for i in range(len1):
        for j in range(max(0, i - max_dist), 
                       min(len2, i + max_dist + 1)):
            if (str1[i] == str2[j] and hash2[j] == 0):
                hash1[i] = 1
                hash2[j] = 1
                match += 1
                break
    if (match == 0):
        return 0.0
    t = 0
    point = 0
    for i in range(len1):
        if (hash1[i]):
            while (hash2[point] == 0):
                point += 1
            if (str1[i] != str2[point]):
                t += 1
            point += 1
    t = t//2
    return (match/ len1 + match / len2 + (match - t) / match)/ 3.0

# Cходство Джаро-Винклера
def jaro_winkler(str1, str2): 
    jaro_dist = jaro_distance(str1, str2); 
    if (jaro_dist > 0.7) :
        prefix = 0
        for i in range(min(len(str1), len(str2))) :
            if (str1[i] == str2[i]):
                prefix += 1; 
            else :
                break
        prefix = min(4, prefix); 
        jaro_dist += 0.1 * prefix * (1 - jaro_dist); 
    return jaro_dist


#Расстояние Карловского
def karlovsky_distance(str1, str2):
    str1 = '\b\b' + str1 + '\f\f'
    str2 = '\b\b' + str2 + '\f\f'
    dist = -4
    for i in range(len(str1) - 2):
        if str1[i:i+3] not in str2:
            dist += 1
    for i in range(len(str2) - 2):
        if str2[i:i+3] not in str1:
            dist += 1
    return 1 - max(0, dist) / (len(str1) + len(str2) - 8)


#Коэффициент Танимото
def tanimoto(str1, str2):
    a, b, c = len(str1), len(str2), 0.0

    for sym in str1:
        if sym in str2:
            c += 1

    return c / (a + b - c)

def euclidean_distance(str1, str2):
    vec = countVectorize(str1, str2)
    distance = 0
    for i in range(len(vec[0])):
        distance += (vec[0][i] - vec[1][i])**2
    return 1 - sqrt(distance) / (sum(vec[0]) + sum(vec[1]))


#Косинусное расстояние
from numpy.linalg import norm
def cos_count(str1, str2):
    vec = countVectorize(str1, str2)
    return np.dot(vec[0],vec[1])/(norm(vec[0])*norm(vec[1]))


#N-gramms
def count_dictionary_entries(lines):
    sum = 0
    for key, value in lines.items():
        sum += value
    return sum

def build_ngrams(line, batch_size):
    result = {}
    if (len(line) < batch_size) :
        result[line] = 1
    else:
        for i in range(len(line) - batch_size):
            key = line[i: i + batch_size]
            if (' ' in key):
                continue
            old = result.get(key, 0)
            result[key] = old + 1
    return result

def n_gramms(str1, str2):
    dict1 = build_ngrams(str1, 2)
    dict2 = build_ngrams(str2, 2)
    cnt1 = count_dictionary_entries(dict1)
    cnt2 = count_dictionary_entries(dict2)
    overlaps = 0
    for key, value1 in dict1.items():
        value2 = dict2.get(key, 0)
        overlaps += min(value1, value2)
    return overlaps * 2 / (cnt1 + cnt2)


#Мера Сёренсена
def sorensen_dice_coefficient(str1, str2):
    a = set()
    b = set()
    for i in range(len(str1)-1):
        a.add(str1[i] + str1[i+1])
    for i in range(len(str2)-1):
        b.add(str2[i] + str2[i+1])
    return 2 * len(a & b) / (len(a) + len(b))


#функция, проверяющая являются ли рерайтами 2 строки, используя различные метрики сравнения 2 строк на схожесть
#каждая метрика имеет свой вес
def is_rewrite_metrics(str1, str2):
    w1=1
    w2=3
    w3=5

    str1=str1[:len(str1)-1].lower()
    str2=str2[:len(str2)-1].lower()

    f1=hellinger_distance(str1, str2)
    f2=tanimoto(str1, str2)
    f3=euclidean_distance(str1, str2)
    f4=jaro_winkler(str1, str2)
    f5=cos_count(str1, str2)
    f6=sorensen_dice_coefficient(str1, str2)
    f7=set_equal(str1, str2)
    f8=check_pronouns(str1, str2)
    f9=n_gramms(str1, str2)
    f10=karlovsky_distance(str1, str2)

    y=(w1*(f1+f2)+w2*(f3+f4+f5+f6+f7)+w3*(f8+f9+f10))/(2*w1+5*w2+3*w3)

    return y>=0.8


def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union


def is_rewrite_smart(str1, str2, sin_dict):
    if str1[-1]!=str2[-1]:
        return False
    punct='''!"#$%&'()*+,./:;<=>?@[\]^_`{|}~'''
    for i in range(len(punct)):
        str1=str1.replace(punct[i], ' ')
        str2=str2.replace(punct[i], ' ')
    str1=str1.lower()
    str2=str2.lower()
    mas1=(str1.split())
    mas2=(str2.split())
    mas1.sort()
    mas2.sort()
    if (mas1==mas2):
        return True
    word1=[a for a in mas1 if a not in mas2]
    word2=[a for a in mas2 if a not in mas1]
    if (len(word1)!=1 or len(word2)!=1):
        return False
    if levenstein(word1[0], word2[0])==1 and len(word1[0])==len(word2[0]):
        return True
    mas1=normalization(str1).split()
    mas2=normalization(str2).split()
    mas_similar=[]
    for i in range(len(mas1)):
        massiv_syns=[]
        if (((sin_dict[sin_dict['name']==mas1[i]]['similars'].values).size!=0) and ((sin_dict[sin_dict['name']==mas1[i]]['synonyms'].values).size!=0)):
            similars_1=list(sin_dict[sin_dict['name']==mas1[i]]['similars'].values[0])
            synonyms_1=list(sin_dict[sin_dict['name']==mas1[i]]['synonyms'].values[0])
            massiv_syns=similars_1+synonyms_1
        massiv_syns.append(mas1[i])
        mas_similar.append(massiv_syns)
    ch=0
    used=[]
    for i in range(len(mas2)):
        for j in range(len(mas_similar)):
            if j not in used:
                if mas2[i] in mas_similar[j]:
                    ch+=1
                    used.append(j)
    return (ch/len(mas2)==1)       

#Индекс Туманности Ганнинга
def gunning_fog_index_check(str1, str2):
    l1=str1.count('.')+str1.count('!')+str1.count('?')
    l2=str2.count('.')+str2.count('!')+str2.count('?')
    mas1=str1.split()
    mas2=str2.split()

    q_slov1=len(mas1)
    q_slov2=len(mas2)

    big_words1=[c for c in mas1 if (c.count('а')+c.count('е')+c.count('ё')+c.count('и')+c.count('о')+c.count('у')+c.count('ы')+c.count('э')+c.count('ю')+c.count('я'))>3]
    big_words2=[c for c in mas2 if (c.count('а')+c.count('е')+c.count('ё')+c.count('и')+c.count('о')+c.count('у')+c.count('ы')+c.count('э')+c.count('ю')+c.count('я'))>3]
    gunning_fog_index1=(0.4*(q_slov1/l1)+100*(len(big_words1)/q_slov1))
    gunning_fog_index2=(0.4*(q_slov2/l2)+100*(len(big_words2)/q_slov2))
    return ((gunning_fog_index1-gunning_fog_index2)<=1.5)


def is_rewrite_author_style(str1, str2):
    mas_introductory=['итак', 'следовательно', 'значит', 'напротив', 'наоборот', 'далее', 'наконец', 'впрочем', 'между прочим', 'в общем', 'в частности', 'кроме того','сверх того', 'прежде всего', 'стало быть', 'например', 'к примеру', 'главное', 'таким образом', 'кстати', 'кстати сказать', 'к слову сказать','во-первых','во-вторых', 'в-третьих', 'с одной стороны', 'с другой стороны', 'повторяю', 'подчеркиваю', 'словом', 'одним словом', 'иными словами','другими словами', 'иначе говоря', 'попросту говоря', 'мягко выражаясь', 'если можно сказать', 'если можно так выразиться', 'с позволения сказать','лучше сказать', 'так сказать', 'что называется', 'собственно говоря', 'вообще говоря', 'вернее сказать', 'точнее сказать', 'говорят', 'сообщают','передают', 'по словам', 'по сообщению', 'по сведениям','по мнению', 'по-моему', 'по-твоему', 'по-нашему', 'по-вашему', 'по слухам','по преданию', 'помнится', 'слышно', 'дескать', 'мол', 'видишь ли', 'видите ли', 'понимаешь ли', 'понимаете ли','знаешь ли', 'знаете ли','поймите', 'поверьте', 'послушайте', 'согласитесь','вообразите','представьте себе','извините','простите','веришь ли','верите ли','скажем','допустим','предположим','пожалуйста','к счастью','к несчастью','по счастью','по несчастью','к радости','к огорчению','к досаде','к прискорбию','к сожалению','к удивлению','к изумлению','к ужасу','к стыду','на радость','на счастье','на беду','чего доброго','нечего греха таить','странное дело','удивительное дело','неровен час','конечно', 'несомненно', 'без всякого сомнения', 'очевидно', 'безусловно', 'разумеется', 'бесспорно', 'действительно', 'наверное','возможно', 'верно', 'вероятно', 'по всей вероятности', 'может', 'может быть', 'быть может', 'должно быть', 'кажется', 'казалось бы', 'видимо', 'по-видимому', 'пожалуй', 'в самом деле', 'подлинно', 'правда', 'не правда ли', 'в сущности','по существу', 'по сути', 'надо полагать', 'думаю', 'надеюсь', 'полагаю', 'самое большее', 'самое меньшее', 'по крайней мере','бывает', 'бывало', 'случается', 'по обычаю', 'по обыкновению', 'по правде', 'по совести', 'по справедливости', 'кроме шуток', 'смешно сказать','не в укор будет сказано','признаться', 'надо сказать', 'сказать по чести', 'честно говоря', 'между нами говоря', 'между нами будь сказано']
    str1=str1.lower()
    str2=str2.lower()
    mas1_intrs=[]
    mas2_intrs=[]
    for i in range(len(mas_introductory)):
        if mas_introductory[i] in str1:
            mas1_intrs.append(mas_introductory[i])
    
    for i in range(len(mas_introductory)):
        if mas_introductory[i] in str2:
            mas2_intrs.append(mas_introductory[i])
    
    punct='''!"#$%&'()*+,./:;<=>?@[\]^_`{|}~'''
    punct1=[]
    for i in range(len(str1)):
        if punct.find(str1)>=0:
            punct1.append(str1[i])
    
    punct2=[]
    for i in range(len(str2)):
        if punct.find(str2)>=0:
            punct2.append(str2[i])
    if (len(mas1_intrs)==0 or len(mas2_intrs)==0):
        if ((set(punct1)==set(punct2)) and (gunning_fog_index_check(str1, str2)==True) and (n_gramms(str1, str2)>0.85) and check_pronouns(str1, str2)):
            return True
        return False
    if ((set(punct1)==set(punct2)) and (tanimoto(mas1_intrs, mas2_intrs)>0.5)  and (gunning_fog_index_check(str1, str2)==True) and(n_gramms(str1, str2)>0.85) and check_pronouns(str1, str2)):
        return True
    return False
    



    