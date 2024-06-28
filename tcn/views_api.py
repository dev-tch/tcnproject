from .serializers import WindowSerializer, CustomUserSerializer, OfficeSerializer
from .models import Window, CustomUser, Office
from rest_framework import status as restHttpCodes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction

@api_view(['GET'])
def status(request):
    return Response({"message": "api works well"})

@api_view(['POST'])
def assign_agent_to_window(request, number_window):
    print(number_window)
    print("enter assign api")
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
