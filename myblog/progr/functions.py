def is_rewrite(str1, str2):
    if str1[-1]!=str2[-1]:
        return False
    mas1=(str1[:len(str1)-1].lower().split())
    mas2=(str2[:len(str2)-1].lower().split())
    if (str1!=str2 and set(mas1)==set(mas2)):
        return True
    return False