import pandas as pd
from itertools import combinations


def compatible(df, members, i):
    # groups can only have size of 3
    if len(members) > 2:
        return False
    
    # groups that student i belong to:
    SUC  = int(df.loc[[i]]["SUC"])
    SUCL = int(df.loc[[i]]["SUCL"])
    BCL  = int(df.loc[[i]]["BCL"])

    # current student cannot have any common previous group with any of
    # the members.
    so_far_OK = True
    
    for index in members:
        so_far_OK = so_far_OK and (df.loc[index]['SUC'] != SUC) and (
            df.loc[index]['SUCL'] != SUCL) and (df.loc[index]['BCL'] != BCL)
    return so_far_OK


def bf(df):
    end = len(df.index)
    all_combos = []
    for i in range(0, end):
        group = [i]
        for j in range(i, end):
            if (compatible(df, group, j)):
                group.append(j)
            for k in range(j, end):
                if (compatible(df, group, k)):
                    group.append(k)
                all_combos.append(group)
    return all_combos


def bt(allah):
    for i in range

df = pd.read_excel('data.xlsx')
#df = df.sample(frac=1).reset_index(drop=True)  # shuffles the data
allah = bf(df)

