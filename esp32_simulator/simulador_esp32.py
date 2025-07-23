import requests
import json
import time
import threading

# Configurações
DJANGO_API_URL = "http://localhost:8000/api/sensor-data/"
BROKER_URL = "mqtt://localhost:1883"
SENSOR_ID = "simulated_esp32"

def send_to_django(temperature, humidity):
    payload = {
        "sensor_id": SENSOR_ID,
        "temperature": temperature,
        "humidity": humidity
    }
    try:
        response = requests.post(
            DJANGO_API_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5  # Adiciona timeout
        )
        print(f"Django response: {response.status_code}")
        if response.status_code == 201:
            print(f"✓ Dados enviados: Temp={temperature}°C, Humidity={humidity}%")
        return response.status_code == 201
    except Exception as e:
        print(f"✗ Erro ao enviar para Django: {str(e)}")
        return False

def main():
    print("Simulador ESP32 - Digite valores (Enter para manter anteriores, 'q' para sair)")
    last_temp, last_humidity = 25.0, 60.0
    
    while True:
        try:
            print(f"\nValores atuais: Temp={last_temp}°C, Humidity={last_humidity}%")
            
            temp_input = input("Nova temperatura (ou Enter): ").strip()
            if temp_input.lower() == 'q':
                break
                
            humidity_input = input("Nova umidade (ou Enter): ").strip()
            if humidity_input.lower() == 'q':
                break
            
            # Atualiza valores
            temp = float(temp_input) if temp_input else last_temp
            humidity = float(humidity_input) if humidity_input else last_humidity
            
            # Envia dados
            send_to_django(temp, humidity)
            last_temp, last_humidity = temp, humidity
                
        except ValueError:
            print("⚠ Erro: Valores devem ser números")
        except KeyboardInterrupt:
            print("\n👋 Simulador encerrado")
            break

if __name__ == "__main__":
    main()