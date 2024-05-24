def validate_dict(format:dict, data:dict)->bool:
    for key, rule in format.items():
        if rule.get["__required"] and key not in data:
            print(f"❌  Missing required field {key}. @channel_points.py(validate_dict)")
            return False
        if rule.get("__type"):
            tpe = rule.get("__type")
            if not isinstance(data[key], tpe):
                print(f"❌  Invalid type for {key}. @channel_points.py(validate_dict)")
                return False
        if rule.get("__length"):
            min, max = rule.get("__length").split("..")
            min = int(min) if min else -999_999_999
            max = int(max) if max else 999_999_999
            if not isinstance(data[key], int) and not isinstance(data[key], dict):
                if not min <= len(data[key]) <= max:
                    print(f"❌  Invalid length for {key}. @channel_points.py(validate_dict)\n->length must be between {min} and {max}")
                    return False
            elif not isinstance(data[key], dict):
                if not min <= data[key] <= max:
                    print(f"❌  Invalid value for {key}. @channel_points.py(validate_dict)\n->value must be between {min} and {max}")
                    return False