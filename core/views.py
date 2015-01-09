from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy

from django.views.generic import FormView

from core.models import Whitelist
from .forms import HonorCodeForm



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
