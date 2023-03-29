import pandas as pd


def getdata():
    data = pd.read_csv("prompts.csv")
    x = data["prompt"].tolist()
    return x
