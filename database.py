#this file gonna have all the connection strings for our application to connect with mysql

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base     #ye 3 sb databse.py file in projects me honge

URL_DATABASE = "mysql+pymysql://root:Mohit7soni%40@localhost:3306/fastapimysql"  #connection string   -->YAHA AAPKE MYSQL KA URL FOR CONNECTION

engine = create_engine(URL_DATABASE, echo=True)   #ye engine banayega connection ke liye

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  #ye session banayega database ke sath interact karne ke liye -->ye bhi sbme same

Base = declarative_base()