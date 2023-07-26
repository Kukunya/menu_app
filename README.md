==================================== APP DESCRIPTION ====================================

A simple application for food establishments that is based on PostgreSQL and FastAPI.  
Works with menu units, submenus and dishes that are entered into the database. They will allow you to add elements, delete, update, and provide information about them using the appropriate rest api requests.  

ASGI-server uviconr is used to test the application.  

======================================== RUN APP ========================================

For correct operation, you need:
    PostgreSQL 14.2, compiled by Visual C++ build 1914, 64-bit,
    Python 3.9

The necessary dependencies are specified in "/requirements.txt".

====================================

To get started, from the root of the application install dependencies:
    >pip install -r requirements.txt

====================================

Define database parameters:

1 OPTION
You can set the parameters directly in the "/menu_app/conf.py" file (not recommended for security reasons)
------------------------------------
2 OPTION
To create a virtual environment variable specify variable values according to your database settings.  
    for windows:  
        >set sql_host=<host-ip>
        >set sql_port=<host-port>
        >set sql_user=<database user>
        >set sql_pass=<database password>
        >set database=<database name>
------------------------------------
3 OPTION
If multiple uses of the script are planned, then you should add variables to the file "Activate.bat" and to "Deactivate.bat" file should be specified without the values of variables (example ">set sql_host="). Restart venv.

====================================

From the root of the application, run ASGI-server uvicorn:
    >uvicorn menu_app.main:app

====================================== API METHODS ======================================

Api methods and parameters used can be found in the "/menu_app/main.py" file, a description of all methods and parameters will be added with updates.