def get_first_matching_object(predicate, objects=[]):
    for obj in objects:
        if ob:= predicate(obj):
            return ob
    return None

print(get_first_matching_object(lambda x: x == 2, [2, 3, 4]))
