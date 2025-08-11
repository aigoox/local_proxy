import json
from mitmproxy import http

# Handle validate function
def exceptionValue(message):
    raise ValueError(message)

# Read file JSON
with open("configs.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

# Check format json config
if not isinstance(CONFIG, list):
    exceptionValue("JSON bắt buộc phải là list")

for idx, item in enumerate(CONFIG):
    if not isinstance(item, dict):
        exceptionValue(f"Phần tử thứ {idx} không phải object")
    required_keys = ["target_domain", "path_map"]
    for key in required_keys:
        if key not in item:
            exceptionValue(f"Phần tử thứ {idx + 1} thiếu key '{key}'")

# Handle request
def request(flow: http.HTTPFlow):

    global CONFIG_OBJECT
    CONFIG_OBJECT = next(
        (cfg for cfg in CONFIG if flow.request.pretty_host == cfg.get("target_domain")),
        None
    )
    print(f"----request: {CONFIG_OBJECT}")
    if(CONFIG_OBJECT) :    
        try:
            path_only = flow.request.path.split("?")[0]
            if path_only in CONFIG_OBJECT.get("path_map"):
                if CONFIG_OBJECT.get("redirect_domain"):
                    flow.request.host = CONFIG_OBJECT.get("redirect_domain")

                flow.request.path = CONFIG_OBJECT.get("path_map")[path_only]
            else:
                CONFIG_OBJECT = None     
        except Exception as e:
            print(f"Request Exception: {e}")
            return   
    else:
        return

def modify_json_response(original_json):
    try:
        modify_type = CONFIG_OBJECT.get("modify_response_type")
        new_data = CONFIG_OBJECT.get("new_response_json")

        if modify_type == "full":
            return new_data

        elif modify_type == "field":
            path = new_data.get("path")
            value = new_data.get("value")
            if not path:
                return original_json

            keys = path.split("/")
            temp = original_json
            for k in keys[:-1]:
                if k not in temp or not isinstance(temp[k], dict):
                    temp[k] = {}
                temp = temp[k]
            temp[keys[-1]] = value
            return original_json

        else:
            return original_json
    except Exception as e:
        print(f"Error Modifier: {e}")


# Handle response
def response(flow: http.HTTPFlow):

    print(f"----response: {CONFIG_OBJECT}")
    if(CONFIG_OBJECT) :  
        try:
            modifyResponseType = CONFIG_OBJECT.get("modify_response_type")
            isModify = modifyResponseType == "full" or modifyResponseType == "field"
            newResponse = CONFIG_OBJECT.get("new_response_json")
            if isModify and newResponse != None:
                # flow.response.headers["Content-Type"] = "application/json"
                try:
                    original_json = json.loads(flow.response.text)
                except json.JSONDecodeError as e:
                    print(f"JSON parse error: {e}")
                    return  # Không phải JSON thì bỏ qua
                modified_json = modify_json_response(original_json)
                print(f"after response: {modified_json}")
                flow.response.text = json.dumps(modified_json, ensure_ascii=False)
                print(f"after response modify: {flow.response.text}")

        except Exception as e:
            print(f"Error Response: {e}")
            return
    else:
        return
