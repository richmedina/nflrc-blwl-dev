from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, FormView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django import forms

from braces.views import LoginRequiredMixin
from filebrowser.sites import site
from filebrowser.base import FileListing

from core.mixins import HonorCodeRequired
from quiz.models import Quiz
from multichoice.models import MCQuestion, Answer
from .models import Module, Lesson, LessonSection, LessonQuiz, PbllPage
from .forms import ModuleUpdateForm, ModuleCreateForm, LessonCreateForm, LessonUpdateForm, LessonSectionUpdateForm, LessonQuizQuestionCreateForm, AnswersFormSet, PbllPageUpdateForm

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['pbllpage'] = PbllPage.objects.get(pk=1)
        context['modules'] = Module.objects.all()
        return context

class ModuleView(LoginRequiredMixin, HonorCodeRequired, DetailView):
    model = Module
    template_name = 'module.html'

    def get_context_data(self, **kwargs):
        context = super(ModuleView, self).get_context_data(**kwargs)
        context['lessons'] = self.get_object().lessons.all()
        return context

class LessonView(LoginRequiredMixin, HonorCodeRequired, DetailView):
    model = Lesson
    template_name = 'lesson.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super(LessonView, self).get_context_data(**kwargs)
        context['sections'] = self.get_object().sections.all()
        try:
            quiz_url = self.get_object().lesson_quiz.get().quiz.url
            context['quiz'] =  quiz_url
        except:
            pass
        
        try:
            context['curr_section'] = self.kwargs['section']
        except:
            context['curr_section'] = 'topic'

        context['section_items'] = self.get_object().sections.filter(content_type=context['curr_section'])
        
        try:
            context['lesson_thread'] =  self.get_object().lesson_discussion.get().thread.slug
            preview_replies = self.get_object().lesson_discussion.get().thread.replies.all().filter(deleted=False).order_by('-modified')
            context['lesson_thread_replies'] = preview_replies[0:1]
        except:
            context['lesson_thread'] = None

        context['module_lessons'] = self.get_object().module.lessons.all()
        return context

class PbllPageView(DetailView):
    model = PbllPage
    template_name = "pbllpage.html"


class ModuleCreateView(LoginRequiredMixin, HonorCodeRequired, CreateView):
    model = Module
    template_name = "create_form.html"
    form_class = ModuleCreateForm

    def get_context_data(self, **kwargs):
        context = super(ModuleCreateView, self).get_context_data(**kwargs)
        context['object_type'] = 'Module'
        return context

class ModuleUpdateView(LoginRequiredMixin, HonorCodeRequired, UpdateView):
    model = Module
    template_name = "edit_form.html"
    form_class = ModuleUpdateForm

    def get_context_data(self, **kwargs):
        context = super(ModuleUpdateView, self).get_context_data(**kwargs)
        context['object_type'] = 'Module'
        return context


class LessonCreateView(LoginRequiredMixin, HonorCodeRequired, CreateView):
    model = Lesson
    template_name = "create_form.html"
    form_class = LessonCreateForm

    def get_context_data(self, **kwargs):
        context = super(LessonCreateView, self).get_context_data(**kwargs)
        context['object_type'] = 'Lesson'
        return context


class LessonUpdateView(LoginRequiredMixin, HonorCodeRequired, UpdateView):
    model = Lesson
    template_name = "edit_form.html"
    form_class = LessonUpdateForm

    def get_context_data(self, **kwargs):
        context = super(LessonUpdateView, self).get_context_data(**kwargs)
        context['object_type'] = 'Lesson'
        return context

class LessonSectionUpdateView(LoginRequiredMixin, HonorCodeRequired, UpdateView):
    model = LessonSection
    template_name = "edit_form.html"
    form_class = LessonSectionUpdateForm

    def get_context_data(self, **kwargs):
        context = super(LessonSectionUpdateView, self).get_context_data(**kwargs)
        context['object_type'] = self.get_object().content_type
        context['filelisting'] = FileListing('uploads', sorting_by='date', sorting_order='desc').listing

        return context

class LessonQuizQuestionDetailView(LoginRequiredMixin, HonorCodeRequired, DetailView):
    model = MCQuestion
    template_name = 'question_preview.html'
    lesson = None
    quiz = None

    # def dispatch(self, request, *args, **kwargs):
    #     self.quiz = self.get_object().quiz.all().get()
    #     self.lesson = get_object_or_404(LessonQuiz, quiz=self.quiz).lesson
    #     return super(LessonQuizQuestionDetailView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(LessonQuizQuestionDetailView, self).get_context_data(**kwargs)
        context['answers'] = self.get_object().get_answers_list()
        context['quiz'] = self.get_object().quiz.all().get()
        context['lesson'] = get_object_or_404(LessonQuiz, quiz=context['quiz']).lesson
        return context

class LessonQuizQuestionCreateView(LoginRequiredMixin, HonorCodeRequired, CreateView):
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
        answers_form = AnswersFormSet()
        
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
        answers_form = AnswersFormSet(self.request.POST)
        
        if form.is_valid() and answers_form.is_valid():
            return self.form_valid(form, answers_form)
        else:
            return self.form_invalid(form, answers_form)

    def form_valid(self, form, answers_form):
        """
        Called if all forms are valid. Creates a MCQuestion instance along with
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


class LessonQuizQuestionUpdateView(LoginRequiredMixin, HonorCodeRequired, UpdateView):
    model = MCQuestion
    template_name = 'question_update_form.html'
    form_class = LessonQuizQuestionCreateForm
    lesson = None
    quiz = None

    def dispatch(self, request, *args, **kwargs):
        self.quiz = Quiz.objects.filter(pk=kwargs['quiz_id'])
        self.lesson = get_object_or_404(LessonQuiz, quiz=self.quiz.get()).lesson
        return super(LessonQuizQuestionUpdateView, self).dispatch(request, *args, **kwargs)

    # def get_initial(self):
    #     initial = self.initial.copy()
    #     initial['quiz'] = self.quiz
    #     return initial

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        answers_form = AnswersFormSet(instance=self.get_object())
        
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
        answers_form = AnswersFormSet(self.request.POST)
        
        if form.is_valid() and answers_form.is_valid():
            return self.form_valid(form, answers_form)
        else:
            return self.form_invalid(form, answers_form)

    def form_valid(self, form, answers_form):
        """
        Called if all forms are valid. Creates a MCQuestion instance along with
        associated Answers and then redirects to success_url.
        """
        # self.object = form.save()
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

class LoginForbiddenView(TemplateView):
    template_name = 'login-forbidden.html'

class PbllPageUpdateView(LoginRequiredMixin, HonorCodeRequired, UpdateView):
    model = PbllPage
    template_name = "edit_form.html"
    form_class = PbllPageUpdateForm

    def get_context_data(self, **kwargs):
        context = super(PbllPageUpdateView, self).get_context_data(**kwargs)
        context['object_type'] = 'Generic Page'
        return context

