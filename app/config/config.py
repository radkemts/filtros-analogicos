class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    HOST = '0.0.0.0'

class ProductionConfig(Config):
    DEBUG = False
    HOST = None
