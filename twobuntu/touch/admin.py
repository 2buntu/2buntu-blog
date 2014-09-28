from django.contrib import admin

from twobuntu.touch.models import Application, Department, Keyword, Publisher, Screenshot

admin.site.register(Application)
admin.site.register(Department)
admin.site.register(Keyword)
admin.site.register(Publisher)
admin.site.register(Screenshot)
