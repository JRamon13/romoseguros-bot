import requests
import os
from flask import Flask, request

app = Flask(__name__)

ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "EAAWmcbtkxJcBPgQKAXvrJ3kpKBdie0pW8ff0IRUg6ueXxgtZA6L5zegs3wgXoJm6KX1t24BKueFMDqecjINkSG5xTJ1Q4sQqyFwrsXYX7ZClw9LDi5hFAC0ZAZCfjEpGdEPY422W4jOZBXIJ67rKZBMEwMVQhjkKEwR7Ut7pkKvCOTXYE9ZBCZAulMzhTUXb7yPs5P3bmi3QCKxjN1ZAjkJOZBn58TdrBaPrZAZBZCPDnl7xmFZA6NWrFyh7GyPSO0jaYZDTA")
PHONE_NUMBER_ID = os.getenv("META_PHONE_NUMBER_ID", "862425433611454")
VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "romoseguros123")

def enviar_mensaje(numero, texto):
    """Envía un mensaje de WhatsApp a través de la API de Meta"""
    url = f"https://graph.facebook.com/v20.0/{862425433611454}/messages"
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
        return None

@app.route("/", methods=["GET"])
def home():
    """Ruta principal para verificar que el servidor está funcionando"""
    return {
        "status": "online",
        "service": "WhatsApp Chatbot - Romo Seguros",
        "version": "1.0"
    }, 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # ✅ Verificación inicial de Meta
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            print("[v0] Webhook verificado exitosamente")
            return challenge
        print("[v0] Token de verificación inválido")
        return "Token inválido", 403

    # ✅ Procesamiento de mensajes
    datos = request.get_json()
    try:
        entry = datos.get("entry", [])
        if not entry:
            return "ok", 200
            
        changes = entry[0].get("changes", [])
        if not changes:
            return "ok", 200
            
        value = changes[0].get("value", {})
        messages = value.get("messages", [])
        
        if not messages:
            return "ok", 200
        
        numero = messages[0].get("from")
        texto_obj = messages[0].get("text", {})
        texto = texto_obj.get("body", "").strip().lower()
        
        print(f"[v0] Mensaje recibido de {numero}: {texto}")

        if texto in ["hola", "menu", "inicio", "hi", "hello"]:
            enviar_mensaje(numero, 
                "👋 ¡Hola! Soy tu asistente SophIA de Romo Seguros.\n\n"
                "Elige una opción:\n"
                "1️⃣ Cotizar seguro\n"
                "2️⃣ Renovar póliza\n"
                "3️⃣ Reportar siniestro\n"
                "4️⃣ Hablar con un asesor\n\n"
                "Escribe el número de la opción que deseas.")
        
        elif texto == "1":
            enviar_mensaje(numero, 
                "🚗 ¿Qué tipo de seguro deseas cotizar?\n\n"
                "1️⃣ Auto\n"
                "2️⃣ Vida\n"
                "3️⃣ Gastos médicos\n"
                "4️⃣ Hogar\n\n"
                "Escribe el número de tu elección.")
        
        elif texto == "2":
            enviar_mensaje(numero, 
                "🔁 Para renovar tu póliza, necesito:\n\n"
                "📝 Nombre completo\n"
                "🔢 Número de póliza\n\n"
                "Por favor, envíamelos en ese orden.")
        
        elif texto == "3":
            enviar_mensaje(numero, 
                "⚠️ Lamentamos mucho el siniestro.\n\n"
                "Para ayudarte mejor, cuéntame:\n"
                "• ¿Qué ocurrió?\n"
                "• ¿Cuándo sucedió?\n"
                "• ¿Hay personas lesionadas?\n\n"
                "Un asesor se pondrá en contacto contigo de inmediato.")
        
        elif texto == "4":
            enviar_mensaje(numero, 
                "📞 Perfecto, un asesor de Romo Seguros se pondrá en contacto contigo en breve.\n\n"
                "Horario de atención:\n"
                "Lunes a Viernes: 9:00 AM - 6:00 PM\n"
                "Sábados: 9:00 AM - 2:00 PM")
        
        else:
            enviar_mensaje(numero, 
                "🤔 No entendí tu mensaje.\n\n"
                "Escribe *menu* para ver las opciones disponibles.")
    
    except Exception as e:
        print(f"[v0] Error procesando mensaje: {e}")
    
    return "ok", 200

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint para Render"""
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    print(f"[v0] Iniciando servidor en puerto {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
