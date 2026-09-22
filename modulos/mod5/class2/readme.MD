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
        rm ~/.ssh/id_rsa ~/.ssh/id_rsa.pub # si no existe da un mensaje simil error
        ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""

## Paso 2 "entorno AWS"
    Ejecutar terraform

## Paso 3 "configurar EC2"
    Reemplazar <IP_EC2> con la salida de Terraform
    ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i "<IP_EC2>," -u ec2-user --private-key ~/.ssh/id_rsa playbook.yaml
    Ej: ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i "54.158.30.254," -u ec2-user --private-key ~/.ssh/id_rsa playbook.yaml

## Ejecutar venta
    # Correr este comando para simular una VPN
    ssh -i ~/.ssh/id_rsa ec2-user@<IP_EC2> "sudo sed -i 's/.*GatewayPorts.*/GatewayPorts yes/' /etc/ssh/sshd_config && sudo systemctl restart sshd"
    ssh -R 0.0.0.0:5432:localhost:5432 -i ~/.ssh/id_rsa ec2-user@<IP_EC2> -N

    Ej: ssh -i ~/.ssh/id_rsa ec2-user@54.158.30.254 "sudo sed -i 's/.*GatewayPorts.*/GatewayPorts yes/' /etc/ssh/sshd_config && sudo systemctl restart sshd"
        ssh -R 0.0.0.0:5432:localhost:5432 -i ~/.ssh/id_rsa ec2-user@54.158.30.254 -N

    # Para verificar los puertos
    ssh -i ~/.ssh/id_rsa ec2-user@<IP_EC2> "sudo netstat -tuln | grep 5432"
    Ej: ssh -i ~/.ssh/id_rsa ec2-user@54.158.30.254 "sudo netstat -tuln | grep 5432"
    Debemos de ver un mensaje similar a este:
        ➜  class2 git:(main) ✗ ssh -i ~/.ssh/id_rsa ec2-user@54.158.30.254 "sudo netstat -tuln | grep 5432"
            ** WARNING: connection is not using a post-quantum key exchange algorithm.
            ** This session may be vulnerable to "store now, decrypt later" attacks.
            ** The server may need to be upgraded. See https://openssh.com/pq.html
            tcp        0      0 0.0.0.0:5432            0.0.0.0:*               LISTEN     
            tcp6       0      0 :::5432                 :::*                    LISTEN  

    # En caso de necesitar limpiar la conexion correr este comando
    ssh -i ~/.ssh/id_rsa ec2-user@<IP_EC2> "sudo fuser -k 5432/tcp"
    Ej: ssh -i ~/.ssh/id_rsa ec2-user@54.158.30.254 "sudo fuser -k 5432/tcp"

    ssh -i ~/.ssh/id_rsa ec2-user@54.158.30.254 "sudo sed -i 's/.*GatewayPorts.*/GatewayPorts yes/' /etc/ssh/sshd_config && sudo systemctl restart sshd"

    curl -X POST http://<IP_EC2>/venta \
     -H "Content-Type: application/json" \
     -d '{"monto": 1500.50}'

    curl -X POST http://54.158.30.254/venta \
     -H "Content-Type: application/json" \
     -d '{"monto": 1500.50}'

## Verificar la venta
    docker exec -it postgres_onprem psql -U admin_banco -d banco_db -c "SELECT * FROM ventas;"