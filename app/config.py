'''
    The BaseSettings of pydantic module is used to check for all the environment variables 
    are present and in their required form i.e like int,str,etc
    When our application is in production , then every time cross checking whether all environment variables are present becomes very difficult and any error can crash the application
    
    We just need to pass all the environment variables , their datatype and if possible provide the default value into the class <user_defined_name> that extends the BaseSettings of pydantic module


    We have defined all the environment variables in .env file when we are in development, on the other case when we are in production environment we have to save them in system environment variables

    class Config:
        env_file = ".env"   ----> this is used to fetch the environment variables from .env file
                          

'''

from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname : str
    database_port : str
    database_password : str
    database_name : str
    database_username : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int

    class Config:
        env_file = ".env"

settings = Settings()