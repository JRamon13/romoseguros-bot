# Chatbot de WhatsApp - Romo Seguros

Bot automatizado para atención al cliente de Romo Seguros a través de WhatsApp Business API.

## Características

- ✅ Respuestas automáticas 24/7
- ✅ Menú interactivo con opciones
- ✅ Cotización de seguros (Auto, Vida, Gastos médicos, Hogar)
- ✅ Renovación de pólizas
- ✅ Reporte de siniestros
- ✅ Conexión con asesores humanos
- ✅ Listo para desplegar en Render

## Estructura del Proyecto

\`\`\`
├── scripts/
│   └── whatsapp_bot.py      # Código principal del bot
├── requirements.txt          # Dependencias de Python
├── render.yaml              # Configuración para Render
├── DEPLOYMENT.md            # Guía de despliegue
└── README.md                # Este archivo
\`\`\`

## Tecnologías

- **Python 3.11+**
- **Flask**: Framework web
- **WhatsApp Business API**: Mensajería
- **Render**: Hosting y despliegue

## Instalación Local

1. Clona el repositorio
2. Instala las dependencias:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`
3. Configura las variables de entorno:
   \`\`\`bash
   export META_ACCESS_TOKEN="tu_token"
   export META_PHONE_NUMBER_ID="tu_phone_id"
   export WEBHOOK_VERIFY_TOKEN="romoseguros123"
   \`\`\`
4. Ejecuta el bot:
   \`\`\`bash
   python scripts/whatsapp_bot.py
   \`\`\`

## Despliegue en Render

Consulta [DEPLOYMENT.md](DEPLOYMENT.md) para instrucciones detalladas.

## Uso

Los clientes pueden interactuar con el bot enviando:

- **"hola"** o **"menu"**: Ver opciones principales
- **"1"**: Cotizar seguro
- **"2"**: Renovar póliza
- **"3"**: Reportar siniestro
- **"4"**: Hablar con un asesor

## Licencia

© 2025 Romo Seguros. Todos los derechos reservados.
