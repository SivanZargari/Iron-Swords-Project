from django.contrib import admin
from .models import Hero
from django.utils.html import format_html

class HeroAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'age', 'hometown', 'country_of_birth', 'hero_story', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        return 'No Image'

    image_tag.short_description = 'Image'

admin.site.register(Hero, HeroAdmin)
