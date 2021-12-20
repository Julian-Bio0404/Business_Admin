# Business Admin

Backend de una aplicación web para el ontrol de acceso a sedes ( puntos de acceso ) para personal
de empresas.

## Correr el proyecto:

1. Clone este proyecto con:
```bash
git clone https://github.com/Julian-Bio0404/Gaman.git
```

2. En la raíz del proyecto, construya y levante los servicios con:
to run the project, run:
```bash
docker-compose build
docker-compose up
```

3. Crear un superusuario, en otra ventana de consola, ejecute:
```bash
docker-compose run --rm django python manage.py createsuperuser
```

4. Verificar el superusuario (esto es importante, ya que si no se verifica, no podrá hacer login)
```bash
docker-compose run --rm django python manage.py verifysuperusers
```

## Api Docs
En el apartado de Features hay una breve descripción de las funcionalidades de la api, pero para tener ejemplo y saber exactamente como comunicarse con ella, puede:
- Importar el archivo Business-Admin.postman_collection.json a su cuenta de postman
- O visitar: https://documenter.getpostman.com/view/15752557/UVRAK7RF

## Features
- Login: con email y password, al momento de hacer login, se creará un token de acceso
- Crear una compañía: sólo el superusuario podrá crearlas
- listar compañias: cualquier usuario autenticado podrá listarlas
- detalle de una compañía: cualquier usuario autenticado podrá ir al detalle
- Añadir un administrador para la empresa: sólo el superusuario podrá añadirlo, en el proceso se crea el usuario administrador y se envía un token de verificación al email que se  proporcionó. el usuario que figurará como admin de la empresa, tendrá que enviar ese toquen para verificar su cuenta y así permitir que este haga login en la api.
El envío se realiza asíncornamente con celery y redis. (Email-Backend: En consola se simula el mensaje y se imprimirá el token)
- Verificar cuenta de usaurio: copiar y pegar el token que se envío como email en consola
- Actualizar o eliminar una empresa: sólo el admin de la empresa prodrá hacerlo
- Invitar a inscribirse a un empleado: sólo el admin de la empresa podrá hacerlo, proporcionando un email unico. Se enviará un token de invitación al email proporcionado, el empleado deberá proporcionar ese token y sus datos personales, después de esto, figurará como empleado automáticamente y se enviará un token de verificación al correo con el cual se inscribió el empleado.
- Listar empleados de una empresa: cualquier usuario autenticado, podrá hacerlo
- Crear puntos de acceso de una empresa: sólo el admin de la empresa podrá crearlos, el país, estado y ciudad se determinan segun la geolocalización que se proporcione. Estos datos se obtiene por medio de la comunicación de una api de tercero, disponible en: https://nominatim.openstreetmap.org/ui/about.html
- Listar e ir al detalle de un punto de acceso: cualquier usuario autenticado podrá hacerlo
- Actualizar un punto de acceso: sólo el admin de la empresa podrá hacerlo
- Crear, activar, desactivar o eliminar una franja horaria de acceso al punto de acceso: sólo el admin del empresa, podrá hacerlo
- Listar horas de acceso a un punto de acceso: sólo el admin y los empleados podrán hacerlo. Los empleados sólo podrán listar las horas de acceso a los que fueron asignados
- Verificar acceso a un punto de acceso: sólo los empleados de la empresa a la que pertenece el punto dde acceso, prodán verificar su acceso, si es empleado y no tiene horas de acceso, según la hora actual y su punto de geolocalización, retornará False, de lo contrario, retornará True
- Cada vez que un usuario verifica su acceso y este retorna False, se envía una notificación asincronamente al correo del admin de la empresa.
- Actualizar contraseña de usuario
- Recuperar contraseña de usuario