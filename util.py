def bitwiseAnd(a, b):

    res = ""

    for i in range(len(a)):
        if a[i] == "1" and a[i] == b[i]:
            res += a[i]
        else:
            res += "0"
            
    return res