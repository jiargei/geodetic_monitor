from django.views import generic
from django.core.urlresolvers import reverse

from accounts.views import ProjectMixin

from ..models import Position
from ..forms import position as forms


class PositionMixin(ProjectMixin):
    pk_url_kwarg = 'position_id'

    def get_queryset(self, *args, **kwargs):
        return Position.objects.filter(project=self.membership.project)

    def get_form_kwargs(self, *args, **kwargs):
        params = super(PositionMixin, self).get_form_kwargs(*args, **kwargs)
        params.update({'membership': self.membership})
        return params

    def get_success_url(self, *args, **kwargs):
        return reverse(
            'position-list',
            kwargs={'project_id': self.membership.project_id}
        )


class List(PositionMixin, generic.ListView):
    template_name = 'metering/position/list.html'


class Update(PositionMixin, generic.UpdateView):
    form_class = forms.Update
    template_name = 'metering/position/update.html'


class Create(PositionMixin, generic.CreateView):
    form_class = forms.Create
    template_name = 'metering/position/create.html'


class Delete(PositionMixin, generic.DeleteView):
    template_name = 'metering/position/confirm_delete.html'
