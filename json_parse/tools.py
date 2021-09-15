def split_k_v(text):
    text = text.strip()
    if not text:
        return []
    i = 0
    while i < len(text) and text[i] != ':':
        i += 1
    pos = i
    i += 1
    while i < len(text) and (text[i] == ' ' or text[i] == '\n'):
        i += 1

    flag = text[i]
    if flag in '[{':
        mapping = {'[':']','{':'}'}
        count = 0
        while i < len(text):
            if text[i] == flag:
                count += 1
            if text[i] == mapping[flag]:
                count -= 1
            if count == 0:
                break
            i += 1
        i += 1
    else:
        if flag == '"':
            i += 1
            while i < len(text) and text[i] != '"':
                i += 1
            i += 1
    while i < len(text) and text[i] != ',':
        i += 1
    left = (text[:pos],text[pos+1:i])
    right = split_k_v(text[i+1:])
    return [left] + right


def split_arr(text):
    text = text.strip()
    if not text:
        return []
    i = 0
    flag = text[i]
    if flag in '[{':
        mapping = {'[': ']', '{': '}'}
        count = 0
        while i < len(text):
            if text[i] == flag:
                count += 1
            if text[i] == mapping[flag]:
                count -= 1
            if count == 0:
                break
            i += 1
        i += 1
    while i < len(text) and text[i] != ',':
        i += 1
    left = text[:i]
    right = split_arr(text[i + 1:])
    return [left] + right


def parse_item(text):
    text = text.strip()
    if text[0] == '"':
        return text[1:len(text)-1]
    if text[0] in '0123456789':
        return int(text)
    if text == 'null':
        return None
    raise Exception('cant parse')


def parse(text):
    text = text.strip()
    if text[0] == '{':
        data = {}
        k_v_arr = split_k_v(text[1:len(text)-1])
        for k,v in k_v_arr:
            k = parse_item(k)
            data[k] = parse(v)
        return data
    elif text[0] == '[':
        data = []
        arr = split_arr(text[1:len(text)-1])
        for item in arr:
            data.append(parse(item))
        return data
    return parse_item(text)

def pprint(data,depth=0,has_key=False,ident=4):
    if isinstance(data,dict):
        if has_key:
            print('{')
        else:
            print(' '*ident*depth + '{')
        for k in data:
            print(' '*ident*(depth+1) + str(k) + ':',end='')
            pprint(data[k],depth+1,has_key=True)
        print(' '*ident*depth + '}')
    elif isinstance(data,list):
        if has_key:
            print('[')
        else:
            print(' '*ident*depth + '[')
        for o in data:
            pprint(o,depth+1)
        print(' ' * ident*depth + ']')
    else:
        print(' '*ident*depth + str(data)+',')

s = '{"a":[1,{}]}'
print(parse(s))