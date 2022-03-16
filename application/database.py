from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        
        
        
#       Another way of managing database
#from fastapi.params import Body
#from random import randint
#from pydantic.schema import field_schema
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time


#while True:
#    try:
#        connection = psycopg2.connect(host="localhost", database="fastapi", user="postgres",password="postgresql")
#        cursor = connection.cursor()
#        print("Succesful connection!")
#        break
#    
#    except Exception as e:    
#        print("Failed to connect!")
#        print("[ERROR]: ",e)
#        time.sleep(3)


# def get_post(id: int):
    #cursor.execute(f"""SELECT * FROM posts WHERE id = {id}""")
    #response = cursor.fetchone()
    #return response

#my_posts = [{"title":"title-1", "content":"content-1", "id":1}, {"title":"title-2", "content":"content-2", "id":2}]
