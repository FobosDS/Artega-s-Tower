from Settings import *
from Projectile import Magic_Projectile_Manager

class Magic_System:                                             

    def __init__(self, projectile_manager=None):
        self.projectile_manager = (projectile_manager if projectile_manager is not None else Magic_Projectile_Manager())

    def is_loaded(self, stats):                                 
        return stats.combat.magic_shots_loaded > 0

    def try_cast(self, stats):                                  
        combat = stats.combat
        if combat.magic_shots_loaded > 0:
            return "Тьма уже поглощает Оскара!"
        if stats.base.dark_shards < 1:
            return "Оскару не хвататет осколка тьмы"

        if stats.base.dark_shards >= max_dark_shards:
            shots = magic_shots_at_max
        else:
            shots = magic_shots_per_shard

        stats.base.dark_shards -= 1
        combat.magic_shots_loaded = shots
        ess = getattr(stats, "essences", None)                       
        magic_mult = 1.25 if (ess is not None and ess.has("darkness")) else 1
        combat.magic_shots_damage = int((combat.attack_damage * magic_base_multiplier + stats.base.dark_shards * magic_shard_bonus) * magic_mult)
        return f"Оскара поглощает тьма!"

    def fire(self, player):                                     
        combat = player.stats.combat
        if combat.magic_shots_loaded <= 0:
            return False                  
        if combat.magic_shot_timer > 0:
            return True                   
        combat.magic_shots_loaded -= 1
        combat.magic_shot_timer = magic_shot_cooldown
        self.projectile_manager.fire(player.x, player.y, player.angle, combat.magic_shots_damage)
        if combat.magic_shots_loaded == 0:
            combat.magic_shots_damage = 0
            notify = getattr(player.stats, "notify", None)   
            if notify:
                notify("Организм Оскара очистился от тьмы!")
        return True

    def update(self, dt, player, enemies):                      
        combat = player.stats.combat
        timer = getattr(combat, "magic_shot_timer", 0)       
        if timer > 0:
            combat.magic_shot_timer = max(0.0, timer - dt)
        self.projectile_manager.update(dt, enemies) 
