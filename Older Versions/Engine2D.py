def collide(object1, object2):
    hitboxes = set()
    for x in range(0, object1[2] + 1, object1[2]):
        for y in range(0, object1[3] + 1, object1[3]):
            hitboxes.add((object1[0] + x, object1[1] + y))

    for hitbox in hitboxes:
        if (object2[1] <= hitbox[1] <= object2[1] + object2[3] and
           object2[0] <= hitbox[0] <= object2[0] + object2[2]):
            return True

    return False
