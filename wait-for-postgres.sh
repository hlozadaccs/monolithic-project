#!/bin/sh

set -e  # Salir si hay error

echo "🔄 Esperando a que PostgreSQL esté disponible en $POSTGRES_HOST:$POSTGRES_PORT..."

# Espera hasta que PostgreSQL esté listo
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.5
done

echo "✅ PostgreSQL está listo. Iniciando aplicación..."

# Ejecuta el comando pasado como argumento
exec "$@"
