# 🚀 Despliegue de Django en Minikube con Kubernetes

Este manual describe cómo desplegar una aplicación Django en Minikube usando manifiestos de Kubernetes y recursos como Deployment, Service, Ingress, Secret y ConfigMap.

---

## 📦 Pre-requisitos

- Docker
- Minikube
- kubectl
- Proyecto Django con Dockerfile.prod

---

## 🧰 Pasos para el despliegue local

### 1. Iniciar Minikube

```bash
minikube start --driver=docker
minikube addons enable ingress
```

### 2. Usar el entorno Docker de Minikube

```bash
eval $(minikube docker-env)
```

### 3. Construir la imagen Docker

```bash
docker build -t my-app:latest .
```

### 4. Aplicar los manifiestos de Kubernetes

```bash
kubectl apply -f secret.yaml
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

### 5. Verificar que el pod esté corriendo

```bash
kubectl get pods
```

### 6. Exponer el Ingress localmente

```bash
minikube tunnel
kubectl get ingress
```

Accede en el navegador a la IP listada o a `http://localhost` si configuraste hosts.

---

## 📄 Archivos incluidos

- `deployment.yaml` – Define el despliegue de la app
- `service.yaml` – Expone el pod dentro del clúster
- `ingress.yaml` – Expone la app externamente vía HTTP
- `secret.yaml` – Variables sensibles (como claves o contraseñas)
- `configmap.yaml` – Configuración no sensible como entorno o flags
- `deploy_minikube.sh` – Script para automatizar todo el flujo

---

## ✅ Recomendaciones

- Usa `kubectl describe pod <nombre>` si algo falla
- Usa `kubectl logs <nombre>` para ver los logs
- Asegúrate de que Minikube tenga recursos suficientes (`minikube config set memory 4096`)

---

