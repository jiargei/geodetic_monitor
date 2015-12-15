from django.contrib import admin

from setup.models import Project, Membership, Position, Station, Sensor, Target, Task, TimeWindow, Box
from setup.models import ObservationType, Limit, LimitNotification, UserNotification, BoxNotification

# Register your models here.


admin.site.register(Box)
admin.site.register(Project)
admin.site.register(Membership)
admin.site.register(Position)
admin.site.register(Station)
admin.site.register(Sensor)

admin.site.register(Target)

admin.site.register(Task)
admin.site.register(TimeWindow)

admin.site.register(ObservationType)
admin.site.register(Limit)
admin.site.register(BoxNotification)
admin.site.register(LimitNotification)
admin.site.register(UserNotification)