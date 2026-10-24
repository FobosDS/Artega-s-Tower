from Settings import sprites_folder

#entity sprites dictionary
ESD ={
    "ghoul": 
        (660, 460, sprites_folder + "ghoul.png", 0.8, 30),
    "artega_states":{
            "stand":
                (660, 460, sprites_folder + "artega.png", 0.9, 36),
            "cast":
                (580, 460, sprites_folder + "artega_cast.png", 0.9, 36)
        } 

}

#interactive sprites dictionary
ISD = {
    "pedestal": 
        (660, 460, sprites_folder + "pedestal.png", 0.6, 24)
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

#icons dictionary
ID = {
    
}
