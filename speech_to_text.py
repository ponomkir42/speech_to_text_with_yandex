import urllib.request
import json
import requests

# функция, которая генерирует iam_token при помощи oauth_token
# oauth_token берется здесь - https://oauth.yandex.ru/authorize?response_type=token&client_id=1a6990aa636648e9b2ef855fa7bec2fb
# FOLDER_ID - с главной страницы яндекс клауд https://console.cloud.yandex.ru/folders/b1gi<...>2plra2
# IAM-token живет до 12 часов!
def create_token(oauth_token):
    params = {'yandexPassportOauthToken': oauth_token}
    response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', params=params)
    decode_response = response.content.decode('UTF-8')
    text = json.loads(decode_response)
    iam_token = text.get('iamToken')
    expires_iam_token = text.get('expiresAt')

    return iam_token, expires_iam_token


OAUTH_TOKEN = 'y0_A<...>z_aTG3q7As'
result = create_token(OAUTH_TOKEN)
FOLDER_ID = 'b1g<...>lra2'
IAM_TOKEN = result[0]

with open("example.ogg", "rb") as f:
    data = f.read()

params = "&".join([
    "topic=general",
    "folderId=%s" % FOLDER_ID,
    "lang=ru-RU"
])

url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data)
url.add_header("Authorization", "Bearer %s" % IAM_TOKEN)

responseData = urllib.request.urlopen(url).read().decode('UTF-8')
decodedData = json.loads(responseData)

if decodedData.get("error_code") is None:
    print(decodedData.get("result"))
else:
    print(decodedData.get("error_code"))
