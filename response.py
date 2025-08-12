from validate import isFormatArrayObject

def modify_json_response(originalJson, pathKey):
    try:
        modifyType = pathKey.get("modify_response_type")
        newData = pathKey.get("new_response_json")

        if modifyType == "full":
            return newData

        elif modifyType == "field" or modifyType == "array":
            path = newData.get("path")
            value = newData.get("value")
            if not path:
                return originalJson

            keys = path.split("/")
            temp = originalJson
            for k in keys[:-1]:
                if k not in temp or not isinstance(temp[k], dict):
                    temp[k] = {}
                temp = temp[k]
            
            if modifyType == "field":
                temp[keys[-1]] = value
            else:
                if value.get("field") != None:
                    arr = temp[keys[-1]]
                    if isFormatArrayObject(arr, [value.get("field")]) == None:
                        for obj in arr:
                            obj[value.get("field")] = value.get("value")                    
            return originalJson
        else:
            return originalJson
    except Exception as e:
        print(f"Error Modifier: {e}")
        return originalJson