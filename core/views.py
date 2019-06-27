from django.shortcuts import redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import FormView, ListView, UpdateView, CreateView, DeleteView

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin

from core.models import Whitelist, ProjectMembership
from lessons.models import PbllPage, Project
from .forms import HonorCodeForm, WhitelistCreateForm, WhitelistUpdateForm, ProjectParticipantCreateForm



class HonorCodeFormView(FormView):
    template_name = 'inactive.html'
    form_class = HonorCodeForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if form.cleaned_data['honor_agreement']:
        	whitelister = Whitelist.objects.get(email_addr=self.request.user.email)
        	whitelister.honor_agreement = True
        	whitelister.save()
        else:
        	return redirect('home')

        return super(HonorCodeFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(HonorCodeFormView, self).get_context_data(**kwargs)
        context['pbllpage'] = PbllPage.objects.get(slug='honor-agreement')
        return context


class WhitelistView(LoginRequiredMixin, StaffuserRequiredMixin, ListView):
    """Displays listing of all whitelisted email accounts on site."""
    model = Whitelist
    template_name = 'whitelist.html'

    def get_context_data(self, **kwargs):
        context = super(WhitelistView, self).get_context_data(**kwargs)
        return context


class WhitelistObjectCreateView(LoginRequiredMixin, StaffuserRequiredMixin, CreateView):
    """Creates a whitelist object to master whitelist."""
    model = Whitelist
    template_name = 'create_form.html'
    form_class = WhitelistCreateForm
    success_url = reverse_lazy('whitelist')

    def get_initial(self):
        initial = self.initial.copy()
        try:
            membership_slug = self.request.GET.get('proj_membership')
            initial['membership'] = Project.objects.filter(slug=membership_slug)
        except:
            pass  #no query parameter provided or invalid project slug, Proceed with unassociated project.
        return initial

    def form_valid(self, form):
        """
        Called if all forms are valid. Creates whitelist/project membership pairs if project is specified in query parameters.
        """
        self.object = form.save()
        try:
            project_objs = form.cleaned_data['membership']
            if project_objs:
                for i in project_objs:
                    project_membership = ProjectMembership(project=i, user=self.object)
                    project_membership.save()
        except:
            pass

        return super(WhitelistObjectCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(WhitelistObjectCreateView, self).get_context_data(**kwargs)
        return context


class WhitelistObjectUpdateView(LoginRequiredMixin, StaffuserRequiredMixin, UpdateView):
    """Updates a whitelist object. Email address and membership list are relative fields."""
    model= Whitelist
    template_name = 'edit_form.html'
    form_class = WhitelistUpdateForm
    success_url = reverse_lazy('whitelist')

    def get_initial(self):
        initial = self.initial.copy()
        try:
            initial['membership'] = [p.project for p in self.get_object().member_projects.all()]
        except:
            pass  
        return initial

    def form_valid(self, form):
        """
        Called if all forms are valid. Creates whitelist/project membership pairs if project is specified in query parameters.
        """
        self.object = form.save()
        try:
            project_objs = form.cleaned_data['membership']
            if project_objs:
                for i in project_objs:
                    project_membership = ProjectMembership(project=i, user=self.object)
                    project_membership.save()
        except:
            pass

        return super(WhitelistObjectUpdateView, self).form_valid(form)


class WhitelistObjectDeleteView(LoginRequiredMixin, StaffuserRequiredMixin, DeleteView):
    model = Whitelist
    template_name = 'generic_confirm_delete.html'
    success_url = reverse_lazy('whitelist')


class ProjectParticipantListView(LoginRequiredMixin, StaffuserRequiredMixin, ListView):
    template_name = 'participants.html'
    model = Whitelist

    def get_queryset(self):
        project = Project.objects.get(slug=self.kwargs.get('project_slug'))
        queryset = [(q.user, q.pk) for q in project.member_list.all()]
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProjectParticipantListView, self).get_context_data(**kwargs)
        # context['active_list'] = context['object_list'].filter(site_account__isnull=False).order_by('-site_account__last_login')
        context['project'] = Project.objects.get(slug=self.kwargs.get('project_slug'))

        return context


class ProjectParticipantCreateView(LoginRequiredMixin, StaffuserRequiredMixin, CreateView):
    model = ProjectMembership
    template_name = 'add_participant_form.html'
    form_class = ProjectParticipantCreateForm
    project = None

    def get_initial(self):
        initial = self.initial.copy()
        try: 
            self.project = Project.objects.get(slug=self.kwargs.get('project_slug'))
            initial['project'] = self.project
            
        except Exception as e:
            pass

        return initial

    def get_success_url(self):
        return reverse('participants', args=[self.object.project.slug])

    def get_context_data(self, **kwargs):
        context = super(ProjectParticipantCreateView, self).get_context_data(**kwargs)
        context['project_name'] = self.project.title
        context['members'] = [i.user for i in self.project.member_list.all()]
        return context


class ProjectParticipantDeleteView(LoginRequiredMixin, StaffuserRequiredMixin, DeleteView):
    model = ProjectMembership
    template_name = 'generic_confirm_delete.html'

    def get_success_url(self):
        return reverse('participants', args=[self.object.project.slug])

    def get_context_data(self, **kwargs):
        context = super(ProjectParticipantDeleteView, self).get_context_data(**kwargs)
        return context
