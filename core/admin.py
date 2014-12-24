from django.contrib import admin
# admin.autodiscover()

from lessons.models import Module, Lesson, LessonSection, LessonQuiz
from discussions.models import Post

class ExtraMedia:
    js = [
        '/static/js/tinymce/jquery.tinymce.min.js',
        '/static/js/tinymce/tinymce.min.js',
    ]
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(LessonSection)
admin.site.register(LessonQuiz)
admin.site.register(Post)
