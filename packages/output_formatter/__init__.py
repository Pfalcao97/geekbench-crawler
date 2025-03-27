from datetime import datetime as dt

level_columns_mapper = {
    "simple": [
        "title",
        "single-core score",
        "multi-core score",
        "plataform",
        "validation status",
        "upload date",
        "operating system",
        "name",
        "size",
    ],
    "discrete": [
        "title",
        "single-core score",
        "multi-core score",
        "plataform",
        "validation status",
        "upload date",
        "operating system",
        "name",
        "size",
        'file compression', 
        'navigation', 
        'html5 browser', 
        'pdf renderer', 
        'photo library', 
        'clang', 
        'text processing', 
        'asset compression', 
        'object detection', 
        'background blur', 
        'horizon detection', 
        'object remover', 
        'hdr', 
        'photo filter', 
        'ray tracer', 
        'structure from motion',
    ]
}


def _try_rename(key:str) -> str:
    name_mapper = {
        "name": "processor",
        "size": "memory",
        "title": "computer model"
    }
    
    if key in name_mapper:
        return name_mapper[key]
    
    return key
    
def _value_format(key, value):
    
    if key == "upload date":

        return dt.strptime(value, "%B %d %Y %I:%M %p")

    return value

def _value_to_str(val) -> str:

    if isinstance(val, dt):
        return val.strftime("%Y-%m-%d %H:%M:%S")
    
    return str(val)

def dict_to_csv(raw_dict:dict, level:str, **kwargs) -> str:

    results = {
        _try_rename(_r[0]) : _value_format(_r[0], _r[1]) for _r in raw_dict.items() if _r[0] in level_columns_mapper[level]
    }

    default_name = f"{results['computer model'].replace(' ', '-')}_{int(results['upload date'].timestamp())}.csv"
    csv_name = kwargs.get("csv_name", default_name)

    if level == "simple":

        header = ",".join(results.keys())
        values = ",".join(
            map(
                _value_to_str,
                results.values()
            )
        )

        csv_str = "\n".join([header,values])
    elif level == "discrete":
        raise NotImplementedError("Level not yet implemeted")


    with open(csv_name, "w") as pen:
        pen.write(csv_str)



if __name__ == "__main__":
    print("Output formater")