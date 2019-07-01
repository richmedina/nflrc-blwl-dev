from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, FormView, DeleteView, ListView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django import forms

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from filebrowser.sites import site
from filebrowser.base import FileListing

from core.mixins import HonorCodeRequired, WhitelistRequiredMixin
from quiz.models import Quiz, Sitting
from multichoice.models import MCQuestion, Answer
from .models import Project, Module, Lesson, LessonModule, LessonSection, LessonQuiz, PbllPage
from .forms import ModuleUpdateForm, ModuleCreateForm, LessonCreateForm, LessonModuleCreateForm, LessonUpdateForm, LessonSectionUpdateForm, LessonQuizQuestionCreateForm, AnswersCreateFormSet, AnswersUpdateFormSet, PbllPageUpdateForm
 
class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        projects = Project.objects.all()
        context['public_projects'] = projects.filter(public=True)
        if self.request.user.is_authenticated():
            if self.request.user.is_staff:
                context['member_projects'] = projects.filter(public=False)
            else:
                try:
                    w = self.request.user.whitelisting.get()
                    context['member_projects'] = [mp.project for mp in w.member_projects.all()]
                except:
                    pass
        else:
            context['anonymous'] = True
        return context


class ProjectView(WhitelistRequiredMixin, DetailView):
    model = Project
    template_name = 'index_project.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['modules'] = self.get_object().project_modules.all()
        return context  


class ProjectListView(LoginRequiredMixin, StaffuserRequiredMixin, ListView):
    model = Project
    template_name = 'project_list.html'
    

class ProjectCreateView(LoginRequiredMixin, StaffuserRequiredMixin, CreateView):
    model = Project
    template_name = 'create_form.html'

    
class ProjectUpdateView(LoginRequiredMixin, StaffuserRequiredMixin, UpdateView):
    model = Project
    template_name = 'edit_form.html'
    fields = ['title', 'description', 'public']

class ModuleView(WhitelistRequiredMixin, DetailView):
    model = Module
    template_name = 'module.html'

    def get(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, slug=kwargs['project_slug'])
        return super(ModuleView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModuleView, self).get_context_data(**kwargs)
        context['lessons'] = self.get_object().lessons.all().order_by('order')
        context['project'] = self.project
        return context


class LessonView(WhitelistRequiredMixin, DetailView):
    model = Lesson
    template_name = 'lesson.html'
    context_object_name = 'lesson'
    project = None
    module = None

    def get(self, request, *args, **kwargs):
        try:
            self.project = Project.objects.get(slug=kwargs['project_slug'])
            self.module = Module.objects.get(pk=kwargs['module_id'])
        except:
            pass
        return super(LessonView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LessonView, self).get_context_data(**kwargs)
        context['sections'] = self.get_object().sections.all()

        try:
            context['project'] = self.project
            context['module'] = self.module
        except:
            print 'no project'
            pass

        try:
            context['quiz'] = self.get_object().lesson_quiz.get().quiz
        except:
            pass
        
        try:
            context['curr_section'] = self.kwargs['section']
        except:
            context['curr_section'] = 'topic'

        context['section_items'] = self.get_object().sections.filter(content_type=context['curr_section'])
        
        try:
            context['lesson_thread'] =  self.get_object().lesson_discussion.get().thread.id
            preview_replies = self.get_object().lesson_discussion.get().thread.replies.all().filter(deleted=False).order_by('-modified')
            context['lesson_thread_replies'] = preview_replies[0:1]
        except:
            context['lesson_thread'] = None

        # context['module_lessons'] = self.get_object().module.lessons.all()
        return context


class LessonViewPermLink(DetailView):
    model = Lesson
    template_name = 'lesson_permlink.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super(LessonViewPermLink, self).get_context_data(**kwargs)
        context['sections'] = self.get_object().sections.all()

        try:
            context['quiz'] = self.get_object().lesson_quiz.get().quiz
        except:
            pass
        
        try:
            context['curr_section'] = self.kwargs['section']
        except:
            context['curr_section'] = 'topic'

        context['section_items'] = self.get_object().sections.filter(content_type=context['curr_section'])
        
        try:
            context['lesson_thread'] =  self.get_object().lesson_discussion.get().thread.id
            preview_replies = self.get_object().lesson_discussion.get().thread.replies.all().filter(deleted=False).order_by('-modified')
            context['lesson_thread_replies'] = preview_replies[0:1]
        except:
            context['lesson_thread'] = None

        # context['module_lessons'] = self.get_object().module.lessons.all()
        return context 


class PbllPageView(DetailView):
    model = PbllPage
    template_name = "pbllpage.html"


class ModuleCreateView(LoginRequiredMixin, CreateView):
    model = Module
    template_name = "create_form.html"
    form_class = ModuleCreateForm
    project = None

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, slug=kwargs['project_slug'])
        return super(ModuleCreateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = self.initial.copy()
        initial['project'] = self.project
        return initial

    def get_context_data(self, **kwargs):
        context = super(ModuleCreateView, self).get_context_data(**kwargs)
        context['object_type'] = 'Module'
        return context


class ModuleUpdateView(LoginRequiredMixin, UpdateView):
    model = Module
    template_name = "edit_form.html"
    form_class = ModuleUpdateForm

    def get_context_data(self, **kwargs):
        context = super(ModuleUpdateView, self).get_context_data(**kwargs)
        context['object_type'] = 'Module'
        return context


class ModuleDeleteView(LoginRequiredMixin, DeleteView):
    model = Module
    template_name = 'generic_confirm_delete.html'

    def get_success_url(self):
        return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(ModuleDeleteView, self).get_context_data(**kwargs)
        context['object_type'] = 'Module'
        return context   


class LessonViewAll(ListView):
    model = Lesson
    template_name = 'lesson_list.html'
    context_object_name = 'lessons'

    def get_context_data(self, **kwargs):
        context = super(LessonViewAll, self).get_context_data(**kwargs)
        lesson_list = {}
        for lesson in context['lessons']:
            lesson_modules = [m for m in lesson.modules.all()]
            related_projects = {}
            for lesson_module in lesson_modules:
                try:
                    related_projects[lesson_module.module.project].append(lesson_module.module)
                except:
                    related_projects[lesson_module.module.project] = [lesson_module.module]
            lesson_list[lesson] = {'object': lesson, 'related_projects': related_projects}

        context['lesson_list'] = lesson_list
        return context


class LessonCreateView(LoginRequiredMixin, CreateView):
    model = Lesson
    template_name = "create_lesson_form.html"
    form_class = LessonCreateForm
    project_context = None
    module_context = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.project_context = Project.objects.get(slug=self.request.GET.get('project'))
            self.module_context = Module.objects.get(pk=self.request.GET.get('module'))
        except:
            pass  # Request url does not indicate project/module query parameters

        return super(LessonCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):

        if self.project_context and self.module_context:
            return (reverse('lesson', args=[self.project_context.slug, self.module_context.id, self.object.id]))
        return super(LessonUpdateView, self).get_success_url()


    def get_form(self, form_class):
        form_obj = form_class(**self.get_form_kwargs())

        if not self.module_context:
            form_obj.fields['order_in_module'].widget = forms.HiddenInput()
        
        return form_obj

    def get_initial(self):
        initial = self.initial.copy()
        initial['creator'] = self.request.user
        if self.module_context:
            initial['module'] = self.module_context
        else:
            print self.fields
        return initial

    def form_valid(self, form):
        """
        Called if all forms are valid. Creates a lesson instance along with
        a LessonModule instance.
        """
        self.object = form.save()

        if self.module_context:
            module_obj = form.cleaned_data['module']
            order_in_module = form.cleaned_data['order_in_module']
            lesson_module = LessonModule(module=module_obj, lesson=self.object, order=order_in_module)
            lesson_module.save()

        return super(LessonCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LessonCreateView, self).get_context_data(**kwargs)
        context['object_type'] = 'Lesson'
        context['module'] = self.module_context
        return context


class LessonModuleCreatePairView(LoginRequiredMixin, CreateView):
    model = LessonModule
    template_name = 'create_lesson_module_pair_form.html'
    form_class = LessonModuleCreateForm

    def dispatch(self, request, *args, **kwargs):
        try:
            # self.project_context = Project.objects.get(slug=self.request.GET.get('project'))
            self.module_context = Module.objects.get(pk=self.request.GET.get('module'))
        except:
            pass  # Request url does not indicate project/module query parameters

        return super(LessonModuleCreatePairView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = self.initial.copy()
        if self.module_context:
            initial['module'] = self.module_context
        return initial

    def get_success_url(self):
        return (reverse('module', args=[self.object.module.project.slug, self.object.module.id]))

    def get_context_data(self, **kwargs):
        context = super(LessonModuleCreatePairView, self).get_context_data(**kwargs)
        context['object_type'] = 'Lesson'
        context['module'] = self.module_context
        return context


class LessonUpdateView(LoginRequiredMixin, UpdateView):
    model = Lesson
    template_name = "edit_form.html"
    form_class = LessonUpdateForm
    project_context = None
    module_context = None
    lesson_module = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.module_context = Module.objects.get(pk=self.request.GET.get('module'))
            self.project_context = self.module_context.project
            self.lesson_module = LessonModule.objects.filter(module=self.module_context).get(lesson=self.get_object())
        except Exception as e:
            pass  # Request url does not indicate project/module query parameters

        return super(LessonUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.project_context and self.module_context:
            return reverse('lesson', args=[self.project_context.slug, self.module_context.id, self.object.id])
        return super(LessonUpdateView, self).get_success_url() 

    def get_form(self, form_class):
        form_obj = form_class(**self.get_form_kwargs())

        if not self.module_context:
            form_obj.fields.pop('order_in_module')
            form_obj.fields.pop('lesson_module_obj')
        
        return form_obj

    def get_initial(self):
        initial = self.initial.copy()
        initial['creator'] = self.request.user

        if self.lesson_module:
            initial['order_in_module'] = self.lesson_module.order
            initial['lesson_module_obj'] = self.lesson_module

        return initial

    def form_valid(self, form):
        """
        Called if all forms are valid. Updates the order field for module/lesson pairs.
        """
        self.object = form.save()
        try:
            lesson_module = form.cleaned_data['lesson_module_obj']
            if lesson_module:
                lesson_module.order = form.cleaned_data['order_in_module']
                lesson_module.save()
        except:
            pass

        return super(LessonUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LessonUpdateView, self).get_context_data(**kwargs)
        context['object_type'] = 'Lesson'
        return context


class LessonDeleteView(LoginRequiredMixin, DeleteView):
    model = Lesson
    template_name = 'generic_confirm_delete.html'

    def get_success_url(self):
        return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(LessonDeleteView, self).get_context_data(**kwargs)
        context['object_type'] = 'Lesson'
        return context


class LessonModuleDeletePairView(LoginRequiredMixin, DeleteView):
    model = LessonModule
    template_name = 'lesson_module_confirm_delete.html'

    def get_success_url(self):
        return (reverse('module', args=[self.object.module.project.slug, self.object.module.id]))

    def get_context_data(self, **kwargs):
        context = super(LessonModuleDeletePairView, self).get_context_data(**kwargs)
        context['object_type'] = 'Lesson'
        return context    


class LessonSectionUpdateView(LoginRequiredMixin, UpdateView):
    model = LessonSection
    template_name = "edit_form.html"
    form_class = LessonSectionUpdateForm

    def dispatch(self, request, *args, **kwargs):

        return super(LessonSectionUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        try:
            self.module_context = Module.objects.get(pk=self.request.GET.get('module'))
            self.project_context = self.module_context.project
            self.lesson_context = Lesson.objects.get(pk=self.request.GET.get('lesson'))
            
            return reverse('lesson_section', args=[self.project_context.slug, self.module_context.id, self.lesson_context.id, self.get_object().content_type])
            
        except Exception as e:        
            return super(LessonSectionUpdateView, self).get_success_url() 

    def get_context_data(self, **kwargs):
        context = super(LessonSectionUpdateView, self).get_context_data(**kwargs)
        context['object_type'] = self.get_object().content_type
        context['filelisting'] = FileListing('uploads', sorting_by='date', sorting_order='desc').listing

        return context


class LessonQuizQuestionListView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = 'question_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(LessonQuizQuestionListView, self).get_context_data(**kwargs)
        context['questions'] = self.get_object().get_questions()
        context['lesson'] = get_object_or_404(LessonQuiz, quiz=self.get_object()).lesson
        return context


class LessonQuizQuestionDetailView(LoginRequiredMixin, DetailView):
    model = MCQuestion
    template_name = 'question_preview.html'
    lesson = None
    quiz = None

    def get_context_data(self, **kwargs):
        context = super(LessonQuizQuestionDetailView, self).get_context_data(**kwargs)
        context['answers'] = Answer.objects.filter(question=self.get_object())
        context['quiz'] = self.get_object().quiz.all().get()
        context['lesson'] = get_object_or_404(LessonQuiz, quiz=context['quiz']).lesson
        return context


class LessonQuizQuestionCreateView(LoginRequiredMixin, CreateView):
    model = MCQuestion
    template_name = 'question_create_form.html'
    form_class = LessonQuizQuestionCreateForm
    lesson = None
    quiz = None

    def dispatch(self, request, *args, **kwargs):
        self.quiz = Quiz.objects.filter(pk=kwargs['quiz_id'])
        self.lesson = get_object_or_404(LessonQuiz, quiz=self.quiz.get()).lesson
        return super(LessonQuizQuestionCreateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = self.initial.copy()
        initial['quiz'] = self.quiz
        return initial

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        answers_form = AnswersCreateFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, answers_form=answers_form, quiz=self.quiz, lesson=self.lesson))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        answers_form = AnswersCreateFormSet(self.request.POST)
        
        if form.is_valid() and answers_form.is_valid():
            return self.form_valid(form, answers_form)
        else:
            return self.form_invalid(form, answers_form)

    def form_valid(self, form, answers_form):
        """
        Called if all forms are valid. Creates a MCQuestion instance along with
        associated Answers and then redirects to success_url. All Sittings for the question
        quiz are reset.
        """
        self.object = form.save()
        answers_form.instance = self.object
        answers_form.save()
        sittings = Sitting.objects.filter(quiz=self.quiz)
        for i in sittings: 
            i.mark_quiz_complete()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, answers_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form, answers_form=answers_form, quiz=self.quiz, lesson=self.lesson))


class LessonQuizQuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = MCQuestion
    template_name = 'question_update_form.html'
    form_class = LessonQuizQuestionCreateForm
    lesson = None
    quiz = None

    def dispatch(self, request, *args, **kwargs):
        self.quiz = Quiz.objects.filter(pk=kwargs['quiz_id'])
        self.lesson = get_object_or_404(LessonQuiz, quiz=self.quiz.get()).lesson
        return super(LessonQuizQuestionUpdateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates the form
        and its inline formsets with existing data.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        answers_form = AnswersUpdateFormSet(instance=self.get_object())
        
        return self.render_to_response(
            self.get_context_data(form=form, answers_form=answers_form, quiz=self.quiz, lesson=self.lesson))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        answers_form = AnswersUpdateFormSet(instance=self.object, data=self.request.POST)
        
        if form.is_valid() and answers_form.is_valid():
            return self.form_valid(form, answers_form)
        else:
            return self.form_invalid(form, answers_form)

    def form_valid(self, form, answers_form):
        """
        Called if all forms are valid. Saves a MCQuestion instance along with
        associated Answers and then redirects to success_url.
        """
        self.object = form.save()
        answers_form.instance = self.object
        answers_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, answers_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form, answers_form=answers_form, quiz=self.quiz, lesson=self.lesson))


class LessonQuizQuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = MCQuestion
    template_name = 'generic_confirm_delete.html'

    def get_success_url(self):
        # remove the sittings for this quiz and return user back quiz question list.
        try:
            quiz = self.get_object().quiz.all()[0]
            Sitting.objects.filter(quiz=quiz).delete()
            return quiz.get_absolute_url()
        except:
            return reverse('home')

    def get_context_data(self, **kwargs):
        context = super(LessonQuizQuestionDeleteView, self).get_context_data(**kwargs)
        context['object_type'] = 'Quiz Question'
        return context    


class LoginForbiddenView(TemplateView):
    template_name = 'login-forbidden.html'


class MembershipAccessErrorView(TemplateView):
    template_name = 'membership-error.html'


class PbllPageUpdateView(LoginRequiredMixin, UpdateView):
    model = PbllPage
    template_name = "edit_form.html"
    form_class = PbllPageUpdateForm

    def get_context_data(self, **kwargs):
        context = super(PbllPageUpdateView, self).get_context_data(**kwargs)
        context['object_type'] = 'Generic Page'
        return context

