import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "jfdbiukrtidfj gsdckgsd;skbu"
    ENV = 'dev'