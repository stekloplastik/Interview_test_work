from django.http import JsonResponse
from django.shortcuts import redirect

from promo.forms import PromoGenerationForm
from django.views.generic.edit import FormView

# Create your views here.


class PromoGenerationView(FormView):

    template_name = 'promo/promo.html'
    form_class = PromoGenerationForm
    success_url = '/'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        form.generate()
        return super().form_valid(form)
