import pandas as pd
from itertools import combinations
from math import floor
from itertools import cycle
import pickle


def compatible(df, members, i):
    
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

    potential_members = members + [i]
    if len(potential_members) == 3:
        tracks = set()
        sexes = set()
        for i in potential_members:
            tracks.add(str(df.loc[i]["Track"]))
            sexes.add(str(df.loc[i]["sex"]))
        if len(tracks) == 1 or len(sexes) == 1:
            return False

    return so_far_OK


def brutus_deluxe(df):
    end = len(df.index)
    all_combos = []
    for i in range(0, end):
        for j in range(i, end):
            if (compatible(df, [i], j)):
                for k in range(j, end):
                    if (compatible(df, [i, j], k)):
                        all_combos.append([i, j, k])
    with open('all_combos.txt', 'wb') as fp:
        pickle.dump(all_combos, fp)
    return all_combos


def find_solution_for_the_mexican(df, sol):
    flat_sol = [item for sublist in sol for item in sublist]
    mexican = -1
    for i in range(0, len(df.index)):
        if i not in flat_sol:
            mexican = i  #found the mexican
 
    for index, group in enumerate(sol):
        if compatible(df, group, mexican):
            sol[index] = (group + [mexican])
            break
    print(sol)
    return sol
    
    
def find_disjoint_set(df, candidates):
    nr_of_students = len(df.index)
    nr_of_groups = floor(len(df.index) / 3)
    students_candidates = []
    for i in range(0, nr_of_students):
        students_candidates.append([])
        for candidate in candidates:
            if i in candidate:
                students_candidates[i].append(candidate)

    visited = set()
    solution = []
    while len(solution) != nr_of_groups:
        students_so_far = []
        solution = []
        for i in range(0, nr_of_students):
            
            for candidate in students_candidates[i]:
                if tuple(candidate) not in visited:
                    if not any(c in students_so_far for c in candidate):
                        students_so_far = students_so_far + candidate
                        solution.append(candidate)
                        visited.add(tuple(candidate))
        print("solution found of size: ", len(solution))

    final_solution = find_solution_for_the_mexican(df, solution)
    return final_solution

def produce_groups(df, solution):
    df['new'] = 0
    index = 1
    for group in solution:
        for student in group:
            df.at[student, 'new'] = index
        index += 1
    
    writer = pd.ExcelWriter('fresh_juice.xlsx')
    df.to_excel(writer, 'sheet1')
    writer.save()

df = pd.read_excel('data.xlsx')
allah = brutus_deluxe(df)

with open('all_combos.txt', 'rb') as fp:
    allah = pickle.load(fp)

sol = find_disjoint_set(df, allah)
produce_groups(df, sol)
