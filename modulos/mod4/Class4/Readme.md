# Ejecucion 

## Activar minikube o cluster de k8s con CNI
    minikube start --driver=docker --cni=calico

## Antes
### Aplicar yaml
    kubectl apply -f app-vulnerable.yml

### Entar al pod
    kubectl exec -it app-vulnerable -- bash
    # Ejecutar
        # 1. Mostrar que eres el usuario root
        whoami
        # Resultado: root

        # 2. Instalar herramientas o ejecutar acciones no autorizadas
        apt install -y nmap
        # Dentro del pod app-vulnerable:
        curl -LO "https://dl.k8s.io/release/v1.30.0/bin/linux/amd64/kubectl"
        chmod +x kubectl
        mv kubectl /usr/local/bin/

        # Verificar que habla con la API del cluster usando el ServiceAccount montado:
            kubectl get pods


## Despues
### Aplicar yaml
    kubectl apply -f app-sec.yaml

    # Crear pod atacante de prueba
    kubectl run pod-atacante --image=alpine -- sleep 3600

    # Capturar IP de la DB
    DB_IP=$(kubectl get pod db-sensible -o jsonpath='{.status.podIP}') 

    # Probar la conexión
    kubectl exec -it pod-atacante -- nc -zv -w 3 $DB_IP 6379 -> timeout

### Entrar al pod
    kubectl exec -it app-segura -- sh
        #verificar IP
         nc -zv -w 3 10.244.120.70 6379 -> open

    Entrar al pod sniffer
        kubectl exec -it pod-intruso-sniffer -- bash
        #verificar ip
        nc -zv -w 3 10.244.120.70 6379 -> succeeded

