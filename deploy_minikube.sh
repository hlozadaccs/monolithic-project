#!/bin/bash

set -e

echo "🔧 Cambiando el entorno Docker para usar el de Minikube..."
eval $(minikube docker-env)

echo "🐳 Construyendo imagen local para my-app:latest..."
docker build -t my-app:latest .

echo "📦 Aplicando manifiestos de Kubernetes..."
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml

echo "⏳ Esperando a que los pods estén listos..."
kubectl wait --for=condition=Ready pod -l app=django-app --timeout=90s

echo "🚪 Abriendo túnel para Ingress (ejecuta en una ventana separada si deseas mantenerlo activo)..."
echo "👉 Ejecuta: minikube tunnel"
echo "👉 Luego accede a: http://localhost o la IP del Ingress"

echo "✅ Despliegue en Minikube completado."
