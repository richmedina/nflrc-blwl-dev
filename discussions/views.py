from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView, UpdateView, FormView, View
from django.core.urlresolvers import reverse

from braces.views import CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, LoginRequiredMixin, StaffuserRequiredMixin

from .models import Post, DiscussionLog
from .forms import PostForm, PostReplyForm
from lessons.models import LessonDiscussion, Project, Module, LessonModule, Lesson
from core.mixins import HonorCodeRequired, WhitelistRequiredMixin


class DiscussionListView(LoginRequiredMixin, TemplateView):
    template_name = 'discussions_index.html'

    def get(self, request, *args, **kwargs):

        return super(DiscussionListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DiscussionListView, self).get_context_data(**kwargs)
        threads = []
        try:
            self.project_context = Project.objects.get(slug=kwargs['project_slug'])
            lessons = self.project_context.get_lessons()
            # headers = Post.objects.filter(parent_post=None).order_by('created')
            headers = [{'module': i[0], 'lesson':  i[1], 'thread': i[1].lesson_discussion.all()[0].thread} for i in lessons]

            # self = Project.objects.get(slug=kwargs['project_slug'])
        except:
            pass

        for hdr in headers:
           
            # try:
            #     lesson = LessonDiscussion.objects.get(thread=hdr).lesson
            # except:
            #     lesson = None

            

            try:
                logger = DiscussionLog.objects.filter(user=self.request.user).get(discussion=hdr['thread'])
                last_visit =  logger.modified     
            except:
                last_visit = self.request.user.last_login
        
            replies = hdr['thread'].replies.all().filter(deleted=False)
            newmsgs = replies.filter(modified__gt = last_visit)            
            threads.append({'module': hdr['module'], 'lesson': hdr['lesson'], 'header': hdr['thread'], 'reply_count': len(replies), 'unread_reply_count': len(newmsgs)})

        context['threads'] = threads
        context['project'] = self.project_context
        return context


class DiscussionView(DetailView):
    model = Post
    template_name = 'discussions.html'
    module_context = None
    project_context = None
    lesson_context = None

    def get(self, request, *args, **kwargs):
        try:
            self.module_context = Module.objects.get(pk=kwargs.get('module_id'))
            self.project_context = self.module_context.project
            self.lesson_context = Lesson.objects.get(pk=kwargs.get('lesson_id'))
        except:
            print kwargs
            pass
        return super(DiscussionView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DiscussionView, self).get_context_data(**kwargs)

        context['lesson'] = self.lesson_context
        context['module'] = self.module_context
        context['project'] = self.project_context

        thread_post = self.get_object()
        context['thread'] = thread_post

        try:
            quiz = self.lesson_context.lesson_quiz.get().quiz
            context['quiz'] =  quiz
        except:
            pass
       
        if not self.request.user.is_authenticated():
            return context

        initial_post_data = {}
        initial_post_data['creator'] = self.request.user
        try:
            logger = DiscussionLog.objects.filter(user=self.request.user).get(discussion=thread_post) 
        except:
            logger = DiscussionLog(user=self.request.user, discussion=thread_post)
            logger.save()
        
        replies = thread_post.replies.all().filter(deleted=False).order_by('-created')
        new_replies = replies.filter(modified__gt = logger.modified)

        """ [(post_obj, post_form, [post_replies])]"""
        reply_list = []
        for i in replies:
            thread_reply = (i, i.get_reply_form(creator_init=self.request.user), i.replies.all().filter(deleted=False).order_by('-created'))
            reply_list.append(thread_reply)


        initial_post_data['subject'] = 'Re: %s'% thread_post.subject
        initial_post_data['parent_post'] = thread_post.id  
        form = PostReplyForm(initial=initial_post_data)       

        
        context['thread_list'] = Post.objects.filter(parent_post=None).order_by('created')

        context['replies'] = reply_list
        context['new_replies'] = new_replies
        context['postform'] = form

        logger.save()
        return context


class DiscussionViewPermLink(DetailView):
    model = Post
    template_name = 'discussions_permlink.html'

    def get(self, request, *args, **kwargs):
        return super(DiscussionViewPermLink, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DiscussionViewPermLink, self).get_context_data(**kwargs)

        initial_post_data = {}
        initial_post_data['creator'] = self.request.user
        thread_post = self.get_object()
        context['thread'] = thread_post

        try:
            lesson = thread_post.lesson_post.all().get().lesson
            context['lesson'] = lesson
        except:
            context['lesson'] = None

        try:
            quiz = lesson.lesson_quiz.get().quiz
            context['quiz'] =  quiz
        except:
            pass

        return context


class PostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post.html'


class PostUpdateView(LoginRequiredMixin, CsrfExemptMixin, UpdateView):
    model = Post
    form_class= PostReplyForm
    template_name = 'edit_form.html'


    def get_form_class(self):
        form_class = super(PostUpdateView, self).get_form_class()
        if self.request.user.is_staff:
            form_class = PostForm
        return form_class

    def get_success_url(self):
        current = self.get_object()
        parent = current.parent_post

        if parent:
            if parent.parent_post:  # subthread. make sure to display master thread
                return reverse('discussion_permlink', args=[str(parent.parent_post.id)])
            return reverse('discussion_permlink', args=[str(parent.id)])
        return reverse('discussion_permlink', args=[str(current.id)])
    

class PostCreateView(LoginRequiredMixin, CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, CreateView):
    model = Post
    template_name = 'discussions.html'
    form_class= PostReplyForm


    def post_ajax(self, request, *args, **kwargs):
        postform = PostReplyForm(request.POST)
        if postform.is_valid():

            new_post = postform.save()
            data = {}
            data['id'] = new_post.id
            data['modified'] = new_post.modified.strftime('%b %d %Y %H:%M')
            data['text'] = new_post.text
            data['creator'] = new_post.creator.username
            data['subject'] = new_post.subject

            try:
                logger = DiscussionLog.objects.get(user=request.user, discussion=new_post.parent_post)
                logger.save()
            except:
                pass
            # print self.render_json_response(data)
            return self.render_json_response(data)
        else:
            data = postform.errors
            return self.render_json_response(data)

class PostDeleteView(LoginRequiredMixin, CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, View):
   
    def post_ajax(self, request, *args, **kwargs):
        if request:
            try:
                post = Post.objects.get(id=request.POST['post'])
                
                if post.creator == request.user or request.user.is_staff:
                    post.deleted = True
                    post.save()
                    data = 'data removed'
                    return self.render_json_response(data)
                else:
                    data = 'data not removed'

            except Exception as e:
                data = 'data not removed'
        
        return self.render_json_response(data) 


