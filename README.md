# Bachelorarbeit_FS22
 
## Setup
Clone this project to a local folder.

### Poetry
Install [Poetry](https://python-poetry.org/docs/) which is a tool for dependency management and packaging in Python. Poetry requires Python 2.7 or 3.5+. You can install Poetry using the following commands.

#### osx / linux / bashonwindows:
```curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python```

#### or windows powershell:
```(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python```

### Run the project from shell

#### 1. Go to project folder

```cd ba_code```

#### 2. Get all the packages

```poetry install```

#### 3. Get into poetry environment

```poetry shell```

#### 4. See all availible commands

```python cli_executor.py --help```

#### 5. Execute a predefined command

e.g. ```python cli_executor.py extract-reviews```

### Run the project with PyCharm
Download and install [PyCharm](https://www.jetbrains.com/de-de/pycharm/) which is a Python IDE. Open the IDE after the installation and click on **"Open"** as depicted below.</br></br>
![pycharm_window_img](https://github.com/fatihsolmaz22/Bachelorarbeit_FS22/blob/main/README_resources/01_PyCharm_Window.png)

Navigate to the location where you cloned this project and select **"ba_folder"** and click on **"ok"**.</br></br>
![open_file_or_project_img](https://github.com/fatihsolmaz22/Bachelorarbeit_FS22/blob/main/README_resources/02_Open_File_Or_Project.png)

Once the project has been loaded go to **"File"** --> **"Settings"**.</br></br>
![file_settings_img](https://github.com/fatihsolmaz22/Bachelorarbeit_FS22/blob/main/README_resources/03_File_Settings.png)

Install the Poetry plugin as shown below.</br></br>
![poetry_plugin_img](https://github.com/fatihsolmaz22/Bachelorarbeit_FS22/blob/main/README_resources/04_Poetry_Plugin_Installation.png)

After the installation of the plugin open a Python script e.g. test.py. The IDE recognizes that there is no Python Interpreter configured for the project and suggests three options. Click on **"Create a poetry environment using pyproject.toml"** to complete the project setup.</br></br>
![poetry_plugin_img](https://github.com/fatihsolmaz22/Bachelorarbeit_FS22/blob/main/README_resources/05_Create_poetry_using_pyproject.png)
