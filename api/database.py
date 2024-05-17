from sqlalchemy import create_engine, MetaData, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import datetime

# Conexão com o banco de dados
engine = create_engine("mysql+pymysql://admin:admin@database:3306/banco", pool_pre_ping=True, pool_recycle=3600)
metadata = MetaData()
Base = declarative_base()

# Table de usuários
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))

# Tabela de pedidos
class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    email = Column(String(50))
    description = Column(String(255))

# Criação do banco de dados
metadata.create_all(bind=engine, tables=[Orders.__table__, Users.__table__])

# Sessão do banco de dados
session = Session(bind=engine)

# Sessão do banco de dados
conn = engine.connect()