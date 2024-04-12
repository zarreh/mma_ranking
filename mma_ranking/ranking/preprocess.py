import math

import numpy as np
import pandas as pd


def win_lose(fighter1_result: str, fighter1: str, fighter2: str) -> tuple[str, str]:
    if fighter1_result == "W":
        return fighter1, fighter2
    elif fighter1_result == "L":
        return fighter2, fighter1
    else:
        return fighter2, fighter1


def read_fights(path: str = r"data\all_fights_new.csv") -> pd.DataFrame:
    """
    _summary_

    Args:
        path (str, optional): path to the fights history. Defaults to r`../../data/all_fights_new.csv`.

    Returns:
        pd.DataFrame: fight history dataframe
    """

    def weight(w: str) -> str:
        """
        Clearning the weight class identifier

        Args:
            w (str): weight string

        Returns:
            str: cleaned wight string
        """
        if "Women's" in w:
            if "Strawweight" in w:
                new = "Women's Strawweight"
            elif "Flyweight" in w:
                new = "Women'sFlyweight"
            elif "antamweight" in w:
                new = "Women's Bantamweight"
            elif "Featherweight" in w:
                new = "Women's Featherweight"
        elif "Flyweight" in w:
            new = "Flyweight"
        elif "antamweight" in w:
            new = "Bantamweight"
        elif "Featherweight" in w:
            new = "Featherweight"
        elif "Lightweight" in w:
            new = "Lightweight"
        elif "Welterweight" in w:
            new = "Welterweight"
        elif "Middleweight" in w:
            new = "Middleweight"
        elif "Light Heavyweight" in w:
            new = "Light Heavyweight"
        elif "Heavyweight" in w:
            new = "Heavyweight"
        else:
            new = "other"
        return new

    df = pd.read_csv(path, parse_dates=True, low_memory=False)[
        [
            "Date",
            "fighter1",
            "fighter2",
            "fighter1_result",
            "fighter2_result",
            "BELT",
            "BOUNES",
            "Weight",
            "TIME_FORMAT",
            "Method",
            "Method_detail",
            "Judge1_score",
            "Judge2_score",
            "Judge3_score",
            "ROUND",
            "TIME",
        ]
    ]
    max_date = df["Date"].max()
    df = df[df["Date"] != "Date"]
    df.BOUNES = (df.BOUNES.str.split("/")).str[-1].str.split(".png").str[0]
    df.BELT = (df.BELT.str.split("/")).str[-1].str.split(".png").str[0]
    df.Weight = df.Weight.str.strip("Bout")
    df.Date = pd.to_datetime(df.Date.astype(str))
    df.TIME_FORMAT = df.TIME_FORMAT.str.split(" ").str[0]
    df = df[df["Date"] < str(max_date)]

    # correcting the weight string
    df["Weight"] = df.apply(lambda x: weight(x.Weight), axis=1)

    return df


def win_lose(fighter1_result, fighter1, fighter2):
    if fighter1_result == "W":
        return fighter1, fighter2
    elif fighter1_result == "L":
        return fighter2, fighter1
    else:
        return fighter2, fighter1


def adjust_draw(df):
    df_d = df[df["fighter1_result"] == "D"].copy()

    df_d["w_trans"] = df_d["winner"]
    df_d["winner"] = df_d["losser"]
    df_d["losser"] = df_d["w_trans"]
    df_d.drop("w_trans", axis=1, inplace=True)
    df = pd.concat([df, df_d], axis=0)
    return df


def method(m):
    if "Decision" in m:
        new = "Decision"
    elif "KO" in m:
        new = "KO"
    elif "Submission" in m:
        new = "sub"
    else:
        new = "other"
    return new


# assign values to method
def val(row):
    if row.fighter1_result == "D":
        new = 0
    elif row.fighter1_result == "NC":
        new = 0
    elif row.method == "Decision":
        new = 5
    else:
        new = 7

    if row.BELT == "belt":
        new = new * 2
    return new


# recencey ration
def recency(Date, dt):
    # ((dt - df['Date']).dt.days/365).apply(math.floor)
    date = math.floor((dt - Date).days / 365)
    if date < 3:
        val = 1
    elif date > 3 & date < 10:
        val = 1 - ((date - 2) / 10)
    else:
        val = 0.1
    return val


def load_train_data(path: str = r"data\all_fights_new.csv") -> pd.DataFrame:
    # adjusts the winner and losser position

    df = read_fights(path)
    max_date = df["Date"].max()

    df["winner"] = df.apply(
        lambda x: win_lose(x.fighter1_result, x.fighter1, x.fighter2), axis=1
    ).str[0]

    df["losser"] = df.apply(
        lambda x: win_lose(x.fighter1_result, x.fighter1, x.fighter2), axis=1
    ).str[1]

    df = adjust_draw(df)

    df["method"] = df.apply(lambda x: method(x.Method), axis=1)
    df["value"] = df.apply(lambda x: val(x), axis=1)

    df["adj"] = df.apply(lambda x: recency(x.Date, max_date), axis=1)
    df["adj_val"] = df["adj"] * df["value"]
    df.sort_values(by=["Date"], ascending=False, inplace=True)
    df["draw"] = np.where(df["fighter1_result"] == "D", True, False)

    df = df[
        [
            "Date",
            "winner",
            "losser",
            "BELT",
            "BOUNES",
            "Weight",
            "TIME_FORMAT",
            "Method",
            "Method_detail",
            "Judge1_score",
            "Judge2_score",
            "Judge3_score",
            "ROUND",
            "TIME",
            "fighter1",
            "fighter2",
            "fighter1_result",
            "fighter2_result",
            "method",
            "value",
            "adj",
            "adj_val",
            "draw",
        ]
    ]
    return df


if __name__ == "__main__":
    df = load_train_data()
    # df["Weight"] = df.apply(lambda x: weight(x.Weight), axis=1)
    print(df.head(3))
