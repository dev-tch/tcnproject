#from django.contrib.auth.forms import UserCreationForm
from django.db.models import F, Case, When, IntegerField
from .forms import CustomUserCreationForm
from .manager_forms import OfficeCreationForm
from django.urls import reverse_lazy
#from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from .models import Office, CustomUser, Window
from django.shortcuts import render


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
    
def index(request):
    # data context for agent interaface
    agent_user = None
    agent_window = None
    agent_office = None
    # data context for client  interaface
    offices = {}
    # data context for manager  interaface
    windows_office = {}
    # common variables 
    customuser = request.user
    context = {}
    if hasattr(customuser, 'role') and customuser.role == 'manager':
        # we need office_id to track windows
        office_manager = Office.objects.filter(users=customuser).exclude(ref='guest').first()
        windows_office = Window.objects.filter(office_id=office_manager.ref)
    elif hasattr(customuser, 'role') and  customuser.role == 'agent':
        # we need agent_id and office_id for service counter 
        agent_office = Office.objects.filter(users=customuser).exclude(ref='guest').first()
        agent_window = Window.objects.filter(agent_id=customuser.id, office_id=agent_office.ref).first()
        agent_user = CustomUser.objects.filter(pk=customuser.id).first()
        pass
    elif hasattr(customuser, 'role') and  customuser.role == 'client':
        offices = Office.objects.all().exclude(ref='guest')
    context = {"agent_user": agent_user,
               "agent_office": agent_office,
               "agent_window": agent_window,
               "offices": offices,
               "windows_office": windows_office}
    return render(request, "tcn/home.html", context)

class ListTrackedOffices(ListView):
    model = Office
    template_name = "tcn/list_offices_tracked.html"
    context_object_name = "list_tracked_offices"

    def get_queryset(self):
        """Return the last five published questions."""
        client_user = self.request.user
        offices = Office.objects.filter(counter_notifications__client=client_user, counter_notifications__is_enabled=True).exclude(ref='guest')
        return offices
