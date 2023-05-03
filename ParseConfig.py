from ConfigHash import MultiRegexDict
import json,re
from json.decoder import JSONDecodeError

def permissive_json_loads(text):
    while True:
        try:
            data = json.loads(text)
        except JSONDecodeError as exc:
            if exc.msg == 'Invalid \\escape':
                text = text[:exc.pos] + '\\' + text[exc.pos:]
            else:
                raise
        else:
            return data

def traverse_json(data, path=[], result=[]):
    if isinstance(data, dict):
        for key, value in data.items():
            traverse_json(value, path + [key], result)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            traverse_json(item, path + [i], result)
    else:
        result.append(path + [data])

    return result

# 示例JSON数据
def AnnotationHashLoad( inputJson  ):
    data = permissive_json_loads(open(inputJson).read())
    result = traverse_json(data)
    data_hash = MultiRegexDict()
    for e_path in result:
        start = "data_hash"

        for i in range(0, len(e_path[:-1])):
            if e_path[i].startswith("compile#"):
                e_path[i] = re.sub("^compile#", "", e_path[i])

                start += "[re.compile(e_path[%s]  ) ]" % (i)
            else:
                start += "[e_path[%s] ]" % (i)

        start += "= e_path[%s]" % (len(e_path[:-1]))
        # print(start)
        exec(start)
    return data_hash
# 以下为测试

# data = permissive_json_loads(open("Config.json").read())
# data_hash = AnnotationHashLoad( "Config.json" )


# print(data_hash)
