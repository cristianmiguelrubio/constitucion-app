# Deploy público — Para que cualquiera pueda usar la app

## Opción 1: Railway (recomendado, gratis)

1. Crea cuenta en https://railway.app (gratis)
2. Instala Railway CLI: `npm install -g @railway/cli`
3. Desde la carpeta del proyecto:

```
railway login
railway init
railway up
```

Railway detecta automáticamente Python + Node y despliega ambos.

## Opción 2: Render (gratis)

### Backend (FastAPI):
1. Ve a https://render.com → New → Web Service
2. Conecta tu repositorio GitHub
3. Configuración:
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (React):
1. New → Static Site
2. Root directory: `frontend`
3. Build command: `npm install && npm run build`
4. Publish directory: `dist`
5. En `vite.config.js` cambia el proxy a la URL del backend de Render

## Opción 3: Solo red local (para probar en móvil ya mismo)

Con el `start.bat` actualizado, la app ya escucha en tu red WiFi.

1. Ejecuta `start.bat`
2. Busca tu IP en la consola (pone "Movil: http://192.168.X.X:5173")
3. Abre esa URL en el móvil (mismo WiFi)
4. En Chrome/Safari: menú → "Añadir a pantalla de inicio"

## Variable de entorno importante para producción

En producción cambia la SECRET_KEY:
```
SECRET_KEY=una-clave-larga-y-aleatoria-aqui
```
