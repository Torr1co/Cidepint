# GRUPO 27

### Para correr el programa principal CIDEPINT

// Antes de empezar debe tener instalado docker con una sesion iniciada, npx para npm y poetry

Nos movemos a la carpeta admin

```
    cd admin
```

instalamos las dependencias de poetry y npm

```
    poetry install
    npm install

```

Una vez instaladas componemos nuestro container docker a partir del archivo .env para alojar nuestra base de datos (tienen el formato en .env.example)

```
    docker compose up -d
```

Activamos el ambiente virtual

```
    poetry shell
```

Iniciamos los hooks de pre-commit para mantener un formato estable en todo el desarollo

```
    pre-commit install
```

Corremos flask, como es desarollo siempre debe ser con la flag DEBUG

```
    flask run --debug
```
