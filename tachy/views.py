from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

from .models import TachyTarget
from csvImporter.model import CsvDbModel
from django.views.generic.edit import FormView
from tachy.forms import TachyControlForm

# Create your views here.

# Imaginary function to handle an uploaded file.


class TachyControlView(FormView):
    template_name = 'tachy/control.html'
    form_class = TachyControlForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.execute()
        return super(TachyControlView, self).form_valid(form)
