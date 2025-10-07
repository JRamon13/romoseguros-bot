# Guía de Despliegue en Render

## Pasos para desplegar tu chatbot de WhatsApp en Render

### 1. Preparar tu cuenta de Meta (WhatsApp Business API)

1. Ve a [Meta for Developers](https://developers.facebook.com/)
2. Crea una aplicación de WhatsApp Business
3. Obtén tu **Access Token** y **Phone Number ID**
4. Configura el webhook (lo harás después de desplegar en Render)

### 2. Desplegar en Render

1. Ve a [Render.com](https://render.com/) y crea una cuenta
2. Haz clic en "New +" y selecciona "Web Service"
3. Conecta tu repositorio de GitHub (o sube el código)
4. Render detectará automáticamente que es una aplicación Python
5. Configura las siguientes variables de entorno:
   - `META_ACCESS_TOKEN`: Tu token de acceso de Meta
   - `META_PHONE_NUMBER_ID`: Tu ID de número de teléfono
   - `WEBHOOK_VERIFY_TOKEN`: romoseguros123 (o cámbialo)
   - `PORT`: 10000

### 3. Configurar el Webhook en Meta

1. Una vez desplegado, copia la URL de tu servicio en Render
2. Ve a tu aplicación en Meta for Developers
3. En la sección de WhatsApp > Configuración
4. Agrega la URL del webhook: `https://tu-app.onrender.com/webhook`
5. Token de verificación: `romoseguros123` (el mismo que configuraste)
6. Suscríbete a los eventos: `messages`

### 4. Probar el Chatbot

1. Envía un mensaje de WhatsApp al número configurado
2. El bot debería responder automáticamente
3. Prueba las diferentes opciones del menú

## Comandos útiles

### Ejecutar localmente
\`\`\`bash
python scripts/whatsapp_bot.py
\`\`\`

### Instalar dependencias
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Ejecutar con Gunicorn (producción)
\`\`\`bash
gunicorn scripts.whatsapp_bot:app
\`\`\`

## Solución de problemas

- **El webhook no se verifica**: Asegúrate de que el `WEBHOOK_VERIFY_TOKEN` coincida
- **No se envían mensajes**: Verifica tu `META_ACCESS_TOKEN` y `META_PHONE_NUMBER_ID`
- **Error 500**: Revisa los logs en Render para ver el error específico

## Mejoras futuras

- Agregar base de datos para guardar conversaciones
- Implementar IA para respuestas más inteligentes
- Agregar más opciones al menú
- Integrar con CRM de Romo Seguros
