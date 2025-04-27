#!/bin/sh

set -e  # Finaliza si algún comando falla

echo "🔄 Esperando a que PostgreSQL esté disponible en $DATABASE_HOST:$DATABASE_PORT..."

# Espera hasta que el puerto de Postgres esté disponible

until nc -z -v -w30 $DATABASE_HOST $DATABASE_PORT
do
  echo "PostgreSQL no disponible, reintentando en 1 segundo..."
  sleep 1
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
