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

Parte 2: Automatización con CloudFormation

Desplegaremos un esquema de 2 capas: una VM (EC2) y una base de datos (RDS MySQL).

A. La Plantilla (template.yaml)

Guarda este contenido en un archivo llamado infra.yaml:

AWSTemplateFormatVersion: '2010-09-09'
Description: 'Esquema de 2 capas: EC2 Publica + RDS Privada (Capa Gratuita)'

Resources:
  MyVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 172.16.0.0/16
      EnableDnsSupport: true
      EnableDnsHostnames: true
      Tags: [{Key: Name, Value: Lab-IaC-VPC}]

  PublicSubnet:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MyVPC
      CidrBlock: 172.16.1.0/24
      AvailabilityZone: !Select [ 0, !GetAZs '' ]
      MapPublicIpOnLaunch: true
      Tags: [{Key: Name, Value: Public-App-Subnet}]

  PrivateSubnetA:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MyVPC
      CidrBlock: 172.16.2.0/24
      AvailabilityZone: !Select [ 0, !GetAZs '' ]
      Tags: [{Key: Name, Value: Private-DB-Subnet-A}]

  PrivateSubnetB:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MyVPC
      CidrBlock: 172.16.3.0/24
      AvailabilityZone: !Select [ 1, !GetAZs '' ]
      Tags: [{Key: Name, Value: Private-DB-Subnet-B}]

  InternetGateway:
    Type: AWS::EC2::InternetGateway

  VPCGatewayAttachment:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref MyVPC
      InternetGatewayId: !Ref InternetGateway

  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref MyVPC

  DefaultPublicRoute:
    Type: AWS::EC2::Route
    DependsOn: VPCGatewayAttachment
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway

  PublicSubnetRouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PublicRouteTable
      SubnetId: !Ref PublicSubnet

  WebServerSG:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Permitir HTTP y SSH
      VpcId: !Ref MyVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0

  DatabaseSG:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Permitir MySQL solo desde el WebServer
      VpcId: !Ref MyVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 3306
          ToPort: 3306
          SourceSecurityGroupId: !Ref WebServerSG

  EC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: t2.micro
      ImageId: ami-0c101f26f1473a30b # Amazon Linux 2023 (Cambiar segun region)
      SubnetId: !Ref PublicSubnet
      SecurityGroupIds: [!Ref WebServerSG]
      Tags: [{Key: Name, Value: WebServer-Lab}]

  DBSubnetGroup:
    Type: AWS::RDS::DBSubnetGroup
    Properties:
      DBSubnetGroupDescription: Subredes para la DB
      SubnetIds: [!Ref PrivateSubnetA, !Ref PrivateSubnetB]

  MyDB:
    Type: AWS::RDS::DBInstance
    Properties:
      DBName: mydb
      AllocatedStorage: '20'
      DBInstanceClass: db.t3.micro
      Engine: mysql
      MasterUsername: admin
      MasterUserPassword: Password123!
      VPCSecurityGroups: [!Ref DatabaseSG]
      DBSubnetGroupName: !Ref DBSubnetGroup
      PubliclyAccessible: false
      DeleteAutomatedBackups: true
      SkipFinalSnapshot: true

Outputs:
  InstancePublicIP:
    Value: !GetAtt EC2Instance.PublicIp
  DBEndpoint:
    Value: !GetAtt MyDB.Endpoint.Address


B. Despliegue mediante AWS CLI

Si tienes configurado el AWS CLI en tu máquina, sigue estos pasos:

Validar la plantilla:
Antes de lanzar, verifica que no haya errores de sintaxis:

aws cloudformation validate-template --template-body file://infra.yaml


Crear el Stack:
Ejecuta el siguiente comando para iniciar el despliegue:

aws cloudformation create-stack \
  --stack-name Stack-Clase3-Redes \
  --template-body file://infra.yaml \
  --capabilities CAPABILITY_IAM


Monitorear el estado:
Puedes ver cómo progresa desde la terminal:

aws cloudformation describe-stacks --stack-name Stack-Clase3-Redes --query "Stacks[0].StackStatus"


Obtener los resultados (Outputs):
Una vez que el estado sea CREATE_COMPLETE, obtén la IP de la VM y el endpoint de la DB:

aws cloudformation describe-stacks --stack-name Stack-Clase3-Redes --query "Stacks[0].Outputs"


Eliminar todo (Limpieza de bono):
Al terminar la clase, borra todo para no gastar de más:

aws cloudformation delete-stack --stack-name Stack-Clase3-Redes


Tips de Ahorro y Bono

Capas: RDS db.t3.micro y EC2 t2.micro están cubiertos por el Free Tier.

Bono de 100 USD: Aunque son servicios baratos, el comando delete-stack es tu mejor amigo para asegurar que el bono dure todo el cuatrimestre.