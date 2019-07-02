﻿"""
TESTS is a dict with all you tests.
Keys for this will be categories' names.
Each test is dict with
    "input" -- input data for user function
    "answer" -- your right answer
    "explanation" -- not necessary key, it's using for additional info in animation.
"""

from string import ascii_uppercase as au
from random import sample, randint, choice
from my_solution import hexagonal_islands


def hexagonal_islands_make_random_tests(num):

    all_hexes = {c+str(r) for c in au[:12] for r in range(1, 10)}

    def adjacent_hexes(tgt_hex):
        col, row = tgt_hex[0], int(tgt_hex[1])
        col_idx = au.index(col)
        u_row = row - (1 - col_idx % 2)
        b_row = row + col_idx % 2
        n = col+str(row-1)
        s = col+str(row+1)
        nw = au[col_idx-1]+str(u_row)
        sw = au[col_idx-1]+str(b_row)
        ne = au[col_idx+1]+str(u_row)
        se = au[col_idx+1]+str(b_row)
        return set(map(lambda h: h[0]+str(h[1]) if h in all_hexes else None,
            (n, ne, se, s, sw, nw)))

    def make_island(rest_hexes):
        next_hexes = {choice(list(rest_hexes))}
        done_hexes = next_hexes
        while next_hexes:
            search_hexes = next_hexes
            next_hexes = set()
            for sx in search_hexes:
                adj_hexes = (adjacent_hexes(sx)-{None}) & rest_hexes
                next_hexes |= set(sample(adj_hexes, 
                                    randint(0, min(3, len(adj_hexes)))))
            next_hexes -= done_hexes
            done_hexes |= next_hexes
        adj_sea_hexes = set()
        shore_hexes = set()
        for dx in done_hexes:
            adj_hexes = adjacent_hexes(dx)
            adj_sea_hexes |= adj_hexes - {None} - done_hexes
            if adj_hexes - done_hexes:
                shore_hexes.add(dx)
        return done_hexes, shore_hexes, adj_sea_hexes

    def check_hole(shore_hexes):
        rest_hexes = set(shore_hexes)
        while rest_hexes:
            start_hex = rest_hexes.pop()
            done_hexes = {start_hex}
            next_hexes = {start_hex}
            sea = False
            while next_hexes:
                search_hexes = next_hexes
                next_hexes = set()
                for s in search_hexes:
                    adj_hexes = adjacent_hexes(s)
                    if None in adj_hexes:
                        sea = True
                    next_hexes |= (adjacent_hexes(s)-{None}) & shore_hexes
                next_hexes -= done_hexes
                done_hexes |= next_hexes
            if not sea and len(shore_hexes - done_hexes) > 0:
                return False
            rest_hexes -= done_hexes
        return True

    random_tests = []
    for _ in range(num):
        rest_hexes = set(all_hexes)
        lands = []
        for _ in range(randint(1, 10)):
            while True:
                land, shore, adj_sea = make_island(rest_hexes)
                if check_hole(adj_sea):
                    rest_hexes -= land | adj_sea
                    lands += list(shore)
                    break
            if not rest_hexes:
                break
        answer, inland_hexes = hexagonal_islands(set(lands))
        random_tests.append({'input': lands,
                             'answer': answer,
                             'explanation': list(inland_hexes)})
    return random_tests


TESTS = {
    "Randoms": hexagonal_islands_make_random_tests(10),
    "Basics": [
        {
            'input': ['C5', 'E5', 'F4', 'F5', 'H4',
                        'H5','I4', 'I6', 'J4', 'J5'],
            'answer': [1, 3, 7],
            'explanation': ['I5'],
        },
        {
            'input': ['A1', 'A2', 'A3', 'A4', 'B1', 'B4', 'C2', 'C5',
                        'D2','D3', 'D4', 'D5',
                        'H6', 'H7', 'H8', 'I6', 'I9', 'J5', 'J9',
                        'K6', 'K9', 'L6', 'L7', 'L8'],
            'answer': [16, 19],
            'explanation': ['B2', 'B3', 'C3', 'C4',
                            'I7', 'I8', 'J6', 'J7', 'J8', 'K7', 'K8'],
        },
    ],
}