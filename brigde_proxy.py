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
    required_keys = ["target_domain"]
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
            if CONFIG_OBJECT.get("target_domain") == flow.request.pretty_host:
                if CONFIG_OBJECT.get("redirect_domain"):
                    flow.request.host = CONFIG_OBJECT.get("redirect_domain")
                
                if CONFIG_OBJECT.get("path_map"):
                    path_only = flow.request.path.split("?")[0]
                    if path_only in CONFIG_OBJECT.get("path_map"):
                        flow.request.path = CONFIG_OBJECT.get("path_map")[path_only]     
        except Exception as e:
            print(f"Request Exception: {e}")
            return   
    else:
        return

# Handle response
def response(flow: http.HTTPFlow):

    print(f"----response: {CONFIG_OBJECT}")
    if(CONFIG_OBJECT) :  
        try:
            if bool(CONFIG_OBJECT.get("modify_response")) & CONFIG_OBJECT.get("new_response_json"):
                flow.response.text = json.dumps(CONFIG_OBJECT.get("new_response_json"), ensure_ascii=False)
                flow.response.headers["Content-Type"] = "application/json"
        except:
            return
    else:
        return
