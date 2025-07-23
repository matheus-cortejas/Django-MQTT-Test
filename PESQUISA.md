# Resumo da Pesquisa: Arquiteturas IoT com Django e MQTT

Este documento resume as principais abordagens para construir uma aplicação IoT utilizando Django e o protocolo MQTT, com base em pesquisas sobre suas características, vantagens e cenários de uso.

## 1. O que é MQTT?

MQTT (Message Queuing Telemetry Transport) é um protocolo de mensagens leve e eficiente, ideal para dispositivos com recursos limitados (IoT). Seu funcionamento se baseia no modelo de **publicação/assinatura (pub/sub)**, onde um servidor central chamado **Broker** gerencia a distribuição de mensagens entre clientes.

*   **Clientes (Publishers/Subscribers)**: Dispositivos que enviam (publicam) ou recebem (assinam) mensagens.
*   **Broker**: Intermediário que recebe mensagens e as encaminha para os assinantes corretos.
*   **Tópicos**: "Canais" hierárquicos (ex: `sensores/sala/temperatura`) que organizam as mensagens.

Suas principais vantagens são o baixo consumo de banda, suporte a redes instáveis e escalabilidade.

## 2. Tipos de Broker: Local vs. Cloud

A escolha do broker MQTT impacta diretamente o controle, custo e escalabilidade do projeto.

| Critério | Broker Local (Ex: Mosquitto) | Broker em Nuvem (Ex: HiveMQ) |
| :--- | :--- | :--- |
| **Controle** | ✅ **Total** sobre dados e infraestrutura. | 🔄 **Menor**, pois é gerenciado por terceiros. |
| **Custo** | ✅ **Baixo** (software livre, custo de hardware). | 💲 **Pago** (baseado em uso/planos). |
| **Manutenção**| ⚠️ **Exige** administração manual. | ✅ **Gerenciado** pelo provedor. |
| **Escalabilidade**| ⚠️ **Limitada** ao hardware local. | 🚀 **Alta** e automática. |
| **Ideal para** | Redes privadas, protótipos, automação residencial. | Projetos escaláveis, aplicações comerciais. |

## 3. Arquiteturas de Comunicação

Existem duas abordagens principais para integrar um dispositivo (como o ESP32) com um backend e frontend.

#### **Abordagem 1: ESP32 direto no Broker MQTT**

O dispositivo publica dados diretamente no broker. O frontend (dashboard) assina o mesmo broker para receber as atualizações em tempo real.

*   **Vantagens**: Baixa latência, arquitetura simples.
*   **Desvantagens**: Menos controle central, a lógica de segurança e processamento fica no dispositivo.
*   **Quando usar**: Projetos simples de monitoramento em tempo real.

#### **Abordagem 2: ESP32 envia para o Django (Intermediário)**

O dispositivo envia dados via **HTTP POST** para uma API Django. O Django, então, processa esses dados (salva no banco, valida) e os publica no broker MQTT.

*   **Vantagens**: **Controle centralizado**, maior segurança (o dispositivo não precisa de credenciais MQTT), flexibilidade para processar e armazenar dados.
*   **Desvantagens**: Maior latência (passo extra), arquitetura mais complexa.
*   **Quando usar**: Aplicações que necessitam de persistência de dados, validação, ou regras de negócio complexas.

## Resumão (Baseado no que entendi do projeto)

> A melhor abordagem considerando nosso projeto dos Controles será:
>
> -   **ESP32** recebe os dados do sensor e envia via HTTP (POST) para a API
> -   A **API do Django** recebe os dados, valida, salva no banco e envia uma confirmação `HTTP` de volta para o ESP32.
> -   A API chama o `mqtt_service`, que publica (envia) a mensagem no **Broker MQTT**.
> -   O **Broker MQTT** recebe a mensagem e repassa a mensagem para todos que "precisam" dela
> -   O **JavaScript** (`<script>`) no dashboard processa os dados para atualização em tempo real.
>
> **Observação sobre o funcionamento atual:**
>
> *   No caso do projeto, o que está processando é uma view que retira os dados do banco e atualiza (não era a intenção primaria, mas funciona ao que parece)
> *   Isso acontece por conta do Broker ser bem simples, com o HiveMQ ou Mosquito daria para entender melhor essa parte do processamento no Front
> *   Pode ser apresentado como uma abordagem possivel, simplesmente salvar no banco os dados e puxar pela view sem passar pelo Broker 🤣🤣🤣

---

## Referências

*   [Pesquisa inicial e base (DeepSeek)](https://chat.deepseek.com/a/chat/s/6ccff112-ea10-47fe-a03a-6f72b1d0c88f)
*   [YouTube: MQTT + Django + ESP32](https://www.youtube.com/watch?v=IQBWMHMTTO8&t=43s)
*   [High-Voltages: MQTT in Python](https://highvoltages.co/iot-internet-of-things/mqtt/mqtt-in-python/)
*   [EMQ: How to Use MQTT in Django](https://www.emqx.com/en/blog/how-to-use-mqtt-in-django)
*   [EMQ: MQTT Guide](https://www.emqx.com/en/mqtt-guide)
*   [Paho-MQTT PyPI](https://pypi.org/project/paho-mqtt/)
*   [Documentação Oficial Paho MQTT](https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html)