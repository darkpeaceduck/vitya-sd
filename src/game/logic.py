LONGEST_FIGHT = 10000

def make_damage(dest, fighter):
    damage = fighter.damage
    to_armor = min(damage, dest.armor)
    dest.armor -= to_armor
    damage -= to_armor
    to_hp = min(damage, dest.hp)
    dest.hp -= to_hp
    
def is_destroy(dest):
    return dest.hp <= 0

def simulate_fight(player, enemy):
    for _ in range(0, LONGEST_FIGHT):
        for j in range(0, player.speed):
            make_damage(enemy, player)
            if is_destroy(enemy):
                return player
        for j in range(0, enemy.speed):
            make_damage(player, enemy)
            if is_destroy(player):
                return enemy
            
def get_drop(player, item):
    if item.active:
        return False
    player.armor += item.armor
    player.damage += item.damage
    return True
            
def can_move(obj, delta):
    return 2 * (1.0/obj.move_speed) < delta