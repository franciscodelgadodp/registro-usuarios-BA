# API Banco Azteca Registro de Usuarios

## Descripción

API para registro de usuarios con datos validados

## Herramientas

Python, FastAPI, Postgres

## Requerimientos

Python >= 3.6, un manejador de ambientes virtuales (venv, pipenv) y Make para correr comandos make

## Run the project

1. Inicializa un ambiente virtual de python
2. Activa el ambiente
3. Correr `make install`
4. Crea una copia del archivo .env-example y renombrarlo .env llenando las variables con los valores indicados
5. Correr `make start` to start the project
6. Para la documentación ir a la url `localhost:8000/docs` or `localhost:8000/redoc`

## Explicación de la API

Esta es una API para el registro de usuarios, se tienen 3 niveles de usuario: Admin, Lectura, y Escritura parcial.

Para el usuario de Admin se cuenta con acceso a todas las operaciones, las credenciales del usuario son **carlos_hf@me.com** y **admin**

Para el usuario de Lectura se cuenta con acceso únicamente a las operaciones **GET** el resto de las operaciones aparecerá un mensaje de que las credenciales no son válidas. Las credenciales de este usuario son **julian_ag@me.com** y **read-only**

Para el usuario de Escritura parcial se cuenta con acceso de lectura y de escritura pero como menciona la palabra parcial, únicamente puede hacer cambios en 3 campos: _estado_, _municipio_ y _cp (código postal)_, si intenta este usuario editar otros campos marcará el error de que no tiene permiso de editar ese campo
Las credenciales de este usuario son **efren_mv@me.com** y **write-job**

## Permisos

Los permisos se manejan con scopes que vienen incluidos en la token, estos permisos se generan con el modelo de Scope que tiene un atributo id, y otro llamado name que es un string dividido en 3 partes **entidad:accion:atributos**

Esta estructura permite manejar los permisos a niveles mas finos que es lo que se buscaba para controlar atributos que uno puede manejar. Se especifica la entidad en la que se tiene permiso, la accion que puede ser read, create, update o delete y al final los atributos que se van a afectar con el comando (_Solo aplica para update_).

Para la primera entrada/permiso a la operacion unicamente se checa las primeras 2 partes del string del scope para asegurar que mínimo puede acceder a dicha operación. Esto es suficiente en la mayoría de las operaciones excepto para la operación de modificar una entidad aquí entra la tercera parte del string que indica los atributos afectados

Si se quiere crear el scope que permita modificar todos los elementos de la entidad Usuario entonces se veria asi **user:update:\***, el asterisco indica que afecta a todos los atributos.

En el caso que se quiera limitar a ciertos atributos entonces el ejemplo se vería así: **user:update:nombre,estado**. Aquí el usuario unicamente puede modificar los atrivutos de nombre y estado de la entidad de Usuario

Si el usuario no tiene ningun scope en su token entonce no tendrá ningun acceso a las apis excepto la de login que no tendrá efecto alguno en las apis porque no tiene los permisos para usarlas
