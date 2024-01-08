import requests

url = 'https://flibusta.is/b/34212/fb2'  # замените на URL файла .zip

response = requests.get(url)

if response.status_code == 200:
    with open('file.zip', 'wb') as file:
        file.write(response.content)
    print("Файл успешно скачан")
else:
    print("Ошибка при скачивании файла")
