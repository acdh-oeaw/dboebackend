from django.contrib import admin
from .models import Category, Tag, Collection, Es_document, Annotation
from guardian.admin import GuardedModelAdmin

# Register your models here.


# With object permissions support
class CollectionAdmin(GuardedModelAdmin):
    pass


class AnnotationAdmin(GuardedModelAdmin):
    pass


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Es_document)
admin.site.register(Annotation, AnnotationAdmin)
