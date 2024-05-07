from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from FantasyWorld.models import Response, Subclass
from django_filters import FilterSet, ModelChoiceFilter
from FantasyWorld.filters import SubclassFilter


class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Response.objects.filter(response_subclass__author__id=self.request.user.id)
        context['filterset'] = SubclassFilter(self.request.GET, request=self.request.user.id)
        return context