# 🛠️ Manual de Configuración de Entorno AWS para Despliegue en Kubernetes

Este manual describe paso a paso cómo preparar una cuenta de AWS desde cero, configurar el acceso programático, y crear una base de datos PostgreSQL (RDS) para desplegar una aplicación Django en Kubernetes usando GitHub Actions.

---

## ✅ Paso 1: Crear cuenta de AWS

1. Ir a [https://aws.amazon.com](https://aws.amazon.com)
2. Haz clic en **Crear una cuenta gratuita**
3. Completa:
   - Información personal
   - Tarjeta de crédito
   - Verificación por teléfono
   - Plan: **Básico gratuito**

---

## ✅ Paso 2: Crear usuario IAM y configurar AWS CLI

### 🔹 Crear usuario IAM

1. Inicia sesión como root
2. Ve a **IAM → Usuarios → Agregar usuario**
3. Nombre del usuario: `github-deploy-user`
4. Tipo de acceso: solo seleccionar acceso a consola por ahora si no ves opción programática
5. Finaliza la creación del usuario

### 🔹 Asignar acceso programático manualmente

1. Ve a **IAM > Usuarios**
2. Haz clic sobre el nombre del usuario
3. Ve a la pestaña **Security Credentials**
4. En la sección **Access Keys**, haz clic en **Create access key**
5. Selecciona **Command Line Interface (CLI)** como caso de uso
6. Guarda el `Access key ID` y el `Secret access key` (se muestra una sola vez)

### 🔹 Adjuntar políticas necesarias

1. Desde la vista del usuario IAM, haz clic en **Add permissions**
2. Elige **Attach policies directly**
3. Agrega las siguientes políticas:

   - `AmazonEKSClusterPolicy`
   - `AmazonEKSWorkerNodePolicy`
   - `AmazonEC2FullAccess`
   - `AmazonEC2ContainerRegistryFullAccess` ✅ (este es el nombre correcto de ECR)
   - `IAMFullAccess`
   - `AmazonRDSFullAccess` (opcional)

---

### 🔹 Configurar AWS CLI localmente

Instala AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

Ejecuta:

```bash
aws configure
```

Rellenar con:

```
AWS Access Key ID: <clave>
AWS Secret Access Key: <secreto>
Region: us-east-1
Output: json
```

---

## ✅ Paso 3: Crear base de datos RDS PostgreSQL (desde consola)

1. Ir a **RDS → Bases de datos → Crear base de datos**
2. Configurar:
   - Motor: PostgreSQL
   - Propósito: Desarrollo / Prueba gratuita
   - Nombre: `mydb`
   - Usuario: `postgres`
   - Contraseña: segura
3. Instancia:
   - Tipo: `db.t3.micro` ✅ (incluido en Free Tier)
4. Almacenamiento:
   - 20 GB (predeterminado)
   - Escalado automático: opcional
5. Conectividad:
   - VPC: predeterminada
   - Subred: predeterminada
   - ✅ Acceso público: **Sí**
   - Grupo de seguridad:
     - Puerto: 5432
     - Origen: `0.0.0.0/0` (solo para pruebas; restringir más adelante)

6. Crear y esperar la instancia (~10 min)

---

## 🔜 Próximos pasos

Una vez configurado lo anterior:

- [ ] Crear repositorio ECR (CLI)
- [ ] Crear cluster EKS (CLI)
- [ ] Configurar kubeconfig
- [ ] Crear manifiestos Kubernetes
- [ ] Automatizar despliegue con GitHub Actions

---
