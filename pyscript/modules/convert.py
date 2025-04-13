# function to convert seconds to timer value
def sec_to_timer(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return '%d:%02d:%02d' % (hour, min, sec)

# process entity ID to determine domain
def get_domain(entity):
    ent = f"entity"
    domain = ent[:ent.index(".")]
    return domain