from sklearn.preprocessing import MinMaxScaler # type: ignore
from datetime import timedelta
from typing import Union

import networkx as nx # type: ignore
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
    df_ranked.columns = pd.Index(["page_rank"])  # Fix: Convert the list to a pandas Index object
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
    

def normalizing_page_rank_per_class(
    rankings_df, weight_class_list, run_date, page_rank_column="adj_p_rank"
):
    rankings_df_new = pd.DataFrame()

    for weight_class_ in weight_class_list:
        rankings_df_ = rankings_df[
            (rankings_df["weight"] == weight_class_)
            & (rankings_df["run_date"] == run_date)
        ]

        # standardize the ranking values
        scaler_2 = MinMaxScaler()
        rankings_df_.loc[:, page_rank_column + "_scaled"] = scaler_2.fit_transform(
            rankings_df_[page_rank_column].values.reshape(-1, 1)
        )
        rankings_df_new = pd.concat([rankings_df_new, rankings_df_])
    return rankings_df_new

def ranking_dictionary(rankings_df_new, weight_class, run_date):
    fighter_rankings = (
        rankings_df_new[
            (rankings_df_new["weight"] == weight_class)
            & (rankings_df_new["run_date"] == run_date)
        ][["fighter", "wight_class_rank", "adj_p_rank_scaled"]]
        .set_index("fighter")
        .to_dict("index")
    )
    return fighter_rankings

def adjust_ranking_based_on_matches(
    matches_sorted: pd.DataFrame,
    fighter_rankings: dict["str", dict["str", Union[float, int]]],
    ranking_column: str,
    page_rank_column: str,
    epsilon: float = 0.00001,
    verbose: bool = False,
):

    # ranking_column
    for _, match in matches_sorted.iterrows():
        winner = match["winner"]
        loser = match["losser"]
        date = match["Date"]

        if match["draw"]:
            # Skip if it's a draw since nobody wins or loses
            continue
        if winner not in fighter_rankings or loser not in fighter_rankings:
            # Skip if either fighter is not in the rankings
            continue
        # Check if the winner's page_rank is less than the loser's
        if (
            fighter_rankings[winner][ranking_column]
            >= fighter_rankings[loser][ranking_column]
        ):

            winner_rank = fighter_rankings.get(winner, {"rank": 0})[ranking_column]
            loser_rank = fighter_rankings.get(loser, {"rank": 0})[ranking_column]
            if verbose:
                print("date: {}".format(date))
                print(
                    "Before change --> winner name {} --> rank: {} \n loser name {} --> rank: {}".format(
                        winner, winner_rank, loser, loser_rank
                    )
                )

            # Update the winner's page_rank to match the loser's
            fighter_rankings[winner][page_rank_column] = (
                fighter_rankings[loser][page_rank_column] + epsilon
            )
            # Ensure winner's rank is better (lower) than the loser's
            # We find the next better rank that is not occupied by another fighter
            fighter_rankings[winner][ranking_column] = fighter_rankings[loser][
                ranking_column
            ]
            potential_new_rank = fighter_rankings[loser][ranking_column] + 1

            # update all the ranking higher than the loser
            for fighter in fighter_rankings.keys():
                figher_rank_ = fighter_rankings.get(fighter, {"rank": 0})[
                    ranking_column
                ]

                if (figher_rank_ >= potential_new_rank) and (figher_rank_ < winner_rank):
                    fighter_rankings[fighter][ranking_column] += 1

            fighter_rankings[loser][ranking_column] = potential_new_rank
            winner_rank = fighter_rankings.get(winner, {"rank": 0})[ranking_column]
            loser_rank = fighter_rankings.get(loser, {"rank": 0})[ranking_column]

            if verbose:
                print("-------------------")
                print(
                    "After change --> winner name {} --> rank: {} \n loser name {} --> rank: {}".format(
                        winner, winner_rank, loser, loser_rank
                    )
                )
                print("-------------------\n")

            fighter_rankings = dict(
                sorted(
                    fighter_rankings.items(), key=lambda item: item[1][ranking_column]
                )
            )

    # Convert the updated rankings back to a DataFrame
    updated_rankings = pd.DataFrame.from_dict(
        fighter_rankings, orient="index"
    ).reset_index()

    updated_rankings.columns = pd.Index(["Name", "rank", "page_rank"])

    # Adjust the rank numbers to be sequential after changes
    updated_rankings = updated_rankings.sort_values(
        by=["page_rank"], ascending=False
    ).sort_values(by=["rank"])
    
    return updated_rankings

def get_fighters_in_weightclass(
    df: pd.DataFrame, minimum_fights: int = 3
) -> pd.DataFrame:

    _df_winner = (
        df.groupby(["winner", "Weight"])
        .size()
        .reset_index(name="counts")  # type: ignore
        .sort_values(by="counts", ascending=False)
    )
    _df_loser = (
        df.groupby(["losser", "Weight"])
        .size()
        .reset_index(name="counts") # type: ignore
        .sort_values(by="counts", ascending=False)
    )
    _df_winner = _df_winner.rename(columns={"winner": "fighter"})
    _df_loser = _df_loser.rename(columns={"losser": "fighter"})

    # append the loser data to the winner data to get the total number of matches for each fighter
    df_fighter_weight = pd.concat([_df_winner, _df_loser])
    df_fighter_weight = (
        df_fighter_weight.groupby(["fighter", "Weight"]).sum().reset_index()
    )
    df_fighter_weight = df_fighter_weight[df_fighter_weight["counts"] > minimum_fights]
    return df_fighter_weight


# if __name__ == "__main__":
#     from mma_ranking.config import N_YEARS
#     from mma_ranking.ranking.preprocess import load_train_data

#     df = load_train_data()
#     # df["Weight"] = df.apply(lambda x: weight(x.Weight), axis=1)
#     performance_df = fighter_perfomance(df=df, n_years=N_YEARS)
#     print(performance_df.head(3))
