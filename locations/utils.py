from .models import Location
class LocationDuplicator():
    def __str__(self):
        return "LocationDuplicator"
    
    def duplicate(self, location, top = True, parent=None):
        copy = ""
        new_loc = Location()
        if top:
            copy = "(Copy)"
            parent = Location.objects.filter(name = "Templates").first()
        new_loc.name = location.name + copy
        new_loc.description = location.description
        new_loc.parent = parent
        new_loc.save()
        if location.children.exists():
            for child in location.children.all():
                
                self.duplicate(child, False, new_loc)

        

