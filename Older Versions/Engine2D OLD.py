def collide(object1, object2):
    hitboxes1 = set()
    hitboxes1.add((missile[0], missile[1]))
    hitboxes1.add((missile[0], missile[1] + missile[3]))
    hitboxes1.add((missile[0] + missile[2], missile[1]))
    hitboxes1.add((missile[0] + missile[2], missile[1] + missile[3]))
    
    hitboxes2 = set()
    for x in range(0, object2[2]):
        for y in range(0, object2[3]):
            hitboxes2.add((object2[0] + x, object2[1] + y))
                
    for hit in hitboxes1:
        if hit in hitboxes2:
            return True
    return False
