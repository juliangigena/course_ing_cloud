# Fase 1: El Escenario "Local"

## Docker Compose levantando Flask + PostgreSQL en tu computadora.
    # 1. Levantar entorno local
    docker-compose up -d --build

    # 2. Probar inserción de datos
    curl -X POST http://localhost/venta -H "Content-Type: application/json" -d '{"monto": 500.00}'

    # 3. SIMULACIÓN DE FALLA LOCAL: Borrar contenedor de DB
    docker rm -f postgres_local

    # 4. Probar de nuevo (Dará Error 500 / Connection refused)
    curl -X POST http://localhost/venta -H "Content-Type: application/json" -d '{"monto": 500.00}'

    # PREGUNTA A LA CLASE: ¿De quién es la responsabilidad de recuperar los datos y el servicio?
    # Limpieza local
    docker-compose down -v

# Fase 2: Entorno IaaS
    Ejecutar ssh key
        rm ~/.ssh/id_rsa ~/.ssh/id_rsa.pub # si no existe da un mensaje simil error
        ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""

    Crear EC2 con terrarform

    Conectarse a la EC2
        ssh -i ~/.ssh/id_rsa ec2-user@<IP_EC2>

    Instalar todo:
        # En la EC2
        sudo yum update -y || sudo apt update -y
        sudo yum install -y docker || sudo apt install -y docker.io
        sudo systemctl start docker
        sudo systemctl enable docker
        sudo usermod -aG docker ec2-user
        sudo yum install -y docker-compose-plugin
        # 1. Crear el directorio de plugins para buildx si no existe
        sudo mkdir -p /usr/libexec/docker/cli-plugins
        # 2. Descargar la versión más reciente de buildx
        sudo curl -SL https://github.com/docker/buildx/releases/download/v0.19.3/buildx-v0.19.3.linux-amd64 -o /usr/libexec/docker/cli-plugins/docker-buildx
        # 3. Darle permisos de ejecución
        sudo chmod +x /usr/libexec/docker/cli-plugins/docker-buildx

        # Salir y reingresar para actualizar grupos
        exit

        # Correr en tu PC dentro de la carpeta fase1/ (remplazando IP y Key)
        scp -i ~/.ssh/id_rsa ../fase1/app.py ../fase1/Dockerfile ../fase1/docker-compose.yaml ec2-user@<IP_EC2>:/home/ec2-user/

        ssh -i ~/.ssh/id_rsa ec2-user@<IP_EC2>
        sudo docker compose up -d --build

# Fase 3: PaaS / Servicios Administrados
    # Desplegar el Stack con Serverless Framework
        # Desplegar todo el stack en AWS
            aws cloudformation deploy \
            --template-file serverless.yml \
            --stack-name demo-fase3-paas \
            --capabilities CAPABILITY_IAM \
            --region us-east-1
        
        #Obtener la IP del Contenedor Fargate y el Endpoint de RDS
            # 1. Obtener el ARN de la tarea corriendo en ECS
            TASK_ARN=$(aws ecs list-tasks --cluster cluster-demo-fase3 --query "taskArns[0]" --output text)
            # 2. Obtener la ENI (Interfaz de red) adjunta a la tarea Fargate
            ENI_ID=$(aws ecs describe-tasks --cluster cluster-demo-fase3 --tasks $TASK_ARN --query "tasks[0].attachments[0].details[?name=='networkInterfaceId'].value" --output text)
            # 3. Obtener la IP Pública asignada
            PUBLIC_IP=$(aws ec2 describe-network-interfaces --network-interface-ids $ENI_ID --query "NetworkInterfaces[0].Association.PublicIp" --output text)

            echo "IP Pública de la App: http://$PUBLIC_IP:5000"
        
        # Probar la Aplicación en Vivo (PaaS + Serverless)
            # Health Check
            curl http://$PUBLIC_IP:5000/

            # Registrar una Venta
            curl -X POST http://$PUBLIC_IP:5000/venta \
                -H "Content-Type: application/json" \
                -d '{"monto": 9990.00}'

        # Eliminar todo
            aws cloudformation delete-stack --stack-name demo-fase3-paas --region us-east-1



## Comando para pruebas:
    #1
    docker exec -it postgres_local psql -U admin_banco -d banco_db -c "SELECT * FROM ventas;"
    #2
    Simulación de Incidentes en Fase 2:

    Incidente 3 (Acceso SSH / Malas configuraciones):

        Mostrar el Security Group con 22 abierto a todo el mundo.

        Simular intervención/intrusión borrando o deteniendo el contenedor web:
        Bash

            docker stop web_app_local

        Debate: AWS dio la VM sana; la configuración del firewall (SG) e intrusión es 100% responsabilidad del cliente.

        Incidente 2 (Falla del Data Center / Apagón físico):

        Desde la consola de AWS, ir a EC2 > Instance State > Stop / Terminate.

        Intentar ingresar a la IP pública de la EC2 desde el navegador.

        Debate: La falla del hardware es de AWS, pero la indisponibilidad de la aplicación para el negocio es responsabilidad del cliente por depender de una sola instancia/AZ sin redundancia ni Auto Scaling.
    #3
        RDS_HOST=$(aws cloudformation describe-stacks \
        --stack-name demo-fase3-paas \
        --region us-east-1 \
        --query "Stacks[0].Outputs[?OutputKey=='RDSEndpoint'].OutputValue" \
        --output text)

        echo $RDS_HOST

        PGPASSWORD='Secret123!' psql -h $RDS_HOST -U admin_banco -d postgres -c "DROP DATABASE banco_db;"

        aws rds describe-db-snapshots \
        --db-instance-identifier banco-db-paas \
        --region us-east-1

        PGPASSWORD='Secret123!' psql -h $RDS_HOST -U admin_banco -d postgres -c "CREATE DATABASE banco_db;"