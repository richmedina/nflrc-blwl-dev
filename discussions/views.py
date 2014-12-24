from django.views.generic import TemplateView, CreateView, ListView

from braces.views import CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, LoginRequiredMixin

from .models import Post
from .forms import PostForm, PostReplyForm

class DiscussionView(LoginRequiredMixin, TemplateView):
    template_name = 'discussions.html'
    
    def get_context_data(self, **kwargs):
        context = super(DiscussionView, self).get_context_data(**kwargs)
        initial_post_data = {}
        initial_post_data['creator'] = self.request.user

        threads = []
        headers = Post.objects.filter(parent_post=None).order_by('-modified')

        for hdr in headers:
            replies = hdr.replies.all().order_by('-modified')
            initial_post_data['subject'] = 'Re: %s'% hdr.subject
            initial_post_data['parent_post'] = hdr.id  
            form = PostReplyForm(initial=initial_post_data)
            threads.append({'header': hdr, 'replies': replies, 'postform': form})

        context['threads'] = threads
        return context

class PostView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post.html'

class PostCreateView(LoginRequiredMixin, CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, CreateView):
    model = Post
    template_name = 'discussions.html'
    form_class= PostForm
    # success_url = reverse_lazy('view_note')

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