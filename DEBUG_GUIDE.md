# Guía de Depuración - WhatsApp Chatbot

## Problema: El bot no responde a los mensajes

### Paso 1: Verificar que el webhook esté recibiendo mensajes

1. Ve a tu servicio en Render: https://dashboard.render.com
2. Selecciona tu servicio "romoseguros-bot"
3. Click en la pestaña **"Logs"**
4. Envía "Hola" desde WhatsApp
5. Busca en los logs:

**Si ves esto, el webhook está funcionando:**
\`\`\`
[v0] ===== MENSAJE RECIBIDO =====
[v0] Datos completos recibidos: {...}
[v0] 📱 Número: 521234567890
[v0] 💬 Texto recibido: 'hola'
\`\`\`

**Si NO ves nada, el problema es la configuración en Meta.**

### Paso 2: Verificar suscripción a eventos en Meta

1. Ve a [developers.facebook.com](https://developers.facebook.com)
2. Selecciona tu aplicación
3. Ve a **WhatsApp** > **Configuración** > **Webhook**
4. Click en **"Administrar"** (junto a los campos de webhook)
5. Verifica que estés suscrito a:
   - ✅ **messages** (OBLIGATORIO)
   - ✅ **message_status** (opcional)

**Si no está marcado "messages", márcalo y guarda.**

### Paso 3: Verificar que tu número esté agregado

1. En Meta for Developers
2. Ve a **WhatsApp** > **Introducción**
3. En **"Paso 2: Enviar mensajes con la API"**
4. Verifica que tu número esté en la lista de "Números de teléfono"
5. Si no está, agrégalo:
   - Click en **"Agregar número de teléfono"**
   - Ingresa tu número con código de país (ej: +52 1234567890)
   - Recibirás un código de verificación por WhatsApp
   - Ingresa el código

### Paso 4: Verificar variables de entorno en Render

1. En Render, ve a tu servicio
2. Click en **"Environment"** en el menú lateral
3. Verifica que tengas estas variables:

\`\`\`
META_ACCESS_TOKEN=EAABsbCS1iHgBO... (tu token real)
META_PHONE_NUMBER_ID=862425433611454
WEBHOOK_VERIFY_TOKEN=romoseguros123
\`\`\`

**Si META_ACCESS_TOKEN dice "TU_ACCESS_TOKEN_DE_META", necesitas configurarlo.**

### Paso 5: Verificar que el token no haya expirado

El token temporal de Meta expira en 24 horas.

1. Ve a Meta for Developers
2. **WhatsApp** > **Introducción** > **Paso 3**
3. Copia el nuevo token
4. Actualiza la variable `META_ACCESS_TOKEN` en Render
5. Reinicia el servicio en Render

### Paso 6: Probar manualmente el envío de mensajes

Abre esta URL en tu navegador (reemplaza con tus datos):

\`\`\`
https://graph.facebook.com/v20.0/862425433611454/messages
\`\`\`

Envía un POST con:
\`\`\`json
{
  "messaging_product": "whatsapp",
  "to": "521234567890",
  "type": "text",
  "text": {"body": "Prueba manual"}
}
\`\`\`

Headers:
\`\`\`
Authorization: Bearer TU_ACCESS_TOKEN
Content-Type: application/json
\`\`\`

Si esto funciona, el problema es el webhook. Si no funciona, el problema es la configuración de Meta.

### Errores Comunes

#### Error: "Token inválido"
- El META_ACCESS_TOKEN expiró o es incorrecto
- Genera un nuevo token en Meta

#### Error: "Phone number not found"
- El META_PHONE_NUMBER_ID es incorrecto
- Verifica el ID en Meta > WhatsApp > Introducción

#### Error: "Recipient phone number not valid"
- Tu número no está agregado como número de prueba
- Agrégalo en Meta > WhatsApp > Introducción > Paso 2

#### No aparece nada en los logs
- El webhook no está suscrito a "messages"
- Verifica en Meta > WhatsApp > Configuración > Webhook > Administrar

### Comandos útiles

**Ver logs en tiempo real en Render:**
- Ve a la pestaña "Logs" y deja la página abierta
- Los logs se actualizan automáticamente

**Reiniciar el servicio:**
- En Render, click en "Manual Deploy" > "Deploy latest commit"

### Contacto de soporte

Si después de seguir todos estos pasos el bot sigue sin funcionar:

1. Copia los logs completos de Render
2. Toma capturas de pantalla de:
   - La configuración del webhook en Meta
   - Las variables de entorno en Render
   - Los logs cuando envías un mensaje
3. Abre un ticket de soporte en Meta o Render según corresponda
