from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

from .models import TachyTarget
from csvImporter.model import CsvDbModel

# Create your views here.

# Imaginary function to handle an uploaded file.


class TachyTargetCsvModel(CsvDbModel):

    class Meta:
        dbModel = TachyTarget
        delimiter = ";"


def handle_uploaded_file(f):
    csv_list = TachyTargetCsvModel.import_data(data=open(f))


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
