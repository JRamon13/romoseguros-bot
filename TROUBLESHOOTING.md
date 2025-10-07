# Solución de Problemas - Webhook de WhatsApp

## Error: "No se pudo validar la URL de devolución de llamada"

### Paso 1: Verificar que la App está Corriendo en Render

1. Ve a tu dashboard de Render: https://dashboard.render.com
2. Busca tu servicio "romoseguros-bot"
3. Verifica que el estado sea **"Live"** (verde)
4. Si está en "Building" o "Failed", espera o revisa los logs

### Paso 2: Probar la URL Manualmente

Abre en tu navegador:
\`\`\`
https://romoseguros-bot.onrender.com/
\`\`\`

Deberías ver:
\`\`\`json
{
  "status": "online",
  "service": "WhatsApp Chatbot - Romo Seguros",
  "version": "1.0"
}
\`\`\`

Si ves un error o no carga, tu app no está corriendo correctamente.

### Paso 3: Verificar Variables de Entorno en Render

1. En Render, ve a tu servicio
2. Click en **"Environment"** en el menú lateral
3. Verifica que tengas estas 3 variables:
   \`\`\`
   META_ACCESS_TOKEN=EAABsbCS1iHgBO... (tu token real)
   META_PHONE_NUMBER_ID=862425433611454
   WEBHOOK_VERIFY_TOKEN=romoseguros123
   \`\`\`
4. Si falta alguna, agrégala y haz click en **"Save Changes"**
5. Render reiniciará automáticamente tu app

### Paso 4: Ver los Logs en Render

1. En tu servicio de Render, click en **"Logs"**
2. Deberías ver algo como:
   \`\`\`
   [v0] Configuración cargada:
   [v0] - PHONE_NUMBER_ID: 862425433...
   [v0] - ACCESS_TOKEN configurado: Sí
   [v0] - VERIFY_TOKEN: romoseguros123
   [v0] Iniciando servidor en puerto 10000
   \`\`\`

### Paso 5: Configurar el Webhook en Meta (Orden Correcto)

1. **Primero**: Asegúrate de que tu app en Render esté corriendo (pasos anteriores)

2. **Luego**: Ve a Meta for Developers
   - Tu aplicación > WhatsApp > Configuración > Webhook
   - Click en **"Editar"**

3. **Ingresa**:
   - **URL de devolución de llamada**: `https://romoseguros-bot.onrender.com/webhook`
   - **Token de verificación**: `romoseguros123` (exactamente igual que en tu código)

4. **Click en "Verificar y guardar"**

5. **Observa los logs en Render** en tiempo real:
   - Deberías ver:
   \`\`\`
   [v0] ===== VERIFICACIÓN DE WEBHOOK =====
   [v0] Mode recibido: subscribe
   [v0] Token recibido: romoseguros123
   [v0] Token esperado: romoseguros123
   [v0] ✅ Webhook verificado exitosamente
   \`\`\`

### Paso 6: Suscribirse a Eventos

Después de verificar exitosamente:

1. En la misma página de Webhook, click en **"Administrar"**
2. Suscríbete a:
   - ✅ **messages**
   - ✅ **message_status** (opcional)
3. Click en **"Guardar"**

## Problemas Comunes

### ❌ "Token inválido"
- **Causa**: El VERIFY_TOKEN en Render no coincide con el de Meta
- **Solución**: Verifica que sea exactamente `romoseguros123` en ambos lados

### ❌ "Connection timeout"
- **Causa**: Tu app en Render no está corriendo o está en modo "sleep"
- **Solución**: 
  - Abre `https://romoseguros-bot.onrender.com/` para despertarla
  - Espera 30 segundos y vuelve a intentar en Meta

### ❌ "SSL certificate error"
- **Causa**: Render aún no ha generado el certificado HTTPS
- **Solución**: Espera 5-10 minutos después de crear el servicio

### ❌ La app se duerme (plan gratuito de Render)
- **Causa**: Render duerme apps gratuitas después de 15 minutos de inactividad
- **Solución**: 
  - Usa un servicio de "ping" como UptimeRobot para mantenerla despierta
  - O actualiza a un plan de pago de Render

## Comandos Útiles para Debugging

### Probar el endpoint de verificación manualmente:
\`\`\`bash
curl "https://romoseguros-bot.onrender.com/webhook?hub.mode=subscribe&hub.verify_token=romoseguros123&hub.challenge=TEST123"
\`\`\`

Debería devolver: `TEST123`

### Probar el health check:
\`\`\`bash
curl https://romoseguros-bot.onrender.com/health
\`\`\`

Debería devolver: `{"status":"healthy"}`

## Contacto

Si después de seguir todos estos pasos aún tienes problemas, revisa:
1. Los logs completos en Render
2. Que tu cuenta de Meta esté verificada
3. Que no haya restricciones de firewall o región
