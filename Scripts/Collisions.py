def check_walls_collision(test_rect, walls):
    for wall in walls:
        if test_rect.colliderect(wall):
            return True
    return False

def check_objects_collision(test_rect, objects):
    for obj in objects:
        if test_rect.colliderect(obj.rect):
            return True
    return False

def check_collision(test_rect, walls, objects):
    return check_walls_collision(test_rect, walls) or check_objects_collision(test_rect, objects)