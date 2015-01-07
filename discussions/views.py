from django.views.generic import TemplateView, CreateView, ListView, DetailView

from braces.views import CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, LoginRequiredMixin

from .models import Post
from .forms import PostForm, PostReplyForm
from lessons.models import LessonDiscussion


class DiscussionListView(LoginRequiredMixin, TemplateView):
    template_name = 'discussions_index.html'

    def get_context_data(self, **kwargs):
        context = super(DiscussionListView, self).get_context_data(**kwargs)
        headers = Post.objects.filter(parent_post=None).order_by('-modified')
        threads = []

        for hdr in headers:
           
            try:
                lesson = LessonDiscussion.objects.get(thread=hdr).lesson
            except:
                lesson = None
            
            threads.append({'lesson': lesson, 'header': hdr, 'reply_count': hdr.replies.count()})

        context['threads'] = threads
        return context


class DiscussionView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'discussions.html'
    
    def get_context_data(self, **kwargs):
        context = super(DiscussionView, self).get_context_data(**kwargs)
        initial_post_data = {}
        initial_post_data['creator'] = self.request.user
        thread_post = self.get_object()
        
        try:
            lesson = LessonDiscussion.objects.get(thread=thread_post).lesson
        except:
            lesson = None

        replies = thread_post.replies.all().order_by('-modified')
        initial_post_data['subject'] = 'Re: %s'% thread_post.subject
        initial_post_data['parent_post'] = thread_post.id  
        form = PostReplyForm(initial=initial_post_data)

        context['thread'] = thread_post
        context['thread_list'] = Post.objects.filter(parent_post=None).order_by('-modified')
        context['lesson'] = lesson
        context['replies'] = replies
        context['postform'] = form

        return context

class PostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post.html'

class PostCreateView(LoginRequiredMixin, CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, CreateView):
    model = Post
    template_name = 'discussions.html'
    form_class= PostForm

    def post_ajax(self, request, *args, **kwargs):
        postform = PostForm(request.POST)
        if postform.is_valid():

            new_post = postform.save()
            data = {}
            data['modified'] = new_post.modified.strftime('%b %d %Y %H:%M')
            data['text'] = new_post.text
            data['creator'] = new_post.creator.username
            data['subject'] = new_post.subject

            # print self.render_json_response(data)
            return self.render_json_response(data)
        else:
            data = postform.errors
            print 'Errors?' , data
            return self.render_json_response(data)