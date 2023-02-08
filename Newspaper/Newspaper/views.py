from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.utils.translation import gettext as _


class CorePage(View):
    def get(self, request):
        string = _('Welcome to News portal')

        return HttpResponse(string)

