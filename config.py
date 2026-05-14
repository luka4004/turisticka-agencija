import os

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/turisticka_agencija"
    SQLALCHEMY_TRACK_MODIFICATIONS = False