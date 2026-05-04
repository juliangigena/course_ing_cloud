Laboratorio Práctico: Arquitectura de Redes en AWS

Este laboratorio se divide en dos fases: el entendimiento manual de la red y la automatización mediante Infraestructura como Código (IaC).

Parte 1: Creación Manual de una VPC (The Hard Way)

El objetivo es entender cada componente antes de automatizarlo.

1. Crear la VPC

Ve a VPC Dashboard -> Your VPCs -> Create VPC.

Name tag: Lab-Manual-VPC.

IPv4 CIDR block: 10.0.0.0/16.

Deja el resto por defecto y haz clic en Create VPC.

2. Crear las Subredes (Subnets)

Subred Pública: Public-Subnet | AZ: us-east-1a | CIDR: 10.0.1.0/24.

Subred Privada: Private-Subnet | AZ: us-east-1a | CIDR: 10.0.2.0/24.

3. Conexión y Enrutamiento

Crea un Internet Gateway (Lab-IGW) y conéctalo a la VPC.

Crea una Route Table (Public-RT), agrega una ruta 0.0.0.0/0 hacia el IGW y asóciala a la Public-Subnet.
