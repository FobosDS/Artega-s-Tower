drawed_maps = {
    1:[
    "ONNNNOOOOOOO",
    "O...SCs.E.HO",
    "O.P.......HO",
    "O...UOTOO..N",
    "OD..OD.HH..N",
    "U...N......O",
    "O.H.1..m.O.N",
    "O........U.O",
    "U.NNNTN..O.T",
    "O.D..D...O.O",
    "O........J.O",
    "OTNOTOUTNNNO",
    ],

    2:[
    "OOOOOOOOOOO.............OOOOOOOOOOO.............",
    "OHDHDHOHH..OO.........OOHHH....HHHO.............",
    "O.....O...D..OO.....OOD.....D.....O.............",
    "O..P.DOD....1.DOOOOOD.............O.............",
    "OD....O........HHHO...1......1...DO.............",
    "OOO...OOOOOD......O...............O.............",
    "OHHO..DOF.HOD...D..O....D.......DOO.............",
    "O..O....O..HO.2.....J......1....OHO.............",
    "O.1OH...O1..J........O.........J..O.............",
    "O..OH..DO...HOHHG.C..HO.1......J.DO.............",
    "OG......O...HOOOOOOOOOO...D..DO...O.............",
    ".OO.....O..1HO.2......OOOOOOOO...O..............",
    ".O......O...OO..OOJOOFOHHO.......O..............",
    "..O.......DOHO..O...OOO..Ou....HO...............",
    "..OD.1.1.OOH.O.DO...OEO1.O.....HO...............",
    "...OH...HOH..O.OD...OJO..O....HO................",
    "...OH...HO.1DO.O......O..O.o..HO................",
    "..OCOD..OH...O.O.2.2..O..O.....DO...............",
    "..O.O...OH.HHO.O.....OO..OOOO.OOO...............",
    ".O..OJJJOH...O.OOOOOODOH........FO..............",
    ".O.OH..GO1...O........OH..1......O..............",
    "O..OH..OG..D.COOOOOO...OH........GO.............",
    "O1.OH..OG.....OD..HHO...OH.....1.GO.............",
    "O..O..DOOOO...O.m..1OO...OOOOOOOOOO.............",
    "O.....O..HHJ........OHO..J..D..HHHO.............",
    "OF.O.DO.1...J.O.....J.HO.J..1.....O.............",
    "OOOO.OO......O...1..O..HOJ....D...O.............",
    "OH....D....2.O.D..HHO...O......1.DO.............",
    "OH......S....OGOOOOOH..1..D......FO.............",
    "OH.D........DOO.....OOD.O...1D....O.............",
    "OH...D.D..HOO.........OOOD.....HHHO.............",
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