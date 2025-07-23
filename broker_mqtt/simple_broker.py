import asyncio
import json
import struct

class SimpleBroker:
    def __init__(self):
        self.clients = {}
        self.subscriptions = {}

    async def handle_connection(self, reader, writer):
        client_id = f"client_{id(writer)}"
        self.clients[client_id] = {'reader': reader, 'writer': writer}
        print(f"Cliente conectado: {client_id}")
        
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                
                await self.process_mqtt_message(client_id, data)
                
        except ConnectionResetError:
            pass
        finally:
            await self.disconnect_client(client_id)

    async def process_mqtt_message(self, client_id, data):
        try:
            # Decodifica dados básicos MQTT
            if len(data) < 2:
                return
                
            message_type = (data[0] >> 4) & 0x0F
            
            if message_type == 1:  # CONNECT
                await self.handle_connect(client_id)
            elif message_type == 8:  # SUBSCRIBE
                await self.handle_subscribe(client_id, data)
            elif message_type == 3:  # PUBLISH
                await self.handle_publish(client_id, data)
                
        except Exception as e:
            print(f"Erro processando mensagem: {e}")

    async def handle_connect(self, client_id):
        # Envia CONNACK
        connack = bytes([0x20, 0x02, 0x00, 0x00])
        writer = self.clients[client_id]['writer']
        writer.write(connack)
        await writer.drain()
        print(f"Cliente {client_id} conectado com sucesso")

    async def handle_subscribe(self, client_id, data):
        # Extrai tópico (implementação simplificada)
        try:
            # Pula cabeçalho MQTT para extrair tópico
            payload_start = 4
            topic_len = struct.unpack('>H', data[payload_start:payload_start+2])[0]
            topic = data[payload_start+2:payload_start+2+topic_len].decode('utf-8')
            
            if client_id not in self.subscriptions:
                self.subscriptions[client_id] = []
            
            if topic not in self.subscriptions[client_id]:
                self.subscriptions[client_id].append(topic)
            
            print(f"Cliente {client_id} inscrito no tópico: {topic}")
            
            # Envia SUBACK
            suback = bytes([0x90, 0x03, data[2], data[3], 0x00])
            writer = self.clients[client_id]['writer']
            writer.write(suback)
            await writer.drain()
            
        except Exception as e:
            print(f"Erro no subscribe: {e}")

    async def handle_publish(self, client_id, data):
        try:
            # Extrai tópico e payload
            payload_start = 2
            topic_len = struct.unpack('>H', data[payload_start:payload_start+2])[0]
            topic = data[payload_start+2:payload_start+2+topic_len].decode('utf-8')
            
            message_start = payload_start + 2 + topic_len
            payload = data[message_start:].decode('utf-8')
            
            print(f"Recebido: Tópico={topic}, Payload={payload}")
            
            # Redistribui para assinantes
            await self.distribute_message(topic, payload, client_id)
            
        except Exception as e:
            print(f"Erro no publish: {e}")

    async def distribute_message(self, topic, payload, sender_id):
        for client_id, subscriptions in self.subscriptions.items():
            if client_id == sender_id:
                continue
                
            # Verifica se o cliente está inscrito no tópico (suporte a wildcards básico)
            for sub_topic in subscriptions:
                if self.topic_matches(topic, sub_topic):
                    await self.send_message_to_client(client_id, topic, payload)
                    break

    def topic_matches(self, topic, subscription):
        # Suporte básico a wildcards
        if subscription.endswith('#'):
            return topic.startswith(subscription[:-1])
        return topic == subscription

    async def send_message_to_client(self, client_id, topic, payload):
        try:
            if client_id not in self.clients:
                return
                
            writer = self.clients[client_id]['writer']
            
            # Constrói mensagem PUBLISH
            topic_bytes = topic.encode('utf-8')
            payload_bytes = payload.encode('utf-8')
            
            remaining_length = 2 + len(topic_bytes) + len(payload_bytes)
            
            # Cabeçalho MQTT PUBLISH
            message = bytearray([0x30, remaining_length])
            message.extend(struct.pack('>H', len(topic_bytes)))
            message.extend(topic_bytes)
            message.extend(payload_bytes)
            
            writer.write(message)
            await writer.drain()
            
        except Exception as e:
            print(f"Erro enviando mensagem para {client_id}: {e}")

    async def disconnect_client(self, client_id):
        if client_id in self.clients:
            writer = self.clients[client_id]['writer']
            writer.close()
            await writer.wait_closed()
            del self.clients[client_id]
            
        if client_id in self.subscriptions:
            del self.subscriptions[client_id]
            
        print(f"Cliente desconectado: {client_id}")

async def main():
    broker = SimpleBroker()
    server = await asyncio.start_server(
        broker.handle_connection, 
        'localhost', 
        1883
    )
    print("Broker MQTT customizado rodando em localhost:1883")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())