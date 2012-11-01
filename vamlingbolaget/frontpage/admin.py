from django.contrib import admin
from models import Frontpage

class FrontpageAdmin(admin.ModelAdmin):
    model = Frontpage

admin.site.register(Frontpage, FrontpageAdmin)

