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

Ejecutar `migrations.sql` con `sqlite3` en el fichero elegido como base de datos