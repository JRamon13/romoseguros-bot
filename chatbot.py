import requests
from flask import Flask, request

app = Flask(__name__)

ACCESS_TOKEN = "TU_ACCESS_TOKEN_DE_META"
PHONE_NUMBER_ID = "TU_PHONE_NUMBER_ID"
VERIFY_TOKEN = "romoseguros123"

def enviar_mensaje(numero, texto):
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
    requests.post(url, headers=headers, json=data)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # ✅ Verificación inicial de Meta
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Token inválido", 403

    # ✅ Procesamiento de mensajes
    datos = request.get_json()
    try:
        numero = datos["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
        texto = datos["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"].strip().lower()

        if texto in ["hola", "menu", "inicio"]:
            enviar_mensaje(numero, "👋 ¡Hola! Soy tu asistente SophIA de Romo Seguros.\nElige una opción:\n1️⃣ Cotizar seguro\n2️⃣ Renovar póliza\n3️⃣ Reportar siniestro\n4️⃣ Hablar con un asesor")
        elif texto == "1":
            enviar_mensaje(numero, "🚗 ¿Qué tipo de seguro deseas cotizar?\n1️⃣ Auto\n2️⃣ Vida\n3️⃣ Gastos médicos\n4️⃣ Hogar")
        elif texto == "2":
            enviar_mensaje(numero, "🔁 Para renovación, por favor indícame tu nombre completo y número de póliza.")
        elif texto == "3":
            enviar_mensaje(numero, "⚠️ Lamentamos el siniestro. Cuéntame brevemente qué ocurrió.")
        elif texto == "4":
            enviar_mensaje(numero, "📞 Un asesor de Romo Seguros se pondrá en contacto contigo en breve.")
        else:
            enviar_mensaje(numero, "No entendí tu mensaje 🤔. Escribe *menu* para ver las opciones.")
    except Exception as e:
        print("Error:", e)
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
