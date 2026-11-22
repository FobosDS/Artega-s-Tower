from Settings import sprites_folder
#enemy sprites dictionary
#f - front, s - side, b - back
ESD ={
    "ghoul":{
        #front
        "f_stand":
        "Assets/Sprites/Enemies/Ghoul/gh_front_stand.png",
        "f_walk1":
        "Assets/Sprites/Enemies/Ghoul/gh_front_walk1.png",
        "f_walk2":
        "Assets/Sprites/Enemies/Ghoul/gh_front_walk2.png",
        "f_attack":
        "Assets/Sprites/Enemies/Ghoul/gh_front_attack.png",
        "f_throw":
        "Assets/Sprites/Enemies/Ghoul/gh_front_throw.png",
        "f_dash1":
        "Assets/Sprites/Enemies/Ghoul/gh_front_dash1.png",
        "f_dash2":
        "Assets/Sprites/Enemies/Ghoul/gh_front_dash2.png",

        #side
        "s_stand":
        "Assets/Sprites/Enemies/Ghoul/gh_side_walk1.png",
        "s_walk1":
        "Assets/Sprites/Enemies/Ghoul/gh_side_walk1.png",
        "s_walk2":
        "Assets/Sprites/Enemies/Ghoul/gh_side_walk2.png",
        "s_attack":
        "Assets/Sprites/Enemies/Ghoul/gh_side_attack.png",
        "s_throw":
        "Assets/Sprites/Enemies/Ghoul/gh_side_throw.png",
        "s_dash1":
        "Assets/Sprites/Enemies/Ghoul/gh_side_dash1.png",
        "s_dash2":
        "Assets/Sprites/Enemies/Ghoul/gh_side_dash2.png",

        #back
        "b_stand":
        "Assets/Sprites/Enemies/Ghoul/gh_back_stand.png",
        "b_walk1":
        "Assets/Sprites/Enemies/Ghoul/gh_back_walk1.png",
        "b_walk2":
        "Assets/Sprites/Enemies/Ghoul/gh_back_walk2.png",
        "b_attack":
        "Assets/Sprites/Enemies/Ghoul/gh_back_attack.png",
        "b_throw":
        "Assets/Sprites/Enemies/Ghoul/gh_back_throw.png",
        "b_dash1":
        "Assets/Sprites/Enemies/Ghoul/gh_back_dash1.png",
        "b_dash2":
        "Assets/Sprites/Enemies/Ghoul/gh_back_dash2.png",

        #hit and death
        "hit":
        "Assets/Sprites/Enemies/Ghoul/gh_hit.png",
        "death":
        "Assets/Sprites/Enemies/Ghoul/gh_death.png",

        #projectile
        "proj":
        "Assets/Sprites/Enemies/Projectiles/poison_pr.png"
    },

    "gargoyle":{
        #front
        "f_stand":
        "Assets/Sprites/Enemies/Gargoyle/ga_front2.png",
        "f_move1":
        "Assets/Sprites/Enemies/Gargoyle/ga_front1.png",
        "f_move2":
        "Assets/Sprites/Enemies/Gargoyle/ga_front2.png",
        "f_attack":
        "Assets/Sprites/Enemies/Gargoyle/ga_attack1.png",
        "f_echo":
        "Assets/Sprites/Enemies/Gargoyle/ga_echo-wave.png",
        "f_dive":
        "Assets/Sprites/Enemies/Gargoyle/ga_attack2.png",

        #side
        "s_stand":
        "Assets/Sprites/Enemies/Gargoyle/ga_side2.png",
        "s_move1":
        "Assets/Sprites/Enemies/Gargoyle/ga_side1.png",
        "s_move2":
        "Assets/Sprites/Enemies/Gargoyle/ga_side2.png",
        "s_attack":
        "Assets/Sprites/Enemies/Gargoyle/ga_side2.png",
        "s_echo":
        "Assets/Sprites/Enemies/Gargoyle/ga_side_echo-wave.png",
        "s_dive":
        "Assets/Sprites/Enemies/Gargoyle/ga_side1.png",

        #back
        "b_stand":
        "Assets/Sprites/Enemies/Gargoyle/ga_back2.png",
        "b_move1":
        "Assets/Sprites/Enemies/Gargoyle/ga_back1.png",
        "b_move2":
        "Assets/Sprites/Enemies/Gargoyle/ga_back2.png",
        "b_attack":
        "Assets/Sprites/Enemies/Gargoyle/ga_back2.png",
        "b_echo":
        "Assets/Sprites/Enemies/Gargoyle/ga_back1.png",
        "b_dive":
        "Assets/Sprites/Enemies/Gargoyle/ga_back1.png",

        #hit and death
        "hit":
        "Assets/Sprites/Enemies/Gargoyle/ga_hit.png",
        "statue":
        "Assets/Sprites/Enemies/Gargoyle/ga_statue.png",
        "fall":
        "Assets/Sprites/Enemies/Gargoyle/ga_fall_attack.png",
        "death":
        "Assets/Sprites/Enemies/Gargoyle/ga_death.png",

        #projectile
        "proj":
        "Assets/Sprites/Enemies/Projectiles/paralich_pr.png"    
    }
}

#interactive sprites dictionary
ISD = {
    "merchant":"Assets/Sprites/Levels/Interactive/merchant.png",
    "chest":{
        "close":"Assets/Sprites/Levels/Interactive/Chests/chest_close.png",
        "open":"Assets/Sprites/Levels/Interactive/Chests/chest_open.png"
    },
    "rare_chest":{
        "close":"Assets/Sprites/Levels/Interactive/Chests/rare_chest_close.png",
        "open":"Assets/Sprites/Levels/Interactive/Chests/rare_chest_open.png"
    },
    "altar":"Assets/Sprites/Levels/Interactive/altar.png"
}

#decorations sprites dictionary
DSD = {
    "barrel":"Assets/Sprites/Levels/Decorations/barrel.png",
    "box":"Assets/Sprites/Levels/Decorations/box.png",
    "cell_break":"Assets/Sprites/Levels/Decorations/cell_break.png",
    "cell_ghoul":"Assets/Sprites/Levels/Decorations/cell_ghoul.png",
    "cell":"Assets/Sprites/Levels/Decorations/cell.png",
    "chains":"Assets/Sprites/Levels/Decorations/chains.png",
    "armor":"Assets/Sprites/Levels/Decorations/armor.png",
    "brazier":"Assets/Sprites/Levels/Decorations/brazier.png",
    "candel1":"Assets/Sprites/Levels/Decorations/candel1.png",
    "candel2":"Assets/Sprites/Levels/Decorations/candel2.png",
    "candel3":"Assets/Sprites/Levels/Decorations/candel3.png",
    "candelabrum":"Assets/Sprites/Levels/Decorations/candelabrum.png",
    "chair":"Assets/Sprites/Levels/Decorations/chair.png",
    "column_peak":"Assets/Sprites/Levels/Decorations/column_peak.png",
    "column":"Assets/Sprites/Levels/Decorations/column.png",
    "grave1":"Assets/Sprites/Levels/Decorations/grave1.png",
    "grave2":"Assets/Sprites/Levels/Decorations/grave2.png",
    "grave3":"Assets/Sprites/Levels/Decorations/grave3.png",
    "king":"Assets/Sprites/Levels/Decorations/king.png",
    "table":"Assets/Sprites/Levels/Decorations/table.png",
    "torch":"Assets/Sprites/Levels/Decorations/torch.png",
    "vase_brown":"Assets/Sprites/Levels/Decorations/vase_brown.png",
    "vase_gray":"Assets/Sprites/Levels/Decorations/vase_gray.png",
    "vase_green":"Assets/Sprites/Levels/Decorations/vase_green.png"
}

floor_decorations = {
    1:["barrel", "box", "cell_break", "cell_ghoul", "cell", "chains", "table", "brazier"],
    2:["barrel", "box", "cell", "chains", "brazier", "grave1", "grave2", "grave3", "vase_brown", "candel1", "candel2", "candel3", "torch"],
    3:["barrel", "vase_green", "candel1", "candel2", "candel3", "candelabrum", "chair", "table"],
    4:["barrel", "vase_gray", "candelabrum", "chair", "table", "torch", "column"],
    5:["column_peak", "brazier", "torch", "candelabrum"]
}

#weapon sprites dictionary
WSD = {
    "sword_attack":[
        sprites_folder + "sword/" + "stand.png",
        sprites_folder + "sword/" + "attack1.png",
        sprites_folder + "sword/" + "attack2.png",
        sprites_folder + "sword/" + "attack3.png"
    ],
    "sword_block": sprites_folder + "sword/" + "block.png"
}

#shelfs dictionary
SH = [
    "Assets/Sprites/Levels/Walls/shelfs/shelf1.png",
    "Assets/Sprites/Levels/Walls/shelfs/shelf2.png",
    "Assets/Sprites/Levels/Walls/shelfs/shelf3.png",
    "Assets/Sprites/Levels/Walls/shelfs/shelf4.png",
    "Assets/Sprites/Levels/Walls/shelfs/shelf5.png",
    "Assets/Sprites/Levels/Walls/shelfs/shelf6.png"
]

#walls textures dictionary
WTD = {
    "H": SH[2],
    **{f"H{i}": path for i, path in enumerate(SH)},
    "E":"Assets/Sprites/Levels/Walls/stairs.png",
    "J":"Assets/Sprites/Levels/Walls/barrier.png",
    "W": "Assets/Sprites/Levels/Walls/1lv_dungeon/1w_simple1.png"
}

floor_walls = {
    #dungeon
    1:[
        ("simple1", 35, "Assets/Sprites/Levels/Walls/1lv_dungeon/1w_simple1.png"),
        ("simple2", 35, "Assets/Sprites/Levels/Walls/1lv_dungeon/1w_simple2.png"),
        ("torch", 14, "Assets/Sprites/Levels/Walls/1lv_dungeon/1w_torch.png"),
        ("grate", 11, "Assets/Sprites/Levels/Walls/1lv_dungeon/1w_grate.png"),
        ("ghoul_grate", 5, "Assets/Sprites/Levels/Walls/1lv_dungeon/1w_ghoul_grate.png")
    ],

    #mausoleum
    2:[
        ("simple", 60, "Assets/Sprites/Levels/Walls/2lv_mausoleum/2w_simple.png"),
        ("decor1", 16, "Assets/Sprites/Levels/Walls/2lv_mausoleum/2w_decor2.png"),
        ("decor2", 16, "Assets/Sprites/Levels/Walls/2lv_mausoleum/2w_decor2.png"),
        ("statue", 8, "Assets/Sprites/Levels/Walls/2lv_mausoleum/2w_statue.png")
    ],

    #archive
    3:[
        ("simple1", 16, "Assets/Sprites/Levels/Walls/3lv_archive/3v_simple1.png"),
        ("simple2", 16, "Assets/Sprites/Levels/Walls/3lv_archive/3v_simple2.png"),
        ("simple3", 16, "Assets/Sprites/Levels/Walls/3lv_archive/3v_simple3.png"),
        ("simple4", 16, "Assets/Sprites/Levels/Walls/3lv_archive/3v_simple4.png"),
        ("simple5", 16, "Assets/Sprites/Levels/Walls/3lv_archive/3v_simple5.png"),
        ("simple6", 16, "Assets/Sprites/Levels/Walls/3lv_archive/3v_simple6.png"),
        ("dark", 4, "Assets/Sprites/Levels/Walls/3lv_archive/3v_simple7.png")
    ],

    #hall
    4:[
        ("simple", 40, "Assets/Sprites/Levels/Walls/4lv_hall/4w_simple.png"),
        ("column1", 20, "Assets/Sprites/Levels/Walls/4lv_hall/4w_column1.png"),
        ("column2", 6, "Assets/Sprites/Levels/Walls/4lv_hall/4w_column2.png"),
        ("brazier", 12, "Assets/Sprites/Levels/Walls/4lv_hall/4w_brazier.png"),
        ("statue", 10, "Assets/Sprites/Levels/Walls/4lv_hall/4w_statue.png"),
        ("flag", 8, "Assets/Sprites/Levels/Walls/4lv_hall/4w_flag.png"),
        ("shield", 4, "Assets/Sprites/Levels/Walls/4lv_hall/4w_shield.png")
    ],

    #peak
    5:[
        ("glass1", 30, "Assets/Sprites/Levels/Walls/5lv_peak/5w_glass1.png"),
        ("glass2", 60, "Assets/Sprites/Levels/Walls/5lv_peak/5w_glass2.png"),
        ("glass4", 10, "Assets/Sprites/Levels/Walls/5lv_peak/5w_glass4.png")
    ]
}
floor_walls_default = floor_walls[1]

#rings dictionary
RD = {
    "ring_fugitive":{
        "name":"Кольцо удачливого беглеца",
        "sprite":"Assets/Sprites/Rings/lucky_fugitive.png",
        "desc":"""
        Некогда принадлежало юркому войну, сбежавшему из темниц башни, но попавшемуся Артеге...
        Его яркий серебряный свет вселяет в вас уверенность в свои силы, увеличивая скорость
        передвижения и уменьшая затраты выносливости!
        """
    },

    "ring_merchant":{
        "name":"Кольцо алчного торговца",
        "sprite":"Assets/Sprites/Rings/greedy_merchant.png",
        "desc":"""
        Однажды один из множества торговцев башни решил поторговаться с самим Артегой и
        благодаря своей смекалке продал ему яд под видом зелья магической мощи...Но яд
        не убил чародея, а судьба торговца осталась неизвестной. Медный отблеск кольца
        напоминает о находчивости великого торговца, позволяя покупать товары дешевле, а также
        находить больше предметов!
        """
    },

    "ring_dragon":{
        "name":"Кольцо древнего дракона",
        "sprite":"Assets/Sprites/Rings/ancient_dragon.png",
        "desc":"""
        Множество трупов различных существ лежит в мавзолее башни, но один из них уникальный - это
        бездыханное тело древнего дракона, убитого Артегой со своим магистром еще в молодости...
        Кольцо служит напоминанием невероятной живучести темного змея, а вечный холод его
        титановой шинки помогает организму противостоять ядам и токсинам!
        """
    },

    "ring_dreamer":{
        "name":"Кольцо непутевого мечтателя",
        "sprite":"Assets/Sprites/Rings/gullible_dreamer.png",
        "desc":"""
        Артега с помощью темной магии научился превращать души существ в различные предметы,
        например, в украшения...Бедная душа глупого мальчишки мечтавшего о невинной любви теперь
        вечно будет томиться в этом красивом кольце, чьи золотые переливы увеличивают
        стойкость владельца и мощь зелий жизни!
        """
    },

    "ring_genius":{
        "name":"Кольцо безумного гения",
        "sprite":"Assets/Sprites/Rings/mad_genius.png",
        "desc":"""
        Некоторые людя желают знаний, желают их до безумия...Древний маг Тьерри, один из
        основателей темной магии, был таким человеком. В знак уважения Артега создал из
        его души, найденной в стенах старой башни, свое любимое кольцо, отлитое из
        синего золота, чей витиеватый узор увеливает длительность зачарований и 
        улучшает лечебную мощь зелий жизни, но делает организм более уязвимым для ядов!
        """
    },

    "ring_murderer":{
        "name":"Кольцо кровожадного убийцы",
        "sprite":"Assets/Sprites/Rings/bloody_murderer.png",
        "desc":"""
        Люди по своей природе жестоки... Жесток и Артега, и его подчиненные, и его враги. Но в этом плане
        всех и каждого превзошел один безумный солдат, прозванный "Берсерком". Он желал мести, для 
        осуществления которой ему была нужна великая сила и отвага, которые он и попросил у чародея.
        В конце концов, Симон стал настолько кровожадной и сильной тварью, что с необычайной легкостью
        перебил всех своих товарищей, поставив в истории самого первого похода на башню точку...Следы
        запекшейся крови на этом ржавом чугунном кольце наполняют вашу душу первобытной яростью и 
        жестокостью, позволяя вам иногда входить в состояние берсерка засчет потери почти всей крови.
        """
    },

    "ring_warrior":{
        "name":"Кольцо честного воина",
        "sprite":"Assets/Sprites/Rings/honest_warrior.png",
        "desc":"""
        Оскар нашел это кольцо в мраморном зале, огромной приемной для различных гостей
        мага и его подчиненных, резко контрастирующим с мрачными комнатами остальной
        части башни. На кольце выгравированно: "Оскар, великий немой воин, бросивший вызов
        владыке темных искусств Артеге"...Оскар не понимает этих надписей, но уверен, что это
        очень важные для него слова. Смесь страха и отваги, передаваемой через приятное
        тепло железа кольца, придает вам сил для продолжения пути, увеличивая вашу стойкость,
        выносливость и силу!
        """
    },

    "ring_aristocrat":{
        "name":"Кольцо трусливого аристократа",
        "sprite":"Assets/Sprites/Rings/cowardly_aristocrat.png",
        "desc":"""
        Прежний король был трусом по своей природе, с самого детства боясь всего: мух, мышей, людей,
        темноты, крестьянских бунтов, стражей и, конечно, Артеги...Говоря на чистоту, его поход на башню был 
        обречен с самого начала, ведь он хотел не победы, а исполнения своего желания. Король больше
        всего на свете боялся смерти и тайн загробного мира, поэтому и пожелал навечно остаться на
        престоле. И его желание исполнилось...Игра света на гранях этого рубинового кольца
        заставляет пережить все худшие страхи короля, улучшая возможность отбиватья от монстров засчет
        повышенной скорости и дальности атаки!
        """
    }
}

floor_names = {
    1:"Первый этаж: Темница",
    2:"Второй этаж: Мавзолей Дракона",
    3:"Третий этаж: Проклятый Архив",
    4:"Четвертый этаж: Мраморный Зал",
    5:"Последний этаж: Пик Башни"
}

sfx = {

}

music = {
   "Dungeon_ND":"Assets/Music/Artega Tower Dungeon no drums.mp3",
   "Dungeon":"Assets/Music/Artega Tower Dungeon.mp3",
   "Mausoleum_ND":"Assets/Music/Artega Tower Mausoleum No Drums.mp3",
   "Mausoleum":"Assets/Music/Artega Tower Mausoleum.mp3",
   "Archive1":"Assets/Music/Artega Tower Archive.mp3",
   "Archive2":"Assets/Music/Artega Tower Archive2.mp3",
   "Marble_Hall":"Assets/Music/Artega Tower Marble Hall.mp3",
   "We_Not_Lost":"Assets/Music/Artega Tower We Not Lost.mp3",
   "Artega":"Assets/Music/Artega Artega.mp3",
   "Artega2":"Assets/Music/Artega Tower End Soon.mp3",
   "Menu":"Assets/Music/Artega Tower Menu.mp3",
   "Death":"Assets/Music/Artega Tower Death.mp3",
   "Win":"Assets/Music/Artega Tower Win.mp3"
}

floor_music = {
    0:["Assets/Music/Artega Tower Menu.mp3"],
    
    1:[
        "Assets/Music/Artega Tower Dungeon no drums.mp3",
        "Assets/Music/Artega Tower Dungeon.mp3"
    ],

    2:[
        "Assets/Music/Artega Tower Mausoleum No Drums.mp3",
        "Assets/Music/Artega Tower Mausoleum.mp3"
    ],

    3:[
        "Assets/Music/Artega Tower Archive.mp3",
        "Assets/Music/Artega Tower Archive2.mp3"
    ],

    4:[
        "Assets/Music/Artega Tower Marble Hall.mp3",
        "Assets/Music/Artega Tower We Not Lost.mp3"
    ]
}