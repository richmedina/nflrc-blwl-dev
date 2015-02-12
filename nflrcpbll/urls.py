from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from filebrowser.sites import site

from lessons.views import HomeView, ModuleView, LessonView, LoginForbiddenView, ModuleUpdateView, LessonUpdateView, LessonSectionUpdateView, PbllPageUpdateView, PbllPageView
from quiz.views import QuizTake
from discussions.views import DiscussionListView, DiscussionView, PostCreateView, PostDeleteView, PostUpdateView
from core.views import HonorCodeFormView, ParticipantListView, ParticipantUpdateView, ParticipantCreateView, ParticipantDeleteView

urlpatterns = patterns('',

    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),

	url(r'^$', HomeView.as_view(), name='home'),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    # url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    
    url(r'^quiz/', include('quiz.urls')),
    
    url(r'^module/(?P<slug>[-\w]+)/$', ModuleView.as_view(), name='module' ),
    url(r'^module/(?P<slug>[-\w]+)/edit/$', ModuleUpdateView.as_view(), name='module_edit' ),
        
    url(r'^lesson/(?P<slug>[-\w]+)/$', LessonView.as_view(), name='lesson' ),
    url(r'^lesson/edit/(?P<slug>[-\w]+)/$', LessonUpdateView.as_view(), name='lesson_edit' ),
    url(r'^lesson/(?P<slug>[-\w]+)/(?P<section>[-\w]+)/$', LessonView.as_view(), name='lesson_section' ),
    url(r'^lesson/(?P<lesson>[-\w]+)/(?P<pk>[-\w]+)/edit/$', LessonSectionUpdateView.as_view(), name='lesson_section_edit' ),
    url(r'^lesson/(?P<quiz_name>[-\w]+)/quiz/take/', QuizTake.as_view(), name='lesson_quiz'),

    url(r'^discussions/(?P<slug>[-\w]+)/$', DiscussionView.as_view(), name='discussion_select' ),
    url(r'^discussions/$', DiscussionListView.as_view(), name='discussion' ),
    url(r'^discussions/post/add/$', PostCreateView.as_view(), name='create_post'),
    url(r'^discussions/post/delete/$', PostDeleteView.as_view(), name='delete_post'),
    url(r'^discussions/post/(?P<pk>[-\w]+)/edit/$', PostUpdateView.as_view(), name='edit_post'),
    

    url(r'^pbllpage/(?P<slug>[-\w]+)/$', PbllPageView.as_view(), name='pbllpage' ),
    url(r'^pbllpage/edit/(?P<slug>[-\w]+)/$', PbllPageUpdateView.as_view(), name='pbllpage_edit' ),

    
    url(r'^participants/$', ParticipantListView.as_view(), name='participants'),
    url(r'^participants/add/$', ParticipantCreateView.as_view(), name='add_participant'),
    url(r'^participants/edit/(?P<pk>[-\w]+)/$', ParticipantUpdateView.as_view(), name='edit_participant'),
    url(r'^participants/delete/(?P<pk>[-\w]+)/$', ParticipantDeleteView.as_view(), name='delete_participant'),

    url(r'^inactive-user/$', HonorCodeFormView.as_view(), name='honor_agreement'),
    url(r'^login-forbidden/$', LoginForbiddenView.as_view(), name='login_forbidden'),
)
