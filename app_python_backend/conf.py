import os

class CONF:

    DATABASE_USERNAME       =   os.getenv("DATABASE_USERNAME")
    DATABASE_PASSWORD       =   os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST           =   os.getenv("DATABASE_HOST")
    DATABASE_PORT           =   os.getenv("DATABASE_PORT", "3306")
    DATABASE_SCHEMA         =   os.getenv("DATABASE_SCHEMA")
    CSV_INPUT               =   os.getenv("CSV_INPUT", "input")

    APP_NAME                =   os.getenv("APP_NAME")
    LOGGING_LEVEL           =   os.getenv("LOGGING_LEVEL", "INFO")
    METRICS_TABLE           =   os.getenv("METRICS_TABLE", "metrics")