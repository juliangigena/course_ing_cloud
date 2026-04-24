# Guía de Demo: Alta de Cuenta y Seguridad Inicial (IAM)

El objetivo de esta demo es configurar una cuenta de AWS siguiendo las mejores prácticas de seguridad de 2026.

## Fase 1: Creación de la Cuenta (Root User)

Registro: Ir a aws.amazon.com y crear la cuenta.

Nota para la clase: Explicar que se requiere tarjeta de crédito, pero el "Free Tier" cubre la mayoría de lo que veremos.

Configuración Root:

Activar MFA (Multi-Factor Authentication) de inmediato. Es el paso #1 de seguridad.

Crear un alias para la cuenta en el dashboard de IAM para facilitar el inicio de sesión.

## Fase 2: Aplicando Least Privilege (IAM)

Explicación: Nunca operaremos con el Root User para tareas diarias. Vamos a crear un usuario con permisos administrativos pero bajo el control de IAM.

Ir al servicio IAM: (Identity and Access Management).

Crear Grupo de Usuarios:

Nombre: Administrators.

Política: Vincular la política AdministratorAccess.

Por qué: Gestionar permisos por grupos es más escalable y auditable que por usuarios individuales.

Crear Usuario:

Nombre: tu-nombre-admin.

Acceso: Habilitar acceso a la Consola de AWS y crear una contraseña segura.

Asignación: Agregar el usuario al grupo Administrators.

Habilitar MFA: Configurar obligatoriamente el segundo factor para este nuevo usuario.

## Fase 3: El "Hito de Seguridad"

Cerrar sesión del Root User.

Entrar con el nuevo usuario IAM (usando el alias de la cuenta).

Concepto clave: Explicar que para un Least Privilege real, en lugar de AdministratorAccess, usaríamos permisos específicos (ej: AmazonEC2FullAccess).

## Fase 4: Configuración de Alertas (Bonus)

Configurar una alarma de facturación es vital para trabajar con tranquilidad. Sigue estos pasos para recibir un correo si el gasto proyectado supera los $5 USD:

Habilitar Alertas de Facturación:

En el buscador de la consola, ve a Billing and Cost Management.

En el menú lateral, ve a Billing Settings.

Marca la opción "Receive Billing Alerts" (Recibir alertas de facturación) y guarda los cambios.

Crear la Alarma en CloudWatch:

Cambia la región de la consola a N. Virginia (us-east-1) (las métricas de facturación siempre residen allí).

Busca el servicio CloudWatch.

En el menú lateral, ve a Alarms -> All alarms y haz clic en Create alarm.

Seleccionar Métrica:

Haz clic en Select metric -> Billing -> Total Estimated Charge.

Selecciona la métrica EstimatedCharges y haz clic en Select metric.

Definir Condiciones:

Threshold type: Static.

Whenever EstimatedCharges is...: Greater (Mayor que).

than...: Define el valor, por ejemplo: 5 (USD).

Configurar Notificación (SNS):

En la sección de Notification, selecciona Create new topic.

Topic name: AlertaGastosCloud.

Email endpoints: Ingresa tu correo electrónico personal.

Haz clic en Create topic. ¡Revisa tu bandeja de entrada y confirma el correo de suscripción que te enviará AWS!

Finalizar:

Ponle un nombre a la alarma (ej: Alarma-Gastos-Mas-de-5USD) y haz clic en Create alarm.