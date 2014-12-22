from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from lessons.views import HomeView, ModuleView, LessonListView, LessonView, IsotopeView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', HomeView.as_view(), name='home'),

    
    url(r'^module/(?P<slug>[-\w]+)/$', ModuleView.as_view(), name='module' ),
    
    url(r'^(?P<module>[-\w]+)/lessons/$', LessonListView.as_view(), name='lesson_list' ),
    url(r'^(?P<module>[-\w]+)/(?P<slug>[-\w]+)/$', LessonView.as_view(), name='lesson' ),

    url(r'^(?P<module>[-\w]+)/(?P<lesson>[-\w]+)/test/', include('quiz.urls')),
    
    url(r'^isotoped/$', IsotopeView.as_view(), name='isotoped' ),
)
