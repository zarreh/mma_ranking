from datetime import datetime, timedelta

import pandas as pd

# dt = datetime.strptime('2020-04-01', '%Y-%m-%d')
dt = datetime.today()  # .date()
str(dt)


def read_fights(path: str = r"..\..\data\all_fights_new.csv") -> pd.DataFrame:
    """_summary_

    Args:
        path (str, optional): path to the fights history. Defaults to r"..\..\data\all_fights_new.csv".

    Returns:
        pd.DataFrame: fight history dataframe
    """
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
    df = df[df["Date"] != "Date"]
    df.BOUNES = (df.BOUNES.str.split("/")).str[-1].str.split(".png").str[0]
    df.BELT = (df.BELT.str.split("/")).str[-1].str.split(".png").str[0]
    df.Weight = df.Weight.str.strip("Bout")
    df.Date = pd.to_datetime(df.Date.astype(str))
    df.TIME_FORMAT = df.TIME_FORMAT.str.split(" ").str[0]
    df = df[df["Date"] < str(dt)]
    return df


# df = read_fights()


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


# df["Weight"] = df.apply(lambda x: weight(x.Weight), axis=1)


def fighter_perfomance(df: pd.DataFrame, n_years: int) -> pd.DataFrame:
    """Generating the finghter performance rate based on the last N years

    Args:
        df (pd.DataFrame): fight history dataframe
        n_years (int): Number of years for performance rate

    Returns:
        pd.DataFrame: _description_
    """
    df_1 = (
        df[(df["Date"] >= dt - timedelta(weeks=52 * n_years))]
        .groupby(["fighter1", "fighter1_result", "Weight"])["TIME_FORMAT"]
        .count()
        .unstack(level=-2)
        .fillna(0)
    )
    df_1.index.set_names(["fighter", "weight"], inplace=True)
    df_2 = (
        df[(df["Date"] >= dt - timedelta(weeks=52 * n_years))]
        .groupby(["fighter2", "fighter2_result", "Weight"])["TIME_FORMAT"]
        .count()
        .unstack(level=-2)
        .fillna(0)
    )
    df_2.index.set_names(["fighter", "weight"], inplace=True)
    df_perf = df_1.add(df_2, fill_value=0)
    df_perf["n_fights"] = df_perf.sum(axis=1)
    df_perf["perf_rat"] = (df_perf["n_fights"] - df_perf["L"]) / df_perf["n_fights"]
    df_perf.columns = df_perf.columns.values
    df_perf = df_perf.sort_values(
        by=["perf_rat", "n_fights"], ascending=False
    ).reset_index(level=-1)
    return df_perf
