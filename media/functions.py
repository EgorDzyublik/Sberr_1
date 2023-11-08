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


#функция, обрабатывающая датафрейм, удаляет дубликаты
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

 
    



    