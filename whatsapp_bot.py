import requests
import os
from flask import Flask, request

app = Flask(__name__)

ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "EAAWmcbtkxJcBPgQKAXvrJ3kpKBdie0pW8ff0IRUg6ueXxgtZA6L5zegs3wgXoJm6KX1t24BKueFMDqecjINkSG5xTJ1Q4sQqyFwrsXYX7ZClw9LDi5hFAC0ZAZCfjEpGdEPY422W4jOZBXIJ67rKZBMEwMVQhjkKEwR7Ut7pkKvCOTXYE9ZBCZAulMzhTUXb7yPs5P3bmi3QCKxjN1ZAjkJOZBn58TdrBaPrZAZBZCPDnl7xmFZA6NWrFyh7GyPSO0jaYZD")
PHONE_NUMBER_ID = os.getenv("META_PHONE_NUMBER_ID", "862425433611454")
VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "romoseguros123")

print(f"[v0] Configuración cargada:")
print(f"[v0] - PHONE_NUMBER_ID: {PHONE_NUMBER_ID[:10]}..." if len(PHONE_NUMBER_ID) > 10 else f"[v0] - PHONE_NUMBER_ID: {PHONE_NUMBER_ID}")
print(f"[v0] - ACCESS_TOKEN configurado: {'Sí' if ACCESS_TOKEN != 'EAAWmcbtkxJcBPgQKAXvrJ3kpKBdie0pW8ff0IRUg6ueXxgtZA6L5zegs3wgXoJm6KX1t24BKueFMDqecjINkSG5xTJ1Q4sQqyFwrsXYX7ZClw9LDi5hFAC0ZAZCfjEpGdEPY422W4jOZBXIJ67rKZBMEwMVQhjkKEwR7Ut7pkKvCOTXYE9ZBCZAulMzhTUXb7yPs5P3bmi3QCKxjN1ZAjkJOZBn58TdrBaPrZAZBZCPDnl7xmFZA6NWrFyh7GyPSO0jaYZD' else 'NO - FALTA CONFIGURAR'}")
print(f"[v0] - VERIFY_TOKEN: {VERIFY_TOKEN}")

def enviar_mensaje(numero, texto):
    """Envía un mensaje de WhatsApp a través de la API de Meta"""
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": texto}
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"[v0] Mensaje enviado exitosamente a {numero}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[v0] Error al enviar mensaje: {e}")
        if hasattr(e.response, 'text'):
            print(f"[v0] Respuesta del servidor: {e.response.text}")
        return None

@app.route("/", methods=["GET"])
def home():
    """Ruta principal para verificar que el servidor está funcionando"""
    return {
        "status": "online",
        "service": "WhatsApp Chatbot - Romo Seguros",
        "version": "1.0",
        "webhook_url": "/webhook",
        "verify_token_configured": VERIFY_TOKEN != "romoseguros123"
    }, 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        print("[v0] ===== VERIFICACIÓN DE WEBHOOK =====")
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        print(f"[v0] Mode recibido: {mode}")
        print(f"[v0] Token recibido: {token}")
        print(f"[v0] Token esperado: {VERIFY_TOKEN}")
        print(f"[v0] Challenge: {challenge}")
        
        if not mode or not token or not challenge:
            print("[v0] ❌ Faltan parámetros en la solicitud de verificación")
            return "Faltan parámetros", 400
        
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("[v0] ✅ Webhook verificado exitosamente")
            return challenge, 200
        else:
            print(f"[v0] ❌ Token de verificación inválido o modo incorrecto")
            print(f"[v0] ❌ Comparación: '{token}' == '{VERIFY_TOKEN}' = {token == VERIFY_TOKEN}")
            return "Token inválido", 403

    if request.method == "POST":
        print("[v0] ===== MENSAJE RECIBIDO =====")
        datos = request.get_json()
        print(f"[v0] Datos completos recibidos: {datos}")
        
        try:
            # Verificar estructura de datos
            if not datos:
                print("[v0] ❌ No se recibieron datos")
                return "ok", 200
            
            entry = datos.get("entry", [])
            print(f"[v0] Entries encontrados: {len(entry)}")
            if not entry:
                print("[v0] ⚠️ No hay entries en los datos")
                return "ok", 200
                
            changes = entry[0].get("changes", [])
            print(f"[v0] Changes encontrados: {len(changes)}")
            if not changes:
                print("[v0] ⚠️ No hay changes en los datos")
                return "ok", 200
                
            value = changes[0].get("value", {})
            print(f"[v0] Value: {value}")
            
            # Verificar si hay mensajes
            messages = value.get("messages", [])
            print(f"[v0] Mensajes encontrados: {len(messages)}")
            
            if not messages:
                print("[v0] ⚠️ No hay mensajes en los datos - podría ser una notificación de estado")
                # Verificar si es una notificación de estado
                statuses = value.get("statuses", [])
                if statuses:
                    print(f"[v0] Es una notificación de estado: {statuses}")
                return "ok", 200
            
            # Extraer información del mensaje
            mensaje = messages[0]
            numero = mensaje.get("from")
            mensaje_id = mensaje.get("id")
            tipo_mensaje = mensaje.get("type")
            
            print(f"[v0] 📱 Número: {numero}")
            print(f"[v0] 🆔 ID del mensaje: {mensaje_id}")
            print(f"[v0] 📝 Tipo de mensaje: {tipo_mensaje}")
            
            # Solo procesar mensajes de texto
            if tipo_mensaje != "text":
                print(f"[v0] ⚠️ Tipo de mensaje no soportado: {tipo_mensaje}")
                enviar_mensaje(numero, "Lo siento, solo puedo procesar mensajes de texto. Escribe *menu* para ver las opciones.")
                return "ok", 200
            
            texto_obj = mensaje.get("text", {})
            texto = texto_obj.get("body", "").strip().lower()
            
            print(f"[v0] 💬 Texto recibido: '{texto}'")
            print(f"[v0] 🔄 Procesando respuesta...")

            respuesta_enviada = False
            
            if texto in ["hola", "menu", "inicio", "hi", "hello"]:
                print("[v0] ✅ Detectado saludo - enviando menú principal")
                resultado = enviar_mensaje(numero, 
                    "👋 ¡Hola! Soy tu asistente SophIA de Romo Seguros.\n\n"
                    "Elige una opción:\n"
                    "1️⃣ Cotizar seguro\n"
                    "2️⃣ Renovar póliza\n"
                    "3️⃣ Reportar siniestro\n"
                    "4️⃣ Hablar con un asesor\n\n"
                    "Escribe el número de la opción que deseas.")
                respuesta_enviada = resultado is not None
            
            elif texto == "1":
                print("[v0] ✅ Opción 1 - Cotizar seguro")
                resultado = enviar_mensaje(numero, 
                    "🚗 ¿Qué tipo de seguro deseas cotizar?\n\n"
                    "1️⃣ Auto\n"
                    "2️⃣ Vida\n"
                    "3️⃣ Gastos médicos\n"
                    "4️⃣ Hogar\n\n"
                    "Escribe el número de tu elección.")
                respuesta_enviada = resultado is not None
            
            elif texto == "2":
                print("[v0] ✅ Opción 2 - Renovar póliza")
                resultado = enviar_mensaje(numero, 
                    "🔁 Para renovar tu póliza, necesito:\n\n"
                    "📝 Nombre completo\n"
                    "🔢 Número de póliza\n\n"
                    "Por favor, envíamelos en ese orden.")
                respuesta_enviada = resultado is not None
            
            elif texto == "3":
                print("[v0] ✅ Opción 3 - Reportar siniestro")
                resultado = enviar_mensaje(numero, 
                    "⚠️ Lamentamos mucho el siniestro.\n\n"
                    "Para ayudarte mejor, cuéntame:\n"
                    "• ¿Qué ocurrió?\n"
                    "• ¿Cuándo sucedió?\n"
                    "• ¿Hay personas lesionadas?\n\n"
                    "Un asesor se pondrá en contacto contigo de inmediato.")
                respuesta_enviada = resultado is not None
            
            elif texto == "4":
                print("[v0] ✅ Opción 4 - Hablar con asesor")
                resultado = enviar_mensaje(numero, 
                    "📞 Perfecto, un asesor de Romo Seguros se pondrá en contacto contigo en breve.\n\n"
                    "Horario de atención:\n"
                    "Lunes a Viernes: 9:00 AM - 6:00 PM\n"
                    "Sábados: 9:00 AM - 2:00 PM")
                respuesta_enviada = resultado is not None
            
            else:
                print(f"[v0] ⚠️ Mensaje no reconocido: '{texto}'")
                resultado = enviar_mensaje(numero, 
                    "🤔 No entendí tu mensaje.\n\n"
                    "Escribe *menu* para ver las opciones disponibles.")
                respuesta_enviada = resultado is not None
            
            if respuesta_enviada:
                print("[v0] ✅ Respuesta enviada exitosamente")
            else:
                print("[v0] ❌ Error al enviar respuesta")
        
        except Exception as e:
            print(f"[v0] ❌ Error procesando mensaje: {e}")
            import traceback
            print(f"[v0] Traceback completo:")
            print(traceback.format_exc())
        
        return "ok", 200

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint para Render"""
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    print(f"[v0] ===================================")
    print(f"[v0] Iniciando servidor en puerto {port}")
    print(f"[v0] ===================================")
    app.run(host="0.0.0.0", port=port, debug=False)
