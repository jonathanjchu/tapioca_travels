from .models import *


def bread_crumbs(loc_id):
    loc = Location.objects.get(id=loc_id)
    parents = []

    while not loc.parent_location:
        loc = Location.objects.get(id=loc.parent_location.id)
        parents.append(loc.id)
    
    return parents
    
