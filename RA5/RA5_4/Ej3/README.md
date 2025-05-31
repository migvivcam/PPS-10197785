# Migración de Docker Compose a Kubernetes K3s

## Docker Compose Original
```yaml
services:
    web:
        build: .
        labels:
        - "traefik.enable=true"
        - "traefik.http.routers.web.rule=Host(`localhost`)"
        - "traefik.http.routers.web.entrypoints=web"
        - "traefik.http.services.web.loadbalancer.server.port=80"
    redis:
        image: redis
        volumes:
            - "./data:/data"
        command: redis-server --appendonly yes
        labels:
        - "traefik.enable=false"
    traefik:
        image: traefik:v2.3
        command:
        - "--log.level=DEBUG"
        - "--api.insecure=true"
        - "--providers.docker=true"
        - "--providers.docker.exposedByDefault=false"
        - "--entrypoints.web.address=:4000"
        ports:
        - "4000:4000"
        - "8080:8080"
        volumes:
        - "/var/run/docker.sock:/var/run/docker.sock"
        labels:
        - "traefik.enable=true"
```

## Manifiestos de Kubernetes K3s

### 1. Namespace
```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: myapp
```

### 2. ConfigMap para Traefik
```yaml
# traefik-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: traefik-config
  namespace: myapp
data:
  traefik.yml: |
    log:
      level: DEBUG
    api:
      dashboard: true
      insecure: true
    entryPoints:
      web:
        address: ":4000"
      dashboard:
        address: ":8080"
    providers:
      kubernetesIngress: {}
      kubernetesCRD: {}
```

### 3. PersistentVolume y PersistentVolumeClaim para Redis
```yaml
# redis-storage.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: redis-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /tmp/redis-data
  storageClassName: local-storage
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-pvc
  namespace: myapp
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: local-storage
```

### 4. Redis Deployment y Service
```yaml
# redis.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: myapp
  labels:
    app: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:latest
        command: ["redis-server", "--appendonly", "yes"]
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: redis-data
          mountPath: /data
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
      volumes:
      - name: redis-data
        persistentVolumeClaim:
          claimName: redis-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
  namespace: myapp
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
  type: ClusterIP
```

### 5. Web Application Deployment y Service
```yaml
# web-app.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  namespace: myapp
  labels:
    app: web
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: your-web-app:latest  # Reemplaza con tu imagen construida
        ports:
        - containerPort: 80
        env:
        - name: REDIS_HOST
          value: "redis-service"
        - name: REDIS_PORT
          value: "6379"
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: web-service
  namespace: myapp
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
```

### 6. Traefik RBAC
```yaml
# traefik-rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: traefik
  namespace: myapp
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: traefik
rules:
- apiGroups: [""]
  resources: ["services", "endpoints", "secrets"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["extensions", "networking.k8s.io"]
  resources: ["ingresses", "ingressclasses"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["extensions", "networking.k8s.io"]
  resources: ["ingresses/status"]
  verbs: ["update"]
- apiGroups: ["traefik.containo.us"]
  resources: ["*"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: traefik
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: traefik
subjects:
- kind: ServiceAccount
  name: traefik
  namespace: myapp
```

### 7. Traefik Deployment y Services
```yaml
# traefik.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: traefik
  namespace: myapp
  labels:
    app: traefik
spec:
  replicas: 1
  selector:
    matchLabels:
      app: traefik
  template:
    metadata:
      labels:
        app: traefik
    spec:
      serviceAccountName: traefik
      containers:
      - name: traefik
        image: traefik:v2.10
        args:
        - --log.level=DEBUG
        - --api.dashboard=true
        - --api.insecure=true
        - --entrypoints.web.address=:4000
        - --entrypoints.dashboard.address=:8080
        - --providers.kubernetesIngress
        - --providers.kubernetesCRD
        ports:
        - containerPort: 4000
          name: web
        - containerPort: 8080
          name: dashboard
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
---
apiVersion: v1
kind: Service
metadata:
  name: traefik-web
  namespace: myapp
spec:
  selector:
    app: traefik
  ports:
  - port: 4000
    targetPort: 4000
    nodePort: 30400
  type: NodePort
---
apiVersion: v1
kind: Service
metadata:
  name: traefik-dashboard
  namespace: myapp
spec:
  selector:
    app: traefik
  ports:
  - port: 8080
    targetPort: 8080
    nodePort: 30800
  type: NodePort
```

### 8. Ingress para la aplicación web
```yaml
# web-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  namespace: myapp
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: web
spec:
  ingressClassName: traefik
  rules:
  - host: localhost
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

## Instrucciones de Despliegue

### 1. Construir y subir la imagen de la aplicación web
```bash
# Construir la imagen (desde el directorio con tu Dockerfile)
docker build -t your-web-app:latest .

# Si usas un registry local o remoto
docker tag your-web-app:latest your-registry/your-web-app:latest
docker push your-registry/your-web-app:latest
```

### 2. Aplicar los manifiestos en orden
```bash
# Crear namespace
kubectl apply -f namespace.yaml

# Aplicar RBAC para Traefik
kubectl apply -f traefik-rbac.yaml

# Crear almacenamiento para Redis
kubectl apply -f redis-storage.yaml

# Desplegar Redis
kubectl apply -f redis.yaml

# Desplegar aplicación web
kubectl apply -f web-app.yaml

# Desplegar Traefik
kubectl apply -f traefik.yaml

# Crear Ingress
kubectl apply -f web-ingress.yaml
```

### 3. Verificar el despliegue
```bash
# Ver todos los recursos
kubectl get all -n myapp

# Ver logs
kubectl logs -f deployment/web -n myapp
kubectl logs -f deployment/redis -n myapp
kubectl logs -f deployment/traefik -n myapp

# Verificar Ingress
kubectl get ingress -n myapp
```

### 4. Acceder a la aplicación
- **Aplicación web**: http://localhost:30400
- **Dashboard de Traefik**: http://localhost:30800

## Principales Diferencias y Consideraciones

### Cambios Arquitectónicos:
1. **Networking**: En lugar de enlaces automáticos de Docker, usamos Services de Kubernetes
2. **Storage**: Los volúmenes se manejan con PV/PVC en lugar de bind mounts
3. **Service Discovery**: Las aplicaciones se comunican usando nombres de servicios DNS
4. **Load Balancing**: Traefik usa Ingress controllers en lugar de labels de Docker
5. **Scaling**: Fácil escalado horizontal con `replicas`

### Beneficios de K3s:
- **Alta disponibilidad** con múltiples réplicas
- **Health checks** automáticos con liveness/readiness probes
- **Resource limits** para mejor gestión de recursos
- **Rolling updates** sin downtime
- **Service mesh** capabilities con Traefik

### Configuración adicional recomendada:
1. **SSL/TLS**: Agregar certificados con cert-manager
2. **Monitoring**: Integrar Prometheus y Grafana
3. **Secrets**: Usar Kubernetes Secrets para datos sensibles
4. **ConfigMaps**: Para configuraciones de aplicación
