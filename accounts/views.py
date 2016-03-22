from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from .models import Project, Membership


class ProjectMixin(LoginRequiredMixin):
    """Mixin for all project-based views

    checks if an user is logged in and a member of the project
    referenced by <project_id> in the url"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            try:
                self.membership = request.user.memberships.select_related(
                    'project'
                ).get(
                    project_id=self.kwargs['project_id']
                )
            except Membership.DoesNotExist:
                # TODO: if you want to hide the existence of the project
                # rather raise a 404
                raise PermissionDenied('Not a member of this project')
        return super(ProjectMixin, self).dispatch(request, *args, **kwargs)


class ProjectDetail(ProjectMixin, generic.DetailView):
    pk_url_kwarg = 'project_id'
    model = Project
