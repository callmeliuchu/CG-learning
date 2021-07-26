s1 = '!(f)'
s2 = '|(f,t)'
s3 = '&(t,f)'
s4 = '|(&(t,f,t),!(t))'


def parse(s):
    if not s:
        return []
    count = 0
    i = 0
    j = -1
    if s[0] in '!|&':
        i += 1
    while i < len(s):
        if s[i] == '(':
            count += 1
        if s[i] == ')':
            count -= 1
        if count == 0:
            j = i
            break
        i = i + 1
    arr = [s[:j+1]]
    if j < len(s):
        arr = arr + parse(s[j+2:])
    return arr


def func(op,s):
    if not op:
        return True if s == 't' else False
    express_arr = parse(s)
    print(express_arr)
    ret = []
    for tmp in express_arr:
        if tmp[0] not in '!|&':
            ret.append(func('',tmp))
        else:
            ret.append(func(tmp[0],tmp[2:len(tmp)-1]))
    print(op,ret)
    if op == '|':
        return any(ret)
    elif op == '!':
        return not ret[0]
    else:
        return all(ret)

s4 = "|(f,&(t,t))"
print(func(s4[0],s4[2:len(s4)-1]))
