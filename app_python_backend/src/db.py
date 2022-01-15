from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, exc
from sqlalchemy import create_engine, Float
from sqlalchemy.exc import OperationalError

from conf import CONF
from logger import logger
import ssl
import os

class DATABASE_CONNECTION:

    engine_url  = None
    engine      = None
    con         = None
    db_session  = None
    status_ok   = None

    def __init__(self):
        self._create_db_engine()

    def _create_db_engine(self):
        engine_url = "mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8".format(
            username=CONF.DATABASE_USERNAME,
            password=CONF.DATABASE_PASSWORD,
            host=CONF.DATABASE_HOST,
            port=CONF.DATABASE_PORT,
            database=CONF.DATABASE_SCHEMA
        )

        ssl_conf = None
        
        #if CONF.DATABASE_SSL_MODE == "SSL":
        #    logger.debug("Connecting database using SSL")
        #    ssl_conf = {'ssl_ca': os.path.dirname(os.path.abspath(__file__))+F"/{CONF.DATABASE_CA}",'ssl_verify_cert':True,'ssl_disabled': False,'ssl_verify_identity':False }
        #else:
        ssl_conf = None
        
        db_echo = False
        logger.debug("------ SSL CONF ------\n{}".format(ssl_conf))

        logger.debug("Database connection echo:{}".format(db_echo))
        if ssl_conf:
            self.engine = create_engine(engine_url, connect_args=ssl_conf, echo=db_echo)
            logger.debug("Database connection using SSL: {}".format(ssl_conf))
            self._test_database_connection()
        else:
            self.engine = create_engine(engine_url, echo=db_echo)
            logger.debug("Database connection not using SSL")
            self._test_database_connection()

    def _test_database_connection(self):

        if self.engine:
            try:
                self.con = self.engine.connect()
                logger.info("Database connection to {} succesfull".format(CONF.DATABASE_HOST))
                self.status_ok = True

            except OperationalError as e:
                logger.error("Connection to {} on {} failed. {}".format(CONF.DATABASE_SCHEMA, CONF.DATABASE_HOST,e))
                #sys.exit("Database connection failed!")
                self.status_ok = False
                return False

            except ssl.CertificateError as cert_error:
                logger.error("SSL Cert error {}".format(cert_error))
            
            #Close connection test
            self.con.close()

            return True
        else:
            self.status_ok = False
            return False
    
    def dispose_engine(self):

        logger.debug("Disposing database engine")

        if self.engine:
            # Dispose engine
            self.engine.dispose()
            self.engine = None

            return True
        else:
            return False
    
    def init_session(self):
        logger.debug("Database engine: {}".format(self.engine))

        if self.db_session:
            logger.debug("Database session already exists. {}".format(self.db_session))
            return

        if self.engine:
            pass
        else:
            logger.debug("DB engine not found. Creating engine")
            self._create_db_engine()
        
        Session = sessionmaker(bind=self.engine)
        self.db_session = Session()
    
    def close_session(self):

        logger.debug("Closing database session")
        self.db_session.close()
        self.db_session = None

        return True