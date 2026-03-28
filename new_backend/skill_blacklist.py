def skill_blacklist(skills, blacklist):
    if skills:
        skill_set = set(skills)
        blacklist_set = set(blacklist)
        return list(skill_set - blacklist_set)
    else:
        return []
