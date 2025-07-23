from django.shortcuts import render
from api_app.models import SensorData

def dashboard(request):
    # Pega os últimos dados do sensor
    latest_data = SensorData.objects.order_by('-timestamp').first()
    return render(request, 'frontend/dashboard.html', {
        'latest_data': latest_data
    })