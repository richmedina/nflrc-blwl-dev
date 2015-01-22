from django.contrib import admin
from django.forms import ModelForm

from lessons.models import Module, Lesson, LessonSection, LessonQuiz, LessonDiscussion, PbllPage
from discussions.models import Post
from .models import Whitelist

class ExtraMedia:
    js = [
        '/static/js/tinymce/jquery.tinymce.min.js',
        '/static/js/tinymce/tinymce.min.js',
    ]

class LessonDiscussionAdminModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(LessonDiscussionAdminModelForm, self).__init__(*args, **kwargs)
        self.fields['thread'].queryset = Post.objects.filter(parent_post__isnull=True)

    class Meta:
        model = LessonDiscussion
        fields = ['thread', 'lesson']

class LessonSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'content_type', 'lesson')
    list_filter = ['lesson', 'content_type']   

class LessonDiscussionAdmin(admin.ModelAdmin):
	form = LessonDiscussionAdminModelForm

admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(LessonSection, LessonSectionAdmin)
admin.site.register(LessonQuiz)
admin.site.register(LessonDiscussion, LessonDiscussionAdmin)
admin.site.register(Post)
admin.site.register(Whitelist)
admin.site.register(PbllPage)
