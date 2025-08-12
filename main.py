import json
from mitmproxy import http
from response import modify_json_response
from validate import exceptionValue, isFormatArrayObject

# Read file JSON
with open("configs.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

# Check format json config
isCheckValidateConfig = isFormatArrayObject(CONFIG, ["target_domain", "path_map"])
if isCheckValidateConfig != None:
    exceptionValue(isCheckValidateConfig)

# Handle request
def request(flow: http.HTTPFlow):

    global CONFIG_OBJECT
    CONFIG_OBJECT = next(
        (cfg for cfg in CONFIG if flow.request.pretty_host == cfg.get("target_domain")),
        None
    )
    print(f"----request: {CONFIG_OBJECT}")
    if CONFIG_OBJECT != None:    
        try:
            pathOnly = flow.request.path.split("?")[0]
            if pathOnly in CONFIG_OBJECT.get("path_map"):
                pathKey = CONFIG_OBJECT.get("path_map")[pathOnly]
                pathRedirect = pathKey.get("redirect")
                if pathRedirect != None:

                    if CONFIG_OBJECT.get("redirect_domain"):
                        flow.request.host = CONFIG_OBJECT.get("redirect_domain")

                    flow.request.path = pathRedirect
                else:
                    CONFIG_OBJECT = None
            else:
                CONFIG_OBJECT = None     
        except Exception as e:
            print(f"Request Exception: {e}")
            return   
    else:
        return

# Handle response
def response(flow: http.HTTPFlow):

    print(f"----response: {CONFIG_OBJECT}")
    if CONFIG_OBJECT != None:  
        try:
            
            pathOnly = flow.request.path.split("?")[0]
            pathKey = CONFIG_OBJECT.get("path_map").get(pathOnly)
            modifyResponseType = pathKey.get("modify_response_type")
            isModify = modifyResponseType == "full" or modifyResponseType == "field" or modifyResponseType == "array"
            newResponse = pathKey.get("new_response_json")
            if isModify and newResponse != None:
                # flow.response.headers["Content-Type"] = "application/json"
                try:
                    original_json = json.loads(flow.response.text)
                except json.JSONDecodeError as e:
                    print(f"JSON parse error: {e}")
                    return  # Không phải JSON thì bỏ qua
                modifiedJson = modify_json_response(original_json, pathKey)
                flow.response.text = json.dumps(modifiedJson, ensure_ascii=False)

        except Exception as e:
            print(f"Error Response: {e}")
            return
    else:
        return
