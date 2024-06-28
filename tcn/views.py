#from django.contrib.auth.forms import UserCreationForm
from django.db.models import F, Count, Case, When, IntegerField
from .forms import CustomUserCreationForm
from .manager_forms import OfficeCreationForm
from django.urls import reverse_lazy
#from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from .models import Office, CustomUser
# =================start  websocket
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# =================end   websocket
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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

#class CreateOfficeView
class CreateOfficeView(FormView):
    #form_class = UserCreationForm
    form_class = OfficeCreationForm
    success_url = reverse_lazy("tcn:home")
    template_name = "tcn/create_office.html"
    """
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    """
    def form_valid(self, form):
        # override the manager office
        # when signup manager acces with default office 
        # it must join the new office created 
        user = self.request.user
        if user.is_authenticated and user.role == 'manager':
            if user.office_id and user.office_id != 'guest':
                # Display error in the template
                form.add_error(None, "Manager is already associated with an office.")
                return self.form_invalid(form)
            office_instance = form.save()
            user.office_id = office_instance.ref
            user.save()
        return super().form_valid(form)
    
class ListOffices(ListView):
    model = Office
    template_name = "tcn/list_offices.html"
    def get_queryset(self):
        # authenticated manager 
        manager_user = self.request.user
        # get the office linked to authenticated manager but not guest office 
        offices = Office.objects.filter(users__username=manager_user.username).exclude(ref='guest')
        return offices

class ListAgents(ListView):
    model = CustomUser
    template_name = "tcn/list_agents.html"
    context_object_name = "agent_list"
    def get_queryset(self):
        """Return the last five published questions."""
        manager_user = self.request.user
        
        # Assuming manager_user.role == 'manager', get their associated office_id
        manager_office_id = manager_user.office_id  # Adjust this according to your actual field name

        # Filter agents linked to the manager's office
        #agents = CustomUser.objects.filter(role='agent', office_id=manager_office_id)
        agents = CustomUser.objects.filter(role='agent', office_id=manager_office_id).annotate(
        agent_id=F('pk'),
        number_of_windows=F('office__number_of_windows'),
        num_window=Case(
            When(window__agent_id=F('pk'), then=F('window__number_window')),
            default=0,
            output_field=IntegerField(),
        )
        ).order_by('pk')
        
        return agents

counter = 0  # Example counter (should ideally be stored in a database)
@csrf_exempt  # To bypass CSRF protection for this view
@require_POST  # Ensures the view only responds to POST requests
def increment_counter(request):
    global counter
    counter += 1

    # Notify WebSocket clients about the counter update
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'counter_group',
        {
            'type': 'counter_update',
            'counter': counter
        }
    )
    return JsonResponse({'counter': counter})