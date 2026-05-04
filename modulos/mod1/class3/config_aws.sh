#!/bin/bash

# =================================================================
# Script: login_profesional.sh
# Descripción: Configura AWS CLI usando variables de entorno previas.
# Ideal para demostraciones de CI/CD o perfiles DevOps.
# =================================================================

echo "--- Verificando Entorno de FormaTEC ---"

# Verificar si las variables de entorno existen
if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "❌ ERROR: No se detectaron variables de entorno."
    echo "Por favor, ejecuta primero:"
    echo "export AWS_ACCESS_KEY_ID='tu_key'"
    echo "export AWS_SECRET_ACCESS_KEY='tu_secret'"
    exit 1
fi

echo "✅ Variables detectadas. Configurando AWS CLI..."

# Establecer la región por defecto si no existe
REGION=${AWS_DEFAULT_REGION:-us-east-1}

# Aplicar configuración al perfil default sin pedir input
aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
aws configure set region "$REGION"
aws configure set output json

echo "--------------------------------------------"
echo "¡Sincronización completada!"
echo "Validando identidad con el servicio STS..."

# Comando para verificar quién soy
USER_ARN=$(aws sts get-caller-identity --query "Arn" --output text 2>/dev/null)

if [ $? -eq 0 ]; then
    echo "🚀 LOGIN EXITOSO"
    echo "Usuario: $USER_ARN"
    echo "Región: $REGION"
else
    echo "❌ ERROR: Las credenciales del entorno son inválidas."
fi