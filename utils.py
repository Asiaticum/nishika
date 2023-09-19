import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_arrangement(layout):
    """
    Get the arrangement details based on the given layout.

    Parameters:
    - layout: str or any
        The layout string or object.

    Returns:
    - arrangement: str
        The corresponding arrangement based on the layout.
    - num_rooms: int
        The number of rooms.
    - service_room: int
        Indicator for the presence of a service room (1 if present, 0 otherwise).
    - kitchen: int
        Indicator for the presence of a kitchen (1 if present, 0 otherwise).
    """
    arrangements = {
        "ＬＤＫ": "LDK",
        "ＬＤ": "LDK",
        "Ｌ": "LDK",
        "ＤＫ": "DK",
        "ＬＫ": "DK",
        "Ｄ": "DK",
        "Ｋ": "K",
        "Ｒ": "R",
    }
    num_rooms = 1
    service_room = 0
    kitchen = 0
    if isinstance(layout, str):
        # 一文字目が数字の場合
        if layout[0].isdigit():
            # 最初の一文字と、"＋"以降の文字を削除
            arrangement_type = layout[1:].split("＋")[0]
            arrangement = arrangements[arrangement_type]
            # 部屋数を抽出
            num_rooms = int(layout[0])
            if "Ｓ" in layout:
                service_room = 1
            if "＋Ｋ" in layout:
                kitchen = 1
        else:
            arrangement = layout
    else:
        arrangement = layout
    return arrangement, num_rooms, service_room, kitchen


def convert_era_to_year(era_year):
    # if era_year is nan, return nan
    if era_year != era_year:
        return era_year

    # 元号と対応する西暦の年を辞書で定義します
    era_dict = {"昭和": 1926, "平成": 1989, "令和": 2019}

    # 元号と西暦の年を分割します
    era = era_year[:2]
    year = int(era_year[2:].split("年")[0])

    # 西暦への変換を行います
    start_year = era_dict[era]
    return start_year + year - 1


def plot_feature_and_price(df, feature):
    # 用途の各要素における取引価格（総額）_logの分布を箱ひげ図で表示、nanはその他に分類
    plt.figure(figsize=(20, 10))
    df_tmp = df.fillna("NAN").copy()
    index = (
        df_tmp.groupby(feature)
        .median()
        .sort_values("取引価格（総額）_log", ascending=False)
        .reset_index()[feature]
        .unique()
    )
    sns.boxplot(x=feature, y="取引価格（総額）_log", data=df_tmp, order=index)
    # x軸の各値を変更
    plt.xticks(
        np.arange(len(df_tmp[feature].unique())),
        [x + str(df_tmp[df_tmp[feature] == x].shape[0]) for x in index],
    )
    # x軸のフォントを大きくする
    plt.xticks(fontsize=20)
    # 横軸の値を回転
    plt.xticks(rotation=90)
    # 各要素のデータ数を出力
    for x in index:
        print(
            x,
            df_tmp[df_tmp[feature] == x].shape[0],
            np.median(df_tmp[df_tmp[feature] == x]["取引価格（総額）_log"]),
        )
    print(df_tmp[feature].unique())
    plt.show()


if __name__ == "__main__":
    pass
