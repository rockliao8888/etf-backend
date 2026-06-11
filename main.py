from fastapi import FastAPI
import requests
import pandas as pd

app = FastAPI()
@app.get("/")
def home():
    return {"message": "API OK"}

def fetch_data():
    url = "https://www.twse.com.tw/rwd/zh/ETF/getEtfQuote"
    res = requests.get(url)
    data = res.json()

    df = pd.DataFrame(data['data'])

    df.columns = [
        "id","name","price","change","change_percent",
        "volume","open","high","low"
    ]

    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    df["nav"] = df["price"] * 0.99
    df["premium"] = (df["price"] - df["nav"]) / df["nav"] * 100

    df["yield"] = 3 + (df.index % 5)
    df["aum"] = 1000 + df.index * 50

    return df.to_dict(orient="records")


@app.get("/rank/{type}")
def rank(type: str):
    data = fetch_data()

    if type == "yield":
        data.sort(key=lambda x: x['yield'], reverse=True)
    elif type == "premium":
        data.sort(key=lambda x: x['premium'], reverse=True)
    elif type == "aum":
        data.sort(key=lambda x: x['aum'], reverse=True)

    return data
