import json
from mitmproxy import http
from response import modify_json_response
from validate import exceptionValue, isFormatArrayObject

CONFIG_OBJECT = {}

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
    host = flow.request.pretty_host
    path = flow.request.path
    print(f"Request : {host}{path}")
    dataFilter = next(
        (cfg for cfg in CONFIG if host == cfg.get("target_domain")),
        None
    )
    pathSplit = path.split("?")
    pathOnly = pathSplit[0]

    if dataFilter == None:
        CONFIG_OBJECT[pathOnly] = dataFilter
        return 
    CONFIG_OBJECT[path] = dataFilter
    if dataFilter != None:    
        try:
            
            print(f"---- pathSplit: {pathSplit}")
            if pathOnly in dataFilter.get("path_map"):
                
                print(f"----request: {host} | {dataFilter}")
                pathKey = dataFilter.get("path_map")[pathOnly]
                pathRedirect = pathKey.get("redirect")
                if pathRedirect != None:

                    if dataFilter.get("redirect_domain"):
                        flow.request.host = dataFilter.get("redirect_domain")

                    if(len(pathSplit) > 1):
                        pathRedirect += f"?{pathSplit[1]}"

                    print(f"Path chuyển đổi: {pathRedirect}")
                    flow.request.path = pathRedirect
                else:
                    print(f"setup one 1 - {pathOnly}")
                    CONFIG_OBJECT[pathOnly] = None
            else:
                print(f"setup one 2 - {pathOnly}")
                CONFIG_OBJECT[pathOnly] = None     
        except Exception as e:
            print(f"setup one 3 - {pathOnly}")
            CONFIG_OBJECT[pathOnly] = None 
            print(f"Request Exception: {e}")
            return   
    else:
        print(f"setup one 4")
        CONFIG_OBJECT[pathOnly] = None
        return

# Handle response
def response(flow: http.HTTPFlow):

    if CONFIG_OBJECT == None:
        print(f"----response: None")
        return

    path = flow.request.path
    pathSplit = path.split("?")
    pathOnly = pathSplit[0]

    dataConfig = CONFIG_OBJECT.get(pathOnly)

    print(f"----response: {dataConfig}")

    if dataConfig != None:  
        try:
            
            pathOnly = flow.request.path.split("?")[0]
            pathKey = dataConfig.get("path_map").get(pathOnly)
            modifyResponseType = pathKey.get("modify_response_type")
            isModify = modifyResponseType == "full" or modifyResponseType == "field" or modifyResponseType == "array"
            newResponse = pathKey.get("new_response_json")

            if pathKey.get("status_code") != None:
                flow.response.status_code = pathKey.get("status_code")

            if isModify and newResponse != None:
                # flow.response.headers["Content-Type"] = "application/json"
                try:
                    original_json = json.loads(flow.response.text)
                except json.JSONDecodeError as e:
                    print(f"JSON parse error: {e}")
                    return
                modifiedJson = modify_json_response(original_json, pathKey)
                flow.response.text = json.dumps(modifiedJson, ensure_ascii=False)
                CONFIG_OBJECT[pathOnly] = None
        except Exception as e:
            print(f"Error Response: {e}")
            
            CONFIG_OBJECT[pathOnly] = None
            return
    else:
        return
