from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from quiz.views import QuizTake
from lessons.views import HomeView, ModuleView, LessonView, IsotopeView
from discussions.views import DiscussionView, PostCreateView

urlpatterns = patterns('',
	url(r'^$', HomeView.as_view(), name='home'),
    
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^quiz/', include('quiz.urls')),
    
    url(r'^module/(?P<slug>[-\w]+)/$', ModuleView.as_view(), name='module' ),
        
    url(r'^lesson/(?P<slug>[-\w]+)/$', LessonView.as_view(), name='lesson' ),
    url(r'^lesson/(?P<slug>[-\w]+)/(?P<section>[-\w]+)/$', LessonView.as_view(), name='lesson_section' ),
    url(r'^lesson/(?P<quiz_name>[-\w]+)/quiz/take/', QuizTake.as_view(), name='lesson_quiz'),

    url(r'^discussions/$', DiscussionView.as_view(), name='discussion' ),
    url(r'^discussions/post/add/$', PostCreateView.as_view(), name='create_post'),

    url(r'^isotoped/$', IsotopeView.as_view(), name='isotoped' ),
)
