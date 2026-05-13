import requests

session = requests.Session()

register_data = {
    'username': 'admin',
    'email': 'admin@example.com',
    'password': 'admin123',
    'confirm_password': 'admin123',
    'role': 'admin'
}

register_response = session.post('http://127.0.0.1:5000/register', json=register_data)
print("注册响应:", register_response.json())