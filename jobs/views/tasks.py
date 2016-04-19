from django.views import generic
from django.core.urlresolvers import reverse

from accounts.views import ProjectMixin

from ..models import Task
from ..forms import task as forms


class TaskMixin(ProjectMixin):
    pk_url_kwarg = 'task_id'

    def get_queryset(self, *args, **kwargs):
        return Task.objects.filter(project=self.membership.project)

    def get_form_kwargs(self, *args, **kwargs):
        params = super(TaskMixin, self).get_form_kwargs(*args, **kwargs)
        params.update({'membership': self.membership})
        return params

    def get_success_url(self, *args, **kwargs):
        return reverse(
            'task-list',
            kwargs={'project_id': self.membership.project_id}
        )


class List(TaskMixin, generic.ListView):
    template_name = 'jobs/task/list.html'


class Update(TaskMixin, generic.UpdateView):
    form_class = forms.Update
    template_name = 'jobs/task/update.html'


class Create(TaskMixin, generic.CreateView):
    form_class = forms.Create
    template_name = 'jobs/task/create.html'


class Delete(TaskMixin, generic.DeleteView):
    template_name = 'jobs/task/confirm_delete.html'
