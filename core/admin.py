from django.contrib import admin
from django.forms import ModelForm

from lessons.models import Project, Module, Lesson, LessonModule, LessonSection, LessonQuiz, LessonDiscussion, PbllPage
from discussions.models import Post, DiscussionLog
from .models import Whitelist, ProjectMembership

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

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'creator', 'subject', 'deleted', 'parent_post')
    list_filter = ['deleted']

class DiscussionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'discussion', 'created', 'modified')
    list_filter = ['user']

class WhitelistAdmin(admin.ModelAdmin):
    list_display = ('email_addr', 'participant_type', 'honor_agreement')
    list_filter = ['participant_type', 'honor_agreement']
    list_editable = ['email_addr', 'participant_type', 'honor_agreement']

admin.site.register(Project)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(LessonModule)
admin.site.register(LessonSection, LessonSectionAdmin)
admin.site.register(LessonQuiz)
admin.site.register(LessonDiscussion, LessonDiscussionAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(DiscussionLog, DiscussionLogAdmin)
admin.site.register(Whitelist, WhitelistAdmin)
admin.site.register(ProjectMembership)
admin.site.register(PbllPage)
