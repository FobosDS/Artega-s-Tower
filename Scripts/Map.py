drawed_maps = {
    1:[
    "WWWWWWWWWWWW",
    "WGFLSCuWEWHW",
    "W.........HW",
    "W.P.WWWWW..W",
    "WD..WD.HH..W",
    "W...W......W",
    "W.H....p.W.W",
    "W........W.W",
    "W.WWWWW..W.W",
    "W.D..D...W.W",
    "W......1.J.W",
    "WWWWWWWWWWWW",
    ],

    2:[
    "WWWWWWWWWWWW",
    "W...SCu.E.HW",
    "W.P.......HW",
    "W...WWWWW..W",
    "WD..WD.HH..W",
    "W...W......W",
    "W.H....p.W.W",
    "W....1...W.W",
    "W.WWWWW..W.W",
    "W.D..D...W.W",
    "W........J.W",
    "WWWWWWWWWWWW",
    ],

    3:[
    "WWWWWWWWWWWW",
    "W...SCu.E.HW",
    "W.P.......HW",
    "W...WWWWW..W",
    "WD..WD.HH..W",
    "W...W......W",
    "W.H.2..p.W.W",
    "W........W.W",
    "W.WWWWW..W.W",
    "W.D..D...W.W",
    "W........J.W",
    "WWWWWWWWWWWW",
    ],

    4:[
    "WWWWWWWWWWWW",
    "W...SCu.E.HW",
    "W.P.......HW",
    "W...WWWWW..W",
    "WD..WD.HH..W",
    "W...W......W",
    "W.H..3.p.W.W",
    "W........W.W",
    "W.WWWWW..W.W",
    "W.D..D...W.W",
    "W........J.W",
    "WWWWWWWWWWWW",
    ],

    5:[
    "WWWWWWWWWWWW",
    "W...SCR.E.HW",
    "W.P.......HW",
    "W...WWWWW..W",
    "WD..WD.HH..W",
    "W...W......W",
    "W.H..1.p.W.W",
    "W........W.W",
    "W.WWWWW..W.W",
    "W.D..D...W.W",
    "W........J.W",
    "WWWWWWWWWWWW",
    ]
}

drawed_map = list(drawed_maps[1])

def set_floor_map(floor):
    global drawed_map
    new_map = drawed_maps.get(floor) or drawed_maps[1]
    drawed_map.clear()
    drawed_map.extend(new_map)