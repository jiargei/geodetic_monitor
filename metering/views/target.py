from django.views import generic
from django.core.urlresolvers import reverse

from accounts.views import ProjectMixin

from ..models import Target
from ..forms import target as forms


class TargetMixin(ProjectMixin):
    pk_url_kwarg = 'target_id'

    def get_queryset(self, *args, **kwargs):
        return Target.objects.filter(project=self.membership.project)

    def get_form_kwargs(self, *args, **kwargs):
        params = super(TargetMixin, self).get_form_kwargs(*args, **kwargs)
        params.update({'membership': self.membership})
        return params

    def get_success_url(self, *args, **kwargs):
        return reverse(
            'target-list',
            kwargs={'project_id': self.membership.project_id}
        )


class List(TargetMixin, generic.ListView):
    template_name = 'metering/target/list.html'


class Update(TargetMixin, generic.UpdateView):
    form_class = forms.Update
    template_name = 'metering/target/update.html'


class Create(TargetMixin, generic.CreateView):
    form_class = forms.Create
    template_name = 'metering/target/create.html'


class Delete(TargetMixin, generic.DeleteView):
    template_name = 'metering/target/confirm_delete.html'
