from django import forms

from ..models import Task


class Update(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('start_time', 'end_time', 'active', 'day_of_week', )

    def __init__(self, *args, **kwargs):
        self.membership = kwargs.pop('membership', None)
        super(Update, self).__init__(*args, **kwargs)


class Create(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('start_time', 'end_time', 'active', 'day_of_week', )

    def __init__(self, *args, **kwargs):
        self.membership = kwargs.pop('membership', None)
        super(Create, self).__init__(*args, **kwargs)
        self.instance.project = self.membership.project
        self.instance.creator = self.membership.user
