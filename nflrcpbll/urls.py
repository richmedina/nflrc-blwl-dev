from django.conf.urls import patterns, include, url
from django.contrib import admin

from stacks.views import HomeView, StackListView, StackView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    
    url(r'^stacks/', StackListView.as_view(), name='stack_list' ),
    url(r'^stack/(?P<slug>[-\w]+)/$', StackView.as_view(), name='stack' ),


    url(r'^admin/', include(admin.site.urls)),
)
