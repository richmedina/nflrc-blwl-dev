from django.views.generic import TemplateView, DetailView

from .models import Module, Lesson

class HomeView(TemplateView):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['modules'] = Module.objects.all()
		return context

class ModuleView(DetailView):
	model = Module
	template_name = 'module.html'

	def get_context_data(self, **kwargs):
		context = super(ModuleView, self).get_context_data(**kwargs)
		context['lessons'] = self.get_object().lessons.all()
		return context

class LessonView(DetailView):
	model = Lesson
	template_name = 'lesson.html'
	context_object_name = 'lesson'

	def get_context_data(self, **kwargs):
		context = super(LessonView, self).get_context_data(**kwargs)
		
		try:
			quiz_url = self.get_object().lesson_quiz.get().quiz.url
			context['quiz'] =  quiz_url
		except:
			pass
		try: 
			context['section'] = self.kwargs['section']
		except:
			context['section'] = 'topic'
		 
		context['discussion'] = ""
		print self.get_object().module.lessons.all()
		

		return context

class IsotopeView(TemplateView):
	template_name = 'isotope_scratch.html'
