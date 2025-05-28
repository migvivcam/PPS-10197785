# README.md - Actividad 5.1: Instalación y despliegue en K3s (Single-Node) con K9s

## Objetivo
Instalar, configurar y validar un clúster **K3s** en modo *single-node*, desplegar un servicio **nginx** con 2 réplicas, y utilizar **K9s** para la monitorización del clúster.

---

## Requisitos previos
- Sistema operativo Linux (Ubuntu, Debian, CentOS, etc.)
- Usuario con privilegios sudo
- Conexión a internet

---

## Esquema de pasos

### 1. Instalación de K3s (Single-Node)
```bash
curl -sfL https://get.k3s.io | sh -
```

Verificar el estado del servicio:
```bash
sudo systemctl status k3s
```

Comprobar los nodos del clúster:
```bash
sudo k3s kubectl get nodes
```

### 2. Crear alias para `kubectl`
```bash
alias kubectl='k3s kubectl'
```
> Añadir a `~/.bashrc` o `~/.zshrc` para mantenerlo permanente.

### 3. Desplegar nginx con 2 réplicas

Crear el archivo `nginx-deployment.yaml` con el siguiente contenido:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
```

Aplicar el despliegue:
```bash
kubectl apply -f nginx-deployment.yaml
```

Verificar que los pods estén corriendo:
```bash
kubectl get pods
```

### 4. Instalación de K9s

Descargar y extraer:
```bash
curl -sSLo k9s.tar.gz https://github.com/derailed/k9s/releases/latest/download/k9s_Linux_amd64.tar.gz
tar -xvzf k9s.tar.gz
sudo mv k9s /usr/local/bin/
```

Ejecutar:
```bash
k9s
```