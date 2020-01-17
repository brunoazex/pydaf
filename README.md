# PyDaf - Python Data Analysis Framework

## Purpose
To abstract repetitive related tasks to retrieve, process and deliver data transformations. Also, to avoid reading lots of API docs in favour to get focused only writing code for `Processors`.


## Overview

- Drivers
    
    Their scope is to extract data from somewhere to respond a processor request. 
    There are two built-in drivers:
        
    - Postgres: Fetches data from Postgres databases
    - CSV: Loads data from comma separated files

- Processors

    Their scope is to request raw data from drivers, process as needed and deliver processed data to output specified on the run method. 
    
    They also can combine multiple datasets to transform data into a new one.

    There are two built-in dataset output helpers:

    ```python   
        def run(self):
            self.dataset \
                .to_console() \ # Prints out dataset into console
                .to_csv() # Exports processed data to `output_dir` specified in settings
    ```

- FlatDataSet

    Is a simple abstraction for DataFrame from panda library. 

- PivotDataSet

    Extends general abstraction supplied by FlatDataSet class into Pivot representation

## Configuration

There are configurations options at `config/` folder where you can put configuration files in yaml format for each app mode you want. 

These settings are mandatory independently of app mode:        
```yaml
    # App scope
    app:
        # Specifies where csv generated files will be stored
        output_dir: ./output 
    
    # Processors scope
    processors:
        # Specifies where the processors are located
        path: ./processors 
        # Array with processors to be run in the specified order
        queue:
            - Processor1
            - ProcessorN
    
    # Database scope is overriden by environment variables if they are present
    database:
        host: localhost
        database: postgres
        user: postgres
        pass: :)
```

The configuration is available through `App` singleton. For example:

```python
    from lib.app import App

    print(App.instance().environment.database.host)
    # Prints localhost
```

## Container

There is a Docker+Compose 'plug and play' files to get framework running on a Linux Alpine container.

The container recipe uses multistage building: 

* First, it makes it up a container to build `wheels` for all pip packages specified on the `container/packages.pip` file

* Then the generated wheels are copied from the builder container to the final container

* Then we call `pip` to install the compiled `wheels` on the final container

* Finally the `app/` folder gets copied into the final container and copied `wheels`gets removed to shrink final container size.

### Settings
You can put all environment variables in the .env file and docker will make them visible inside the container

#### App mode

By default app on a container runs at Production mode but you can run it in production mode. To achieve this just set

```bash
    APP_MODE=PROD #For production mode
    APP_MODE=DEV #For development mode
```

#### Database settings

You must setup database variables in the .env file in case of database connection

```bash   
    DB_HOST= #<for hostname>
    DB_NAME= #<for database name>
    DB_USER= #<for database user>
    DB_PASS= #<for database user's password>
```

## Running PyDaf

Simple run `./run.sh` on your prefered bash.

Examples:

```bash
    # Show commannds options
    ./run.sh --help 

    # Runs in container in production mode
    ./run.sh 

    # Runs in console in production mode
    ./run.sh --target=console

    # Runs in console in development mode
    ./run.sh --target=console --mode=dev 

    # Runs in container in production mode
    ./run.sh --target=container 

    # Runs in container in development mode
    ./run.sh --target=container --mode=dev 

    # Runs in container production mode and build container before run
    ./run.sh --target=container --build 
```

> **Note:** When run in target=console in production mode, you must set database settings on `prod.yml` or as environment variables.
