from datetime import datetime, timedelta

import pandas as pd


def fighter_perfomance(df: pd.DataFrame, n_years: int) -> pd.DataFrame:
    """Generating the finghter performance rate based on the last N years

    Args:
        df (pd.DataFrame): fight history dataframe
        n_years (int): Number of years for performance rate

    Returns:
        pd.DataFrame: _description_
    """
    max_date = df["Date"].max()
    df_1 = (
        df[(df["Date"] >= max_date - timedelta(weeks=52 * n_years))]
        .groupby(["fighter1", "fighter1_result", "Weight"])["TIME_FORMAT"]
        .count()
        .unstack(level=-2)
        .fillna(0)
    )
    df_1.index.set_names(["fighter", "weight"], inplace=True)
    df_2 = (
        df[(df["Date"] >= max_date - timedelta(weeks=52 * n_years))]
        .groupby(["fighter2", "fighter2_result", "Weight"])["TIME_FORMAT"]
        .count()
        .unstack(level=-2)
        .fillna(0)
    )
    df_2.index.set_names(["fighter", "weight"], inplace=True)
    df_perf = df_1.add(df_2, fill_value=0)
    df_perf["n_fights"] = df_perf.sum(axis=1)
    df_perf["perf_rat"] = (df_perf["n_fights"] - df_perf["L"]) / df_perf["n_fights"]
    df_perf.columns = pd.Index(df_perf.columns.values.astype(str))
    df_perf = df_perf.sort_values(
        by=["perf_rat", "n_fights"], ascending=False
    ).reset_index(level=-1)
    return df_perf


if __name__ == "__main__":
    from mma_ranking.config import N_YEARS
    from mma_ranking.ranking.preprocess import load_train_data

    df = load_train_data()
    # df["Weight"] = df.apply(lambda x: weight(x.Weight), axis=1)
    performance_df = fighter_perfomance(df=df, n_years=N_YEARS)
    print(performance_df.head(3))
