# myCRypto
 ## Instalación
 1. Ejecutar
 ```

pip install -r requirements.txt

```

2. Crear _config.py
Renombrar `_config_templates.py` a `config.py` e informar correctamente sus claves.

3. Informar correctamente .env(opcional)
Renombrar `.env_template` a `.env` e infomar las claves

    - FLASK_APP=run.py
    - FLASK_ENV= el que quieras `development` o `production` 

4. Crear BD

    Desde el directorio /data ejecutar
        - sqlite3 <nombre_bd>.db
    Desde la consola de sqlite3 ejecutar
        - .read migrations.sql
    Comprobar que se han creado las tablas
        - .tables
    Salir
        - .q
