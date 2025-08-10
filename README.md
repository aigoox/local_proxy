# Hướng dẫn cài đặt

### Bước 1:

- Chạy tải các thư viện:

```bash
pip install -r requirements.txt
```

- Bước 2: chạy server

- Bước 3: Truy cập http://mitm.it để cài đặt giấy phép https

- Bước 4: Thêm proxy vào thiết bị
+ host: 127.0.0.1
+ port: 5579

>> Có thể thay port khác nếu port đã bị chiếm hữu!



# Chạy server

## - Giao diện website:

```bash
mitmweb -s brigde_proxy.py --listen-host 0.0.0.0 --listen-port 5579
```

## - Giao diện terminal:

```bash
mitmproxy -s brigde_proxy.py --listen-host 0.0.0.0 --listen-port 5579
```

## - Không có giao diện chỉ chạy server và logs:

```bash
mitmdump -s brigde_proxy.py --listen-host 0.0.0.0 --listen-port 5579
```

# Format mẫu

```
[
    {
        "target_domain": "testapi.io",
        "redirect_domain": "facebook.com"
        "path_map": {
            "/api/aprogamer/assets": "/login",
            "/api/xprogamer/persons": "/register"
        },
        "modify_response": true,
        "new_response_json": {
            "status": "ok",
            "debug": "edited by proxy",
            "data": []
        }
    }
]
```