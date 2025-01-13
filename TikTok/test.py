import os

from dotenv import load_dotenv
from tikapi import TikAPI, ValidationException, ResponseException


load_dotenv()
api_key = os.getenv("TIKAPI_KEY")
account_key = os.getenv("TIKAPI_ACCOUNT_KEY")
username = os.getenv("TIKTOKUSERNAME")

# 2. Initialize TikAPI
client = TikAPI(api_key)
User = client.user(accountKey=account_key)

try:
    response = User.posts.video(
        id="7003402629929913605"
    )

    print(response.json())

except ValidationException as e:
    print(e, e.field)

except ResponseException as e:
    print(e, e.response.status_code)


