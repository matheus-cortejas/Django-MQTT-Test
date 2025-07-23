from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SensorDataSerializer
from .models import SensorData
from core.mqtt_service import publish_to_mqtt

class SensorDataAPI(APIView):
    def post(self, request):
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            # Salva os dados
            sensor_data = serializer.save()
            
            # Publica no broker MQTT
            publish_to_mqtt(
                topic=f"sensors/{sensor_data.sensor_id}/data",
                payload=serializer.data
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        # Retorna o último dado do sensor
        latest = SensorData.objects.order_by('-timestamp').first()
        if latest:
            serializer = SensorDataSerializer(latest)
            return Response(serializer.data)
        return Response({'detail': 'Nenhum dado disponível'}, status=status.HTTP_404_NOT_FOUND)
