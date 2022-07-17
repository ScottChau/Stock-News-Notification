import requests
from datetime import datetime,timedelta 
from twilio.rest import Client

# API website 
# 1. https://newsapi.org/
# 2. https://www.alphavantage.co/
# 3. https://www.alphavantage.co/


# Fetch data for stock price
ALPHA_API_KEY = "YOUR_API_KEY"

STOCK = "TSLA"

stock_para = {
    "function": "TIME_SERIES_DAILY",
    "symbol":STOCK,
    "apikey":ALPHA_API_KEY,
}



# 
alpha_url = "https://www.alphavantage.co/query"

response = requests.get (url = alpha_url, params=stock_para)
response.raise_for_status()
data = response.json()

data_daily = data["Time Series (Daily)"]
data_list = [value for (key,value) in data_daily.items()]
yesterday_price = data_list[0]["4. close"]
before_yesterday_price= data_list[1]["4. close"]

time_list = [key for (key,value) in data_daily.items()]

price_diff = float(yesterday_price) - float(before_yesterday_price)

diff_percentage = round((price_diff / float(before_yesterday_price))* 100,2)


# Fetch data for news
NEWS_API_KEY = "YOUR_API_KEY"

new_url= "https://newsapi.org/v2/everything"

company = "Tesla"

new_para = {
    "q": company,
    "from": time_list[0],
    "apiKey": NEWS_API_KEY

}

response_new = requests.get(url = new_url ,params = new_para)
response_new.raise_for_status()
data_news = response_new.json()

twilio_account_sid = "YOUR_TWILIO_SID"
twilio_auth_token = "YOUR_TWILIO_AUTH_TOKEN"

if diff_percentage >= 5 or diff_percentage <= -5:
    new_list = []
    symbol = None
    for n in range(3):
        news = data_news["articles"][n]["title"]
        links = data_news["articles"][n]["url"]
        new_list.append(news)
        new_list.append(links)

    formatted_list = ("\n".join(new_list))

    if diff_percentage >=0:
        symbol = "🔺"
    else:
        symbol = "🔻"
    

    client = Client(twilio_account_sid,twilio_auth_token)
    message = client.messages.create(
                                    body = f" Tesla closing price on {time_list[0]} is {yesterday_price} and\n {time_list[1]} is {before_yesterday_price},\n Percentage difference is {symbol}{diff_percentage}%\nHere are some news for {company}:\n\n{formatted_list}",
                                    from_='YOUR_TWILIO_PHONE',
                                    to = "'YOUR_PHONE'"
                             )
    print(message.status)





