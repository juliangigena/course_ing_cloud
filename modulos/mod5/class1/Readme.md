# Entorno 1

## Crear Ec2
    bash crear_ec2_sin_tags.sh

## Verificar lo creado

## ejecutar el python
    python3 lambda_apaga_todo.py

    si falla por: "ModuleNotFoundError: No module named 'boto3'" -> pip install boto3

## Se apagan las Ec2

## Eliminar entorno1
    python3 eliminar_ec2_sin_tags.py 

## Moraleja
    Resultado en vivo: La Lambda apaga tanto la EC2 de Desarrollo como la de Producción.  Lección FinOps: Intentar automatizar el ahorro de costos (Operar) sin antes haber clasificado la infraestructura (Informar) causa interrupciones de negocio críticas. 

# Entorno 2

## Crear SCP
    Pasos previos:
        # 1. Crear la Organización en tu cuenta
        aws organizations create-organization

        # 2. Habilitar el tipo de política SERVICE_CONTROL_POLICY
        aws organizations enable-policy-type \
        --root-id $(aws organizations list-roots --query "Roots[0].Id" --output text) \
        --policy-type SERVICE_CONTROL_POLICY
    
        aws organizations create-policy \
        --content file://scp_politica_tags.json \
        --description "Fuerza la inclusion del tag CentroDeCostos al crear EC2" \
        --name "SCP-Obligar-CentroDeCostos" \
        --type SERVICE_CONTROL_POLICY

        aws organizations list-policies --filter SERVICE_CONTROL_POLICY --query "Policies[?Name=='SCP-Obligar-CentroDeCostos'].Id" --output text  -> p-8njrh3jw  

        POLICY_ID=$(aws organizations list-policies --filter SERVICE_CONTROL_POLICY --query "Policies[?Name=='SCP-Obligar-CentroDeCostos'].Id" --output text)

        aws organizations attach-policy \
        --policy-id $POLICY_ID \
        --target-id $ACCOUNT_ID
        ############
        aws iam create-policy \
        --policy-name DenyEC2WithoutCostCenter \
        --policy-document file://scp_politica_tags.json

        # Obtener el nombre del usuario actual
        USER_NAME=$(aws sts get-caller-identity --query "Arn" --output text | cut -d'/' -f2)

        # Adjuntar la política al usuario
        aws iam attach-user-policy \
        --user-name $USER_NAME \
        --policy-arn arn:aws:iam::$(aws sts get-caller-identity --query "Account" --output text):policy/DenyEC2WithoutCostCenter

## Crear infraestructura con terraform


