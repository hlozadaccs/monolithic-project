#!/bin/sh

set -e  # Finaliza si algún comando falla

echo "🔄 Esperando a que PostgreSQL esté disponible en $POSTGRES_HOST:$POSTGRES_PORT..."

# Espera hasta que el puerto de Postgres esté disponible
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.5
done

echo "✅ PostgreSQL está listo."

# Ejecutar migraciones
echo "📦 Ejecutando migraciones..."
python manage.py migrate --noinput

# Colectar archivos estáticos (opcional, para prod)
echo "🧹 Colectando archivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar la aplicación con gunicorn
echo "🚀 Iniciando aplicación..."
exec gunicorn core.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 120
