def split_k_v(text):
    ret = []
    while True:
        text = text.strip()
        if not text:
            break
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
            count_1 = 0
            while i < len(text):
                if text[i] == '"':
                    if count_1 == 0:
                        count_1 += 1
                    else:
                        count_1 -= 1
                if count_1 == 0:
                    if text[i] == flag:
                        count += 1
                    if text[i] == mapping[flag]:
                        count -= 1
                    if count == 0:
                        break
                i += 1
            i += 1
        while i < len(text) and (text[i] == ' ' or text[i] == '\n'):
            i += 1
        if i < len(text):
            flag = text[i]
            if flag == '"':
                i += 1
                while i < len(text) and text[i] != '"':
                    i += 1
                i += 1
        while i < len(text) and text[i] != ',':
            i += 1
        left = (text[:pos],text[pos+1:i])
        ret.append(left)
        text = text[i+1:]
    return ret


def split_arr(text):
    ret = []
    while True:
        text = text.strip()
        if not text:
            break
        i = 0
        flag = text[i]
        if flag in '[{':
            mapping = {'[': ']', '{': '}'}
            count = 0
            count_1 = 0
            while i < len(text):
                if text[i] == '"':
                    if count_1 == 0:
                        count_1 += 1
                    else:
                        count_1 -= 1
                if count_1 == 0:
                    if text[i] == flag:
                        count += 1
                    if text[i] == mapping[flag]:
                        count -= 1
                    if count == 0:
                        break
                i += 1
            i += 1
        while i < len(text) and (text[i] == ' ' or text[i] == '\n'):
            i += 1
        if i < len(text):
            flag = text[i]
            if flag == '"':
                i += 1
                while i < len(text) and text[i] != '"':
                    i += 1
                i += 1
        while i < len(text) and text[i] != ',':
            i += 1
        left = text[:i]
        ret.append(left)
        text = text[i + 1:]
    return ret


def parse_item(text):
    text = text.strip()
    if text[0] == '"' or text[0] == "'":
        return text[1:len(text)-1]
    if text[0] in '0123456789':
        return int(text)
    if text == 'null':
        return None
    if text == 'True':
        return True
    if text == 'False':
        return False
    raise Exception('cant parse')


def loads(text):
    text = text.strip()
    if text[0] == '{':
        data = {}
        k_v_arr = split_k_v(text[1:len(text)-1])
        for k,v in k_v_arr:
            k = parse_item(k)
            try:
                data[k] = loads(v)
            except:
                kkk = 0
        return data
    elif text[0] == '[':
        data = []
        arr = split_arr(text[1:len(text)-1])
        for item in arr:
            data.append(loads(item))
        return data
    return parse_item(text)


def pretty_print(data,depth=0,has_key=False,ident=4):
    if isinstance(data,dict):
        if has_key:
            print('{')
        else:
            print(' '*ident*depth + '{')
        for k in data:
            print(' '*ident*(depth+1) + str(k) + ':',end='')
            pretty_print(data[k],depth+1,has_key=True)
        if depth == 0:
            print(' '*ident*depth + '}')
        else:
            print(' ' * ident * depth + '},')
    elif isinstance(data,list):
        if has_key:
            print('[')
        else:
            print(' '*ident*depth + '[')
        for o in data:
            pretty_print(o,depth+1)
        if depth == 0:
            print(' ' * ident*depth + ']')
        else:
            print(' ' * ident*depth + '],')
    else:
        if has_key:
            print(str(data)+',')
        else:
            print(' '*ident*depth + str(data)+',')