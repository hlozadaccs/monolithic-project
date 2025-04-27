# 🌍 Despliegue de proyecto Monolítico en Minikube

Este proyecto permite desplegar una aplicación Django en Minikube usando Gunicorn, PostgreSQL externo y Nginx Ingress.

## 🔧 Requisitos previos

- Docker instalado
- Minikube instalado y en ejecución
- kubectl configurado para Minikube


## ✅ Preparación del entorno

### 1. Iniciar Minikube
```bash
minikube start
eval $(minikube docker-env)
```

### 2. Construir la imagen Docker
```bash
docker build -f Dockerfile.prod -t django-app:prod .
```

## ✨ Configuración de Kubernetes

### 3. Crear el Secret para variables de entorno

Antes de crear el secret, asegúrate que `.env.prod` esté correctamente configurado.

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
kubectl apply -f django-secret.yaml
kubectl get secrets
kubectl describe secret django-secret
kubectl delete secret django-secret  # Opcional
```

### 4. Desplegar los manifiestos Kubernetes

Aplicar los archivos de despliegue y servicio:

```bash
kubectl apply -f django-deployment.yaml
kubectl apply -f django-service.yaml
```


### 5. (Opcional) Habilitar y configurar Ingress

Habilitar el addon Ingress en Minikube:

```bash
minikube addons enable ingress
```

Aplicar el manifiesto de Ingress:

```bash
kubectl apply -f django-ingress.yaml
```

Editar el archivo `/etc/hosts` agregando la IP de Minikube:

```bash
echo "$(minikube ip) django.local" | sudo tee -a /etc/hosts
```


## 📅 Reinicio del deployment

Cada vez que modifiques `Dockerfile.prod`, `entrypoint.sh`, o `requirements.txt`, reconstruye la imagen y reinicia el deployment:

```bash
eval $(minikube docker-env)
docker build -f Dockerfile.prod -t django-app:prod .
kubectl rollout restart deployment django-app
```


## 🌍 Acceso a la aplicación

- **Sin Ingress:**

Accede directamente usando el puerto del NodePort:

```bash
http://$(minikube ip):30080
```

- **Con Ingress:**

Accede usando la URL amigable:

```bash
http://django.local
```


## 📚 Archivos relevantes

- `Dockerfile.prod`
- `docker-compose.prod.yml`
- `entrypoint.sh`
- `django-deployment.yaml`
- `django-service.yaml`
- `django-ingress.yaml`
- `secret.yaml`


## 💚 Notas adicionales

- Los archivos estáticos (`static/`) deben ser recopilados mediante `collectstatic` y están expuestos por Django temporalmente en desarrollo.
- La conexión a PostgreSQL usa `host.minikube.internal` para apuntar al contenedor externo.


---

🚀 Proyecto listo para evolucionar a entornos de nube como AWS EKS o GCP GKE.

# 🔧 Limpieza Completa de Minikube

Este procedimiento elimina todos los recursos desplegados en Minikube, incluyendo deployments, services, ingress, secrets y datos persistentes.

---

## ❌ Detener y eliminar el cluster actual

```bash
minikube stop
minikube delete --all
```

Esto detiene Minikube y elimina todas las configuraciones del cluster.

---

## 📂 Eliminar configuraciones locales

Borrar configuraciones y cachés relacionados en tu equipo:

```bash
rm -rf ~/.minikube
rm -rf ~/.kube
```

> **Nota:** Si usas otros clusters (por ejemplo, en la nube), elimina con cuidado solo el contexto de Minikube.

---

## 🌐 Limpieza opcional de Docker

Si quieres limpiar las imágenes que construiste dentro del entorno de Docker:

1. Conectar al demonio de Docker de Minikube:

```bash
eval $(minikube docker-env)
```

2. Ver las imágenes:

```bash
docker images
```

3. Eliminar imágenes específicas (opcional):

```bash
docker rmi <nombre_imagen>
```

---

## 🌍 Restablecer el /etc/hosts

Si agregaste entradas en `/etc/hosts` como `django.local`, recuerda eliminarlas manualmente si ya no son necesarias:

```bash
sudo nano /etc/hosts
```

Buscar y eliminar líneas como:

```
192.168.49.2 django.local
```

---

# 🔄 Minikube completamente limpio y listo para reiniciar desde cero.

🚀 Ahora puedes ejecutar `minikube start` para comenzar un nuevo ambiente limpio.

