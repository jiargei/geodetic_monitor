from django import forms

from ..models import Position


class Update(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        self.membership = kwargs.pop('membership', None)
        super(Update, self).__init__(*args, **kwargs)


class Create(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        self.membership = kwargs.pop('membership', None)
        super(Create, self).__init__(*args, **kwargs)
        self.instance.project = self.membership.project
        self.instance.creator = self.membership.user
