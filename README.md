## APP DESCRIPTION ##

A simple application for food establishments that is based on PostgreSQL and FastAPI.
Works with menu units, submenus and dishes that are entered into the database. They will allow you to add elements, delete, update, and provide information about them using the appropriate rest api requests.

ASGI-server uviconr is used to test the application.

## RUN APP ##
### WITH DOCKER ###
Download the [docker-compose](https://github.com/Kukunya/menu_app/blob/master/docker-compose/docker-compose.yaml) file and the [environment variables](https://github.com/Kukunya/menu_app/blob/master/docker-compose/env.env) file from the directory to a place convenient for you.

Navigate to the folder where you downloaded the files and run the following commands.
1. To start the uvicorn server daemon with postgresql:

>\>docker-compose up -d

2. To test the API of the application:

>\>docker run --rm --network host kukunya94/menu_app_tests:latest

**Please note that if you abort the test, then subsequent tests will fail, since there is no database cleanup mechanism provided.**

### MANUALLY ###

#### For correct operation, you need: ####
    PostgreSQL 14.2, compiled by Visual C++ build 1914, 64-bit
    Python 3.9

The necessary dependencies are specified in "/requirements.txt".



#### To get started, from the root of the application install dependencies: ####  
>\>pip install -r requirements.txt



#### Define database parameters: ####

###### 1 OPTION ######
You can set the parameters directly in the "/menu_app/conf.py" file (not recommended for security reasons)

###### 2 OPTION ######
To create a virtual environment variable specify variable values according to your database settings.  

*For windows:*  

>\>set sql_host=\<you host-ip>  
>\>set sql_port=\<you host-port>  
>\>set sql_user=\<you database user>  
>\>set sql_pass=\<you database password>  
>\>set database=\<you database name>

###### 3 OPTION ######
If multiple uses of the script are planned, then you should add variables from [2 OPTION](/#2-option) to the file "Activate.bat" and to "Deactivate.bat" file should be specified without the values of variables.  

*For windows:* 
  
>\>set sql_host=  
>\>set sql_port=  
>\>set sql_user=  
>\>set sql_pass=  
>\>set database=

Then restart venv.



#### From the root of the application, run ASGI-server uvicorn: ####  
>\>uvicorn menu_app.main:app

## API METHODS ##

Before deploying the server, familiarize yourself with the api methods and parameters: http://localhost:8000/docs#/
