from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return " > ".join(full_path[::-1])
    
    def duplicate(self, top = True, parent=None):
        copy = ""
        new_loc = Location()
        if top:
            copy = "(Copy)"
            parent = self.parent
        new_loc.name = self.name + copy
        new_loc.description = self.description
        new_loc.parent = parent
        new_loc.save()
        if self.children.exists():
            for child in self.children.all():
                child.duplicate(False, new_loc)