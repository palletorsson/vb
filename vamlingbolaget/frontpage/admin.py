from django.contrib import admin
from models import Frontpage, FrontpageTheme, FrontpageExtended

class FrontpageAdmin(admin.ModelAdmin):
    model = Frontpage

class FrontpageThemeAdmin(admin.ModelAdmin):
    model = FrontpageExtended

class FrontpageExtendedAdmin(admin.ModelAdmin):
    model = FrontpageExtended

admin.site.register(Frontpage, FrontpageAdmin)

admin.site.register(FrontpageTheme, FrontpageThemeAdmin)

admin.site.register(FrontpageExtended, FrontpageExtendedAdmin)

