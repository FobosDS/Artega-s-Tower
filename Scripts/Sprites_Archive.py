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
    "pedestal": sprites_folder + "pedestal.png"
}

#static sprites dictionary
SSD = {
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

#walls textures dictionary
WTD = {
    #dungeon
    "R":"Assets/Sprites/Levels/Walls/1lv_dungeon/1w_grate.png",
    "L":"Assets/Sprites/Levels/Walls/1lv_dungeon/1w_ghoul_grate.png",
    "N":"Assets/Sprites/Levels/Walls/1lv_dungeon/1w_simple1.png",
    "H":"Assets/Sprites/Levels/Walls/1lv_dungeon/1w_simple2.png",
    "T":"Assets/Sprites/Levels/Walls/1lv_dungeon/1w_torch.png",

    #mausoleum
    "I":"Assets/Sprites/Levels/Walls/2lv_mausoleum/2w_simple.png",
    "D":"Assets/Sprites/Levels/Walls/2lv_mausoleum/2w_decor1.png",
    "C":"Assets/Sprites/Levels/Walls/2lv_mausoleum/2w_decor2.png",
    "S":"Assets/Sprites/Levels/Walls/2lv_mausoleum/2w_statue.png"
}