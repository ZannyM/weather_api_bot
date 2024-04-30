import requests
import os
from dotenv import load_dotenv

def get_weather(city):
    load_dotenv()
    api_url = 'https://api.api-ninjas.com/v1/weather?city={}'.format(city)
    response = requests.get(api_url, headers={'X-Api-Key': os.environ.get('API_KEY')})
    if response.status_code == requests.codes.ok:
        if response.json() == []:
            return "⚠️Weather Details Not Found"
        else:
            joke = response.json()
            return joke
        # # print(response.text)
        # print(response.text)
    else:
        print("Error:", response.status_code, response.text)

if __name__ == "__main__":
    print(get_weather('johannesburg'))




