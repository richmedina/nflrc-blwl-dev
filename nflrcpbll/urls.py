from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from filebrowser.sites import site

from lessons.views import HomeView, ProjectView, ProjectListView, ProjectCreateView, ProjectUpdateView, ModuleView, LessonViewAll, LessonView, LessonViewPermLink, LoginForbiddenView, MembershipAccessErrorView, ModuleCreateView, ModuleUpdateView, ModuleDeleteView, LessonCreateView, LessonModuleCreatePairView, LessonModuleDeletePairView, LessonUpdateView, LessonDeleteView, LessonSectionUpdateView, PbllPageUpdateView, PbllPageView, LessonQuizQuestionCreateView, LessonQuizQuestionUpdateView, LessonQuizQuestionDetailView, LessonQuizQuestionListView, LessonQuizQuestionDeleteView
from quiz.views import QuizTake
from discussions.views import DiscussionListView, DiscussionView, DiscussionViewPermLink, PostCreateView, PostDeleteView, PostUpdateView
from core.views import HonorCodeFormView, ProjectParticipantListView, ProjectParticipantCreateView, ProjectParticipantDeleteView, WhitelistView, WhitelistObjectCreateView, WhitelistObjectUpdateView, WhitelistObjectDeleteView

urlpatterns = patterns('',

    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    
    url(r'^login-forbidden/$', LoginForbiddenView.as_view(), name='login_forbidden'),
	url(r'^membership-access/$', MembershipAccessErrorView.as_view(), name='member_access_error'),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    # url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),  
    url(r'^quiz/', include('quiz.urls')),
    url(r'^project_listing/$', ProjectListView.as_view(), name='project_listing' ),
    url(r'^project_add/$', ProjectCreateView.as_view(), name='project_create' ),

# PROJECT (SERIES)
    # Display modules and lessons collected as part of a series.
    # Series (or projects) are collections of modules containing lessons. A series is open or restricted.
    url(r'^(?P<slug>[-\w]+)/$', ProjectView.as_view(), name='project' ),
    url(r'^(?P<slug>[-\w]+)/edit/$', ProjectUpdateView.as_view(), name='project_edit' ),
    
# MODULE
    # Root page for a module.
    # Display information and lessons that are associated with a module.
    url(r'^(?P<project_slug>[-\w]+)/module/add/$', ModuleCreateView.as_view(), name='module_create' ),
    url(r'^(?P<project_slug>[-\w]+)/module/(?P<pk>[-\w]+)/$', ModuleView.as_view(), name='module' ),
    url(r'^(?P<project_slug>[-\w]+)/module/(?P<pk>[-\w]+)/edit/$', ModuleUpdateView.as_view(), name='module_edit' ),
    url(r'^(?P<project_slug>[-\w]+)/module/(?P<pk>[-\w]+)/delete/$', ModuleDeleteView.as_view(), name='module_delete' ),

# LESSON (PROJECT)
    # url(r'^(?P<project_slug>[-\w]+)/module/(?P<module_id>[-\w]+)/lesson/add/$', LessonCreateView.as_view(), name='lesson_create' ),
    url(r'^(?P<project_slug>[-\w]+)/module/(?P<module_id>[-\w]+)/lesson/(?P<pk>[-\w]+)/$', LessonView.as_view(), name='lesson' ),
    url(r'^(?P<project_slug>[-\w]+)/module/(?P<module_id>[-\w]+)/lesson/(?P<pk>[-\w]+)/section/(?P<section>[-\w]+)/$', LessonView.as_view(), name='lesson_section' ),
    url(r'^(?P<project_slug>[-\w]+)/module/(?P<module_id>[-\w]+)/lesson/(?P<lesson_id>[-\w]+)/discussion/(?P<pk>[-\w]+)/$', DiscussionView.as_view(), name='discussion' ),
    url(r'^(?P<project_slug>[-\w]+)/module/(?P<module_id>[-\w]+)/lesson/(?P<lesson_id>[-\w]+)/quiz/(?P<quiz_id>[-\w]+)/quiz/take/', QuizTake.as_view(), name='lesson_quiz'),
   

    
    # url(r'^(?P<project_slug>[-\w]+)/module/lesson/edit/(?P<pk>[-\w]+)/$', LessonUpdateView.as_view(), name='lesson_edit' ),
    # url(r'^(?P<project_slug>[-\w]+)/module/lesson/(?P<pk>[-\w]+)/section/(?P<section>[-\w]+)/$', LessonView.as_view(), name='lesson_section' ),
    # url(r'^(?P<project_slug>[-\w]+)/module/lesson/section/edit/(?P<pk>[-\w]+)/$', LessonSectionUpdateView.as_view(), name='lesson_section_edit' ),
    # url(r'^(?P<project_slug>[-\w]+)/module/lesson/delete/(?P<pk>[-\w]+)/$', LessonDeleteView.as_view(), name='lesson_delete' ),


# LESSON (permalinked)
    url(r'^lesson/all/$', LessonViewAll.as_view(), name='lesson_list'),
    url(r'^lesson/add/$', LessonCreateView.as_view(), name='lesson_create'),
    url(r'^lesson-module/add/$', LessonModuleCreatePairView.as_view(), name='lesson_module_create'),
    url(r'^lesson-module/delete/(?P<pk>[-\w]+)$', LessonModuleDeletePairView.as_view(), name='lesson_module_detach'),
    url(r'^lesson/(?P<pk>[-\w]+)/$', LessonViewPermLink.as_view(), name='lesson_permlink' ),
    url(r'^lesson/(?P<pk>[-\w]+)/section/(?P<section>[-\w]+)/$', LessonViewPermLink.as_view(), name='lesson_section_permlink' ),
    url(r'^lesson/(?P<pk>[-\w]+)/edit/$', LessonUpdateView.as_view(), name='lesson_edit' ),
    url(r'^lesson/section/(?P<pk>[-\w]+)/edit/$', LessonSectionUpdateView.as_view(), name='lesson_section_edit' ),
    url(r'^lesson/(?P<pk>[-\w]+)/delete/$', LessonDeleteView.as_view(), name='lesson_delete' ),

# QUIZ
    url(r'^lesson/quiz/(?P<quiz_id>[-\w]+)/question/(?P<pk>[-\w]+)/$', LessonQuizQuestionDetailView.as_view(), name='question_preview' ),    
    url(r'^lesson/quiz/(?P<quiz_id>[-\w]+)/add/question/$', LessonQuizQuestionCreateView.as_view(), name='question_create' ),    
    url(r'^lesson/quiz/(?P<quiz_id>[-\w]+)/edit/question/(?P<pk>[-\w]+)/$', LessonQuizQuestionUpdateView.as_view(), name='question_edit' ),
    url(r'^lesson/quiz/(?P<quiz_id>[-\w]+)/delete/question/(?P<pk>[-\w]+)/$', LessonQuizQuestionDeleteView.as_view(), name='question_delete' ),
    url(r'^lesson/quiz/(?P<pk>[-\w]+)/list/questions/$', LessonQuizQuestionListView.as_view(), name='question_list' ),        
    url(r'^lesson/quiz/(?P<quiz_id>[-\w]+)/quiz/take/', QuizTake.as_view(), name='lesson_quiz_permlink'),

# DISCUSSION
    url(r'^(?P<project_slug>[-\w]+)/discussion/all/$', DiscussionListView.as_view(), name='discussion_list' ),
    url(r'^discussion/(?P<pk>[-\w]+)/$', DiscussionViewPermLink.as_view(), name='discussion_permlink' ),
    url(r'^discussion/post/add/$', PostCreateView.as_view(), name='create_post'),
    url(r'^discussion/post/delete/$', PostDeleteView.as_view(), name='delete_post'),
    url(r'^discussion/post/(?P<pk>[-\w]+)/edit/$', PostUpdateView.as_view(), name='edit_post'),
    
# CONTENT PAGE
    url(r'^pbllpage/(?P<slug>[-\w]+)/$', PbllPageView.as_view(), name='pbllpage' ),
    url(r'^pbllpage/edit/(?P<slug>[-\w]+)/$', PbllPageUpdateView.as_view(), name='pbllpage_edit' ),

# WHITELIST MANAGMENT 
    url(r'^whitelist/all/$', WhitelistView.as_view(), name='whitelist'),
    url(r'^whitelist/add/$', WhitelistObjectCreateView.as_view(), name='whitelist_add'),
    url(r'^whitelist/edit/(?P<pk>[-\w]+)/$', WhitelistObjectUpdateView.as_view(), name='whitelist_edit'),
    url(r'^whitelist/delete/(?P<pk>[-\w]+)/$', WhitelistObjectDeleteView.as_view(), name='whitelist_delete'),

# PARTICIPANT/PROJECT MEMBERSHIP MANAGEMENT
    url(r'^(?P<project_slug>[-\w]+)/participants/$', ProjectParticipantListView.as_view(), name='participants'),
    url(r'^(?P<project_slug>[-\w]+)/participants/add/$', ProjectParticipantCreateView.as_view(), name='add_participant'),
    url(r'^(?P<project_slug>[-\w]+)/participants/delete/(?P<pk>[-\w]+)/$', ProjectParticipantDeleteView.as_view(), name='remove_participant'),

    url(r'^inactive-user/$', HonorCodeFormView.as_view(), name='honor_agreement'),
    
)
