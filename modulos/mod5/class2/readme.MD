# Entorno hibrido:
    entorno_hibrido/
    ├── docker-compose.yml          # Infraestructura On-Premise (PostgreSQL)
    ├── init.sql                    # Esquema inicial de la DB
    ├── main.tf                     # Código de Terraform para la EC2 en AWS
    ├── inventory.ini               # Inventario dinámico/estático para Ansible
    └── playbook.yml                # Playbook de Ansible para configurar la EC2

## Paso 1 "entorno local"
    Ejecutar el compose:
        docker-compose up -d
    Ejecutar ssh key
        ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""

## Paso 2 "entorno AWS"
    Ejecutar terraform

## Paso 3 "configurar EC2"
    Reemplazar <IP_EC2> con la salida de Terraform
    ansible-playbook -i "<IP_EC2>," -u ec2-user --private-key ~/.ssh/id_rsa playbook.yml

## Ejecutar venta
    ssh -R 0.0.0.0:5432:localhost:5432 -i ~/.ssh/id_rsa ec2-user@18.212.87.56 -N

    curl -X POST http://<IP_EC2>/venta \
     -H "Content-Type: application/json" \
     -d '{"monto": 1500.50}'

    curl -X POST http://18.212.87.56/venta \
     -H "Content-Type: application/json" \
     -d '{"monto": 1500.50}'
## Verificar la venta
    docker exec -it postgres_onprem psql -U admin_banco -d banco_db -c "SELECT * FROM ventas;"