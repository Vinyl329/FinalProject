from .models import Response, Subclass
from django_filters import FilterSet, ModelChoiceFilter


class SubclassFilter(FilterSet):
    class Meta:
        model = Response
        fields = ['response_subclass']

    def __init__(self, *args, **kwargs):
        super(SubclassFilter, self).__init__(*args, **kwargs)
        self.filters['response_subclass'].queryset = Response.objects.filter(author_id=kwargs['request'])