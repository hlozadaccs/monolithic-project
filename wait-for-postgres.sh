#!/bin/sh

set -e  # Salir si hay error

echo "🔄 Esperando a que PostgreSQL esté disponible en $DATABASE_HOST:$DATABASE_PORT..."

# Espera hasta que PostgreSQL esté listo
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 0.5
done

echo "✅ PostgreSQL está listo. Iniciando aplicación..."

# Ejecuta el comando pasado como argumento
exec "$@"
