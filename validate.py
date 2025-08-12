# Handle validate function
def exceptionValue(message):
    raise ValueError(message)

def isFormatArrayObject(data, required_keys):
    if not isinstance(data, list):
        return "JSON bắt buộc phải là list"

    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            return f"Phần tử thứ {idx} không phải object"
        for key in required_keys:
            if key not in item:
                return f"Phần tử thứ {idx + 1} thiếu key '{key}'"
    return None