from django.contrib import admin

from .models import Rating
from .models import Comment

class RatingAdmin(admin.ModelAdmin):
    fields = ['rating_num', 'reviewer', 'content_type', 'object_id', 'content_object']
    readonly_fields = ['content_object']
    class Meta:
        model = Rating

class CommentAdmin(admin.ModelAdmin):
    fields = ['comment_text', 'reviewer', 'content_type', 'object_id', 'content_object']
    readonly_fields = ['content_object']
    class Meta:
        model = Comment

admin.site.register(Rating, RatingAdmin)
admin.site.register(Comment, CommentAdmin)