import boto3


def lambda_handler():
    ec2 = boto3.client('ec2', region_name='us-east-1')

    # Busca todas las instancias encendidas
    response = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )

    to_stop = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            tags = {t['Key']: t['Value'] for t in instance.get('Tags', [])}

            # LÓGICA VULNERABLE:
            # Si no es explícitamente Produccion, O si no tiene tags, la apaga.
            if tags.get('Entorno') != 'Produccion':
                to_stop.append(instance['InstanceId'])

    if to_stop:
        print(f"🔴 APAGANDO INSTANCIAS: {to_stop}")
        ec2.stop_instances(InstanceIds=to_stop)
        print("🚨 GRAVE ERROR: ¡Se apagó Producción por falta de etiquetas!")
    else:
        print("No se encontraron instancias para apagar.")


if __name__ == "__main__":
    lambda_handler()
