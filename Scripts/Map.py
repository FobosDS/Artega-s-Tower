perm_map = [
    
]

drawed_maps = {
    1:[
    "ONNNNOOOOOOO",
    "O...SCtFG.BO",
    "O.P.......HO",
    "O...UOTOO..N",
    "OD..OD.II..N",
    "U...N......O",
    "O.L....o.O.N",
    "O........U.O",
    "U.NNNTN..O.T",
    "O.D..D...O.O",
    "O........J.O",
    "OTNOTOUTNNNO",
    ],

    2:[
    "OOOOOOOOOOO.............OOOOOOOOOOO.............",
    "OADADAOAA..OO.........OOAAA....AAAO.............",
    "O.....O...D..OO.....OOD.....D.....O.............",
    "O..P.DOD....1.DOOOOOD.............O.............",
    "OD....O........AAAO...1......1...DO.............",
    "OOO...OOOOOD......O...............O.............",
    "OAAO..DOF.AOD...D..O....D.......DOO.............",
    "O..O....O..AO.2.....J......1....OAO.............",
    "O.1OA...O1..J........O.........J..O.............",
    "O..OA..DO...AOAAG.C..AO.1......J.DO.............",
    "OG......O...AOOOOOOOOOO...D..DO...O.............",
    ".OO.....O..1AO.2......OOOOOOOO...O..............",
    ".O......O...OO..OOJOOFOAAO.......O..............",
    "..O.......DOAO..O...OOO..Ou....AO...............",
    "..OD.1.1.OOA.O.DO...OEO1.O.....AO...............",
    "...OA...AOA..O.OD...OJO..O....AO................",
    "...OA...AO.1DO.O......O..O.o..AO................",
    "..OCOD..OA...O.O.2.2..O..O.....DO...............",
    "..O.O...OA.AAO.O.....OO..OOOO.OOO...............",
    ".O..OJJJOA...O.OOOOOODOA........FO..............",
    ".O.OA..GO1...O........OA..1......O..............",
    "O..OA..OG..D.COOOOOO...OA........GO.............",
    "O1.OA..OG.....OD..AAO...OA.....1.GO.............",
    "O..O..DOOOO...O.m..1OO...OOOOOOOOOO.............",
    "O.....O..AAJ........OAO..J..D..AAAO.............",
    "OF.O.DO.1...J.O.....J.AO.J..1.....O.............",
    "OOOO.OO......O...1..O..AOJ....D...O.............",
    "OA....D....2.O.D..AAO...O......1.DO.............",
    "OA......S....OGOOOOOA..1..D......FO.............",
    "OA.D........DOO.....OOD.O...1D....O.............",
    "OA...D.D..AOO.........OOOD.....AAAO.............",
    "OOOOOOOOOOO.............OOOOOOOOOOO.............",
    ],

    3:[
    ],

    4:[
    ],

    5:[
    ]
}

drawed_map = list(drawed_maps[1])

def set_floor_map(floor):
    global drawed_map
    new_map = drawed_maps.get(floor) or drawed_maps[1]
    drawed_map.clear()
    drawed_map.extend(new_map)
