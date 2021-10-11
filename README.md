# FastCash Project

This repository contains the FastCash web api code for the course **PythonBiellaGroup FastAPI nights**.

This project contains an example of FastAPI Projects built during the course.


## Install and configure the project

First of all it's important to install `poetry`.  
If you don't know how to install it please follow this guide

If you want to save the virtualenv inside the project folder please do: 

Then you have to initialize the project with: `poetry install`

If you want to use the environment variable, you have to create a .env variable with this values inside:
```bash
APP_DB_NAME=fastcash
APP_DB_USER=root
APP_DB_PASSWORD=<yourpassword>
APP_DB_PORT=<yourport>
APP_DB_HOST="fastcash-db"

APP_ENDPOINT_HOST="localhost"
APP_API_ENDPOINT_PORT=8044
APP_DOCKER_PORT=8044
APP_ENDPOINT_PORT=8044
APP_SECRET_KEY=<yourappsecret>
APP_DEBUG_MODE="False"
APP_VERBOSITY="DEBUG"

POSTGRES_DATA_DIR=<your_machine_data_folder>
POSTGRES_BACKUP_DIR=<your_machine_backup_folder>
```


## VSCode settings

To configure and use vscode as main IDE with Python it's important to create two main files: `settings.json` and `launch.json`.

### Setting the Vscode Ide

This settings can be done only the first time because if you log-in with your Github or Microsoft account it's possible to keep all your settings in every machine and vscode you use.

Please remember to **install the required extensions for vscode** before.

First of all it's important to create inside the project a folder called: `.vscode`.

Inside this folder create new file with the name: `launch.json`.
This file it's important because contains all the settings for the vscode python debugger.

The content of the file is this one (paste inside the file).
```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
      {
        "name": "Python: Current File",
        "type": "python",
        "request": "launch",
        "program": "${file}",
        "console": "integratedTerminal",
        "cwd": "${workspaceFolder}",
        "env": {
          "PYTHONPATH": "${cwd}",
          "VERBOSITY": "DEBUG",
          
        }
      },
      {
        "name": "FastAPI",
        "type": "python",
        "request": "launch",
        "module": "uvicorn",
        "args": ["app.main:app", "--reload", "--port", "8042"],
        "env": {
            "PYTHONPATH": "${cwd}",
            "API_ENDPOINT_PORT": "8042",
            "VERBOSITY": "DEBUG"
        }
      }
    ]
  }

```
With the `Python: Current File` you can launch the debugger on a single python file and with `Flask Backend` you can launch the flask application with the VSCode debugger directly (in Debug mode of course)


Then you have to create another file inside the `.vscode` folder in your project, this file is called: `settings.json`.
The file contains all the **python settings and information for the project and the ide**.

After you have created the file and installed the project with poetry launch: `poetry show -v`, then copy the first path of your virtualenv.

Now paste this settings inside the new `settings.json` file.
```json
{
    "python.pythonPath": "<path of your local virtualenv>/bin/python",
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": false,
    "python.linting.enabled": true
}

```
Substitute `<path of your local virtualenv>` with the path copied from `poetry show -v` command.

After this reload vscode and every time you open a new windows vscode automatically activate the venv created with poetry for you.

### Usefull dev extensions
- Python (with Pylance):
- Jupyter:
- Docker: 
- Todo Tree:
- Remote development:
- Live share: 
- docks-markdown:
- docks-preview:
- Git History:
- Git Lens:
- indent-rainbow: 
- Prettier - Code formatter

### Other informations about vscode or python configurations

If you want to have other informations please check our website (English and Italian only): https://pythonbiellagroup.it

## Launch and debug (development mode)

Instructions to launch and debug the project locally with vscode.

1. Clone the project
2. Install vscode + poetry (if you don't know to install poetry check this guide)
3. Set vscode (and vscode related files for debugging and venv) with the instructions in this readme file
4. Install the dependencies of the project with poetry by doing: `poetry install`
5. If you want to activate the venv created with poetry in your terminal do: `poetry shell`
6. After all the configurations restart vscode, then vscode will update your default IDE virtual env by default (if all the configurations are correct)
7. You can use the vscode debugger to launch the application or to launch a single python script file


The environment variabile called DEBUG_MODE should be False if you want to test the app via gunicorn.
If the environment variable is True you should use the Debug function of VS Code.

If you experience some changes to the pyproject.toml file, you can update your local version of the libraries and environment by running the command: `poetry update`

If you want you can use also the shell script: `launch-debug.sh` to test the project in debug mode with Flask and without gunicorn

## Documentation

If you want to see the official documentation of the project you can check it here:
   - http://localhost:8042/docs
   - http://localhost:8042/redoc

The OpenAPI documentation is created automatically by FastAPI.

Please consider that the port and the host can be changed based on your personal project configuration.

## Launch in production mode

First of all check if you have all the tools installed correctly on your machine.

If you want to launch the code (flask backend) in production mode with `gunicorn` you can use the `launch.sh` script located inside the main folder.

Remember to set the permissions of the script: `sudo chmod +x launch.sh`
Launch with: `./launch.sh`

If you get the error: `gunicorn: not found` you need to activate the poetry env by doing: `poetry shell`

You can also launch the single docker compose if you want to test the code inside the docker container by doing `docker-compose up --build -d`



## Considerations and know issues

To use the system with psycopg2 for the postgres database connection it's important to install in your system (linux-based) the requirements: `sudo apt-get install libpq-dev`

To launch the project from terminal if you are on the project root you have to do: `PYTHONPATH="./" python ./test/<name of the script>.py`

Be carefull not to install virtualenv via `apt` on linux, but use virtualenv by `pip`.

### Useful commands
If you want to restore docker on your machine:
```bash
docker system prune --all
```

Open the port on your machine if you are developing remotely (in a VPS for example and in a Linux OS based):
```bash
# if you want to launch the mapping in detach mode
ssh -f -N pbg

# if you launch the mapping in attach mode inside your current bash window
ssh -f pbg
```

With this command you have to set your <pbg> ssh config profile with the ports in the `~/.ssh/config` file.  
For example:
```bash
# put this inside the config file
LocalForward 8042 127.0.0.1:8042
LocalForward 8000 127.0.0.1:8000
```