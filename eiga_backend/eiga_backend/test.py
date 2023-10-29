import requests

# 定义请求的 URL
url = "http://127.0.0.1:8000/user_register/"  # 替换为实际的 URL

# 定义请求的数据，通常是一个字典，包含您想要传递给视图的数据
data = {
    'user_id': '114514',
    'user_name': 'aona',
    'email': 'reoaoba@qq.com',
    'password': '123456',
    'permission': 'admin',
}

# 发送 POST 请求
response = requests.post(url, data=data)

# 处理响应
if response.status_code == 200:
    print("请求成功")
    # 如果需要，您可以访问响应的内容：response.text
else:
    print("请求失败")
    # 如果需要，您可以访问响应的内容：response.text
