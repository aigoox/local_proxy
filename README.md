# Hướng dẫn cài đặt

## Bước 1:

#### Chạy tải các thư viện:

```bash
pip install -r requirements.txt
```

#### Bước 2: chạy server

#### Bước 3: Truy cập http://mitm.it để cài đặt giấy phép https

#### Bước 4: Thêm proxy vào thiết bị
+ host: 127.0.0.1
+ port: 5579

> Có thể thay port khác nếu port đã bị chiếm dụng

# Chạy server

## - Giao diện website:

```bash
mitmweb -s main.py --listen-host 0.0.0.0 --listen-port 5579
```

## - Giao diện terminal:

```bash
mitmproxy -s main.py --listen-host 0.0.0.0 --listen-port 5579
```

## - Không có giao diện chỉ chạy server và logs:
| Khuyến khích

```bash
mitmdump -s main.py --listen-host 0.0.0.0 --listen-port 5579
```

# Format cấu hình mẫu

```
[
    {
        "target_domain": "testapi.io",
        "path_map": {
            "/api/xprogamer/test_proxy": {
                "redirect": "/api/xprogamer/test_proxy",
                "modify_response_type": "field",
                "status_code": 200,
                "new_response_json": {
                    "value": {
                        "field": "name",
                        "value": "test new field"
                    },
                    "path": "info/partition"
                }
            }
        }
    }
]
```

### Bảng chú thích


| Field                                   | Mô tả                      | Ghi chú                                                                              |
|-----------------------------------------|----------------------------|--------------------------------------------------------------------------------------|
| target_domain                           | Domain cần lắng nghe       | Bắt buộc                                                                             |
| redirect_domain                         | Domain chuyển hướng        | Không bắt buộc                                                                       |
| path_map/<path>                         | Cấu hình path thay thế     | Bắt buộc / Key(old_path)=Value (new_path) | Giữ nguyên path thì old_path = new_path  |
| path_map/new_response_json              | Cấu hình response thay thế | Bắt buộc khi modify_response = true                                                  |
| path_map/modify_response_type           | Kiểu thay đôi response     | full: Thay đổi full response / field: thay đổi giá trị cụ thể / None: không thay đổi |
| path_map/new_response_json/value        | Model thay đổi             | Dành cho modify_response_type = field                                                |
| path_map/new_response_json/path         | Path thay đổi trong json   | Dành cho modify_response_type = field và array                                       |
| path_map/new_response_json/value/value  | Model thay đổi             | Dành cho modify_response_type = array                                                |
| path_map/new_response_json/value/field  | Field cần thay đổi         | Dành cho modify_response_type = array                                                |
| path_map/new_response_json/status_code  | Status code của response   | Không bắt buộc - Không truyền sẽ lấy trạng thái của response thật                    |

### Ví dụ:

**Dữ liệu ban đầu**

```json
{
  "info": {
    "account": "tai_khoan_test",
    "old": 35,
    "partition": [
      {
        "id": 3,
        "name": "a"
      },
      {
        "id": 4,
        "name": "b"
      },
      {
        "id": 5,
        "name": "c"
      }
    ]
  },
  "is_login": true
}
```

- modify_response_type = full

```json
[
    {
        "target_domain": "testapi.io",
        "path_map": {
            "/api/xprogamer/test_proxy": {
                "redirect": "/api/xprogamer/test_proxy",
                "modify_response_type": "full",
                "new_response_json": {
                    "value": {
                        "status": "ok",
                        "debug": "edited by proxy",
                        "data": []
                    },
                    "path": "info/account"
                }
            }
        }
    }
]
```

**Kết quả**

```json
{
    "value": {
        "status": "ok",
        "debug": "edited by proxy",
        "data": []
    },
    "path": "info/account"
}
```

- modify_response_type = field

```json
[
    {
        "target_domain": "testapi.io",
        "path_map": {
            "/api/xprogamer/test_proxy": {
                "redirect": "/api/xprogamer/test_proxy",
                "modify_response_type": "field",
                "new_response_json": {
                    "value": {
                        "status": "ok",
                        "debug": "edited by proxy",
                        "data": []
                    },
                    "path": "info/account"
                }
            }
        }
    }
]
```

**Kết quả**

```json
{
  "info": {
    "account": {
        "status": "ok",
        "debug": "edited by proxy",
        "data": []
    },
    "partition": [
      {
        "id": 3,
        "name": "a"
      },
      {
        "id": 4,
        "name": "b"
      },
      {
        "id": 5,
        "name": "c"
      }
    ],
    "old": 35
  },
  "is_login": true
}
```

- modify_response_type = array

```json
[
    {
        "target_domain": "testapi.io",
        "path_map": {
            "/api/xprogamer/test_proxy": {
                "redirect": "/api/xprogamer/test_proxy",
                "modify_response_type": "array",
                "new_response_json": {
                    "value": {
                        "field": "name",
                        "value": "test new field"
                    },
                    "path": "info/partition"
                }
            }
        }
    }
]
```

**Kết quả**

```json
{
  "info": {
    "account": "tai_khoan_test",
    "partition": [
      {
        "id": 3,
        "name": "test new field"
      },
      {
        "id": 4,
        "name": "test new field"
      },
      {
        "id": 5,
        "name": "test new field"
      }
    ],
    "old": 35
  },
  "is_login": true
}
```