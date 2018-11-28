import pandas as pd
from math import ceil


def compatible(df, i, members):

    if len(members) > 2:
        return False
    SUC  = int(df.loc[[i]]["SUC"])
    SUCL = int(df.loc[[i]]["SUCL"])
    BCL  = int(df.loc[[i]]["BCL"])
    so_far = True
    for index, member in members.iterrows():
        so_far = so_far and (member['SUC'] != SUC) and (member['SUCL'] != SUCL) and (member['BCL'] != BCL)
    return so_far


def bt(df, i, group):
    if i < 0:
        return
    elif group > 23:
        return

    members = df.loc[df['new'] == group]
    if compatible(df, i, members):
        df.at[i, 'new'] = group
        i = i - 1
    elif group < 24:
        group = group + 1
    while i > 0 and group < 24:
        bt(df, i, group)
        members = df.loc[df['new'] == group]
        #if compatible(df, i, members):


def hundred_percent_compatible(student, group):
    SUC = int(student["SUC"])
    SUCL = int(student["SUCL"])
    BCL = int(student["BCL"])
    members = df.loc[df['new'] == group]
    so_far = True
    for index, member in members.iterrows():
        so_far = so_far and (member['SUC'] != SUC) and (member['SUCL'] != SUCL) and (member['BCL'] != BCL)
    return so_far


def nr_solve(df, s, group, group_size):
    visited = set()
    path = []
    final = ceil((s + 1)/group_size)

    path.append(group)
    current_group = group
    visited.add(current_group)

    while (path[-1] <= final) and (len(path) != 0):
        no_viable_groups = False
        viable_students = df.loc[df['new'] == 0]
        students_in_group = []
        chalmers_iterator = viable_students.iterrows()
        (index, student) = next(chalmers_iterator, ('rip', 'rip'))
        while (index != 'rip') and (len(students_in_group) <= 3):

            if hundred_percent_compatible(student, current_group):
                #df.at[index, 'new'] = current_group  # add student to current_group
                students_in_group.append(index)  # add student to local "counter"
                (index, student) = next(chalmers_iterator, ('rip', 'rip'))  # iterate to next student in the list
            if index == 'rip' and group == final and not df.loc[df['new'] == 0].empty:
                no_viable_groups = True

        if no_viable_groups:
            path.pop()
        else:
            path.append(current_group)
            visited
        current_group = path[-1]



df = pd.read_excel('data.xlsx')
df["new"] = 0
df = df.sample(frac=1).reset_index(drop=True)
#bt(df, 68, 1)

nr_solve(df, 68, 1, 3)

# write to a new excel_file
#writer = pd.ExcelWriter('output.xlsx')
#df.to_excel(writer, 'sheet1')
#writer.save()