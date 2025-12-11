from django.contrib import admin

from .models import Annotation, Category, Collection, Es_document, Tag

admin.site.register(Collection)
admin.site.register(Annotation)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Es_document)
