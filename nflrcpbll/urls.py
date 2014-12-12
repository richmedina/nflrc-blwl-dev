from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from lessons.views import HomeView, LessonListView, LessonView, IsotopeView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    
    url(r'^lessons/', LessonListView.as_view(), name='lesson_list' ),
    url(r'^lesson/(?P<slug>[-\w]+)/$', LessonView.as_view(), name='lesson' ),

    url(r'^isotoped/', IsotopeView.as_view(), name='isotoped' ),
    
    url(r'^admin/', include(admin.site.urls)),
)
