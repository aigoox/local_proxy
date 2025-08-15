from validate import isFormatArrayObject, exceptionValue

def handle_set_response(original_json, array_field):
    isFormat = isFormatArrayObject(array_field, ["field"])

    print(isFormat)
    if isFormat != None:
        exceptionValue(isFormat)
        return
    for item in array_field:
        original_json[item.get("field")] = item.get("value",None)

    return original_json

def modify_json_response(originalJson, pathKey):
    try:
        modifyType = pathKey.get("modify_response_type")
        newData = pathKey.get("new_response_json")

        if modifyType == "full":
            return pathKey

        elif modifyType == "field" or modifyType == "array":
            
            temp = originalJson
            path = newData.get("path", "")
            if "value" in newData:
                value = newData.get("value")
                keys = None
                if len(path) > 1:
                    keys = path.split("/")
                    for k in keys[:-1]:
                        if k not in temp or not isinstance(temp[k], dict):
                            temp[k] = {}
                        temp = temp[k]
                print(f"------- keys: {keys}")

                if modifyType == "field":
                    if keys != None:
                        temp[keys[-1]] = handle_set_response(temp[keys[-1]], value)
                    else: 
                        temp = handle_set_response(temp, value)
                else:
                    if keys != None:
                        arr = temp[keys[-1]]
                    else: 
                        arr = temp
                    
                    for obj in arr:
                        obj = handle_set_response(obj, value)
                print(f"origin: {originalJson}")                 
            return originalJson
        else:
            return originalJson
    except Exception as e:
        print(f"Error Modifier: {e}")
        return originalJson