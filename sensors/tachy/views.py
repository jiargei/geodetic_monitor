from django.views.generic.edit import FormView

from sensors.tachy.forms import TachyControlForm


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
