from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Songs

# Register your models here.
# Recordar siempre registrar el modelo de base de datos!!!
# Siempre se te olvida David!!!!


class SongsAdmin(SummernoteModelAdmin):
    list_display = ('id', 'song', 'artista', 'category', 'thumbnail', 'content', 'date_created', 'tags','created_at', 'urlvideo',)
    list_display_links = ('id', 'song')
    search_fields = ('song', )
    list_per_page = 25
    summernote_fields = ('content', )


admin.site.register(Songs, SongsAdmin)