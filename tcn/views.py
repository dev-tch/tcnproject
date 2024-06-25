#from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
#from django.views.generic import CreateView
from django.views.generic.edit import FormView

#class SignUpView(CreateView):
class SignUpView(FormView):
    #form_class = UserCreationForm
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("tcn:login")
    template_name = "tcn/registration/signup.html"
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
