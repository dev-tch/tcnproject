#from .serializers import WindowSerializer, CustomUserSerializer, OfficeSerializer
from .models import Window, CustomUser, Office, CounterNotify
from rest_framework import status as restHttpCodes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404
# =================start  websocket
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# =================end   websocket
from django.db.models import F

@api_view(['GET'])
def status(request):
    return Response({"message": "api works well"})

@api_view(['POST'])
def assign_agent_to_window(request, number_window):
    # control the required fields 
    if not number_window:
        return Response({"error": "num_window is required"},
                        status=restHttpCodes.HTTP_400_BAD_REQUEST)
    agent_id = request.data.get('agent_id')
    office_id = request.data.get('office_id')
    if not agent_id or not office_id:
        return Response({"error": "agent_id and office_id are required"}, status=restHttpCodes.HTTP_400_BAD_REQUEST)

    try:
        agent_id = int(agent_id)
    except ValueError:
        return Response({"error": "agent_id must be integer"},
                        status=status.HTTP_400_BAD_REQUEST)
    # delete agent  from others windows
    try:
        with transaction.atomic():  # Ensure transactional integrity
            Window.objects.filter(agent_id=agent_id).delete()
            try: 
                window = Window.objects.get(pk=number_window)
                window.agent_id = agent_id
                window.office_id = office_id
                window.save()
                json_data = {"message": "Agent assigned to existing window successfully"}
                return Response(json_data, status=restHttpCodes.HTTP_200_OK)
            except (Window.DoesNotExist):
                Window.objects.create(number_window=number_window, agent_id=agent_id, office_id=office_id)
                json_data = {"message": "Agent assigned to new window successfully"}
                return Response(json_data, status=restHttpCodes.HTTP_201_CREATED)
    except Exception as e:  
        return Response({"error": str(e)}, status=restHttpCodes.HTTP_500_INTERNAL_SERVER_ERROR)

# agent api increment counter 
@api_view(['POST'])
def increment_counter(request, ref_office):
    # control fields 
    if not ref_office:
        return Response({"error": "ref_office is required"},
                        status=restHttpCodes.HTTP_400_BAD_REQUEST)
    # get agent_id and number_window from body request 
    agent_id = request.data.get('agent_id')
    number_window = request.data.get('number_window')
    if not agent_id or not number_window:
        return Response({"error": "agent_id and number_window are required"}, status=restHttpCodes.HTTP_400_BAD_REQUEST)
    # get the  office instanse 
    try: 
        office = Office.objects.get(pk=ref_office)
        agent  = CustomUser.objects.get(pk=agent_id)
        window  = Window.objects.get(pk=number_window, agent_id=agent.id)
        #init counter 
        office.counter = F('counter') + 1
        office.save()
        window.number_of_served_tickets = F('number_of_served_tickets') + 1 
        window.save()
        office.refresh_from_db()
        # Notify WebSocket clients about the counter update
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'counter_group',
            {
                'type': 'counter_update',
                'counter': office.counter
            }
        )
    #exceptions = (Office.DoesNotExist, CustomUser.DoesNotExist, Window.DoesNotExist)
    except Office.DoesNotExist:  
        return Response({"error": f"office {ref_office} not found"}, status=restHttpCodes.HTTP_404_NOT_FOUND)
    except CustomUser.DoesNotExist:
        return Response({"error": f"agent  {agent_id} not found"}, status=restHttpCodes.HTTP_404_NOT_FOUND)
    except Window.DoesNotExist:
        return Response({"error": f"window  {number_window} not found"}, status=restHttpCodes.HTTP_404_NOT_FOUND)
  
    return Response({'counter': office.counter})

@api_view(['POST'])
def apply_notify_with_action(request, id_user, action):
    # check validity data of request 
    if not id_user:
        return Response({"error": "No id_user provided"}, status=restHttpCodes.HTTP_400_BAD_REQUEST)
    try:
        id_user = int(id_user)
    except ValueError:
        return Response({"error": "id_user is not an integer"}, status=restHttpCodes.HTTP_400_BAD_REQUEST)
    ref_offices = request.data.get('ref_offices', [])
    if not ref_offices:
        return Response({"error": "No ref_offices provided"}, status=restHttpCodes.HTTP_400_BAD_REQUEST)
    if not isinstance(ref_offices, list):
        return Response({"error": "ref_offices is not a list"}, status=restHttpCodes.HTTP_400_BAD_REQUEST)
    if not action: 
        return Response({"error": "No is_enabled provided"}, status=restHttpCodes.HTTP_400_BAD_REQUEST)

    if not action in ['enable', 'disable']:
        return Response({"error": "action must be  in [enable, disable] "}, status=restHttpCodes.HTTP_400_BAD_REQUEST)
    is_enabled  = True if action == "enable" else False
    # if check data requit is valid we start the process 
    offices = Office.objects.filter(ref__in=ref_offices)
    try:
        with transaction.atomic():  # Ensure transactional integrity
            user = get_object_or_404(CustomUser, pk=id_user)
            for office in offices:
                counternotify, _ = CounterNotify.objects.get_or_create(client_id = user.id, office_id = office.ref)
                counternotify.is_enabled = is_enabled
                counternotify.save()
    except Exception as e:  
        return Response({"error": str(e)}, status=restHttpCodes.HTTP_500_INTERNAL_SERVER_ERROR)
    json_data = {"message": "no action applied was provided"}
    if action == "enable":
        json_data = {"message": "enable notifications for offices applied successfully"}
    if action == "disable":
        json_data = {"message": "disable notifications for offices applied successfully"}
    return Response(json_data, status=restHttpCodes.HTTP_200_OK)
