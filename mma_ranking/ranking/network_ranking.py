from datetime import timedelta
from typing import Union

import networkx as nx
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


def calculate_rank(df: pd.DataFrame) -> pd.DataFrame:
    "calculating the overal page rank for all weights at the same time"

    G_weighted = nx.from_pandas_edgelist(
        df, "losser", "winner", create_using=nx.DiGraph, edge_attr=["adj_val", "Date"]
    )

    weighted_pagerank = nx.pagerank(G_weighted, alpha=0.95)

    df_ranked = pd.DataFrame.from_dict(weighted_pagerank, orient="index")
    df_ranked.columns = ["page_rank"]
    df_ranked.sort_values(by=["page_rank"], ascending=False, inplace=True)
    df_ranked["run_date"] = df.Date.max()

    return df_ranked


def generate_ranks_weightclass(
    df: pd.DataFrame, file_name: Union[str, None] = None
) -> Union[pd.DataFrame, None]:
    "Generate the page rank for each weight class"

    weight_list = df["Weight"].unique()
    df_ranked = calculate_rank(df)
    df_w_rank_all = pd.DataFrame()
    performance_df = fighter_perfomance(df=df, n_years=3)
    max_date = df.Date.max()

    for weight_to_show in weight_list:
        # print(weight_to_show)

        cond = (df["Weight"] == weight_to_show) & (
            df["Date"] >= max_date - timedelta(weeks=52 * 3)
        )
        fighters_list = set(list(df[cond]["winner"]) + list(df[cond]["losser"]))
        df_w_rank = df_ranked[df_ranked.index.isin(fighters_list)].sort_values(
            by=["page_rank"], ascending=False
        )

        df_perf_select = (
            performance_df[
                (performance_df.index.isin(fighters_list))
                & (performance_df["weight"] == weight_to_show)
            ]
            .sort_values("perf_rat", ascending=False)[["perf_rat", "n_fights"]]
            .reset_index()
        )
        df_w_rank_select = df_w_rank.reset_index().rename({"index": "fighter"}, axis=1)

        df_w_rank_adj = pd.merge(
            df_w_rank_select, df_perf_select, on="fighter", how="inner"
        )  # .rename({'key_0':'fighter'}, axis=1)
        df_w_rank_adj["adj_p_rank"] = (
            df_w_rank_adj["page_rank"] * df_w_rank_adj["perf_rat"]
        )
        df_w_rank_adj.sort_values(
            by="adj_p_rank", ascending=False, inplace=True, ignore_index=True
        )

        df_w_rank_adj["weight"] = weight_to_show
        df_w_rank_adj["wight_class_rank"] = (
            df_w_rank_adj["adj_p_rank"]
            .rank(method="dense", ascending=False)
            .astype(int)
        )
        df_w_rank_all = pd.concat([df_w_rank_all, df_w_rank_adj])

    if file_name != "" and file_name is not None:
        df_w_rank_all[df_w_rank_all.wight_class_rank != "wight_class_rank"]
        df_w_rank_all.to_csv(file_name, mode="a", index=False, header=True)
        # df_w_rank_all.to_parquet(file_name, index=False, header=True)
        return None
    else:
        return df_w_rank_all


if __name__ == "__main__":
    from mma_ranking.config import N_YEARS
    from mma_ranking.ranking.preprocess import load_train_data

    df = load_train_data()
    # df["Weight"] = df.apply(lambda x: weight(x.Weight), axis=1)
    performance_df = fighter_perfomance(df=df, n_years=N_YEARS)
    print(performance_df.head(3))
