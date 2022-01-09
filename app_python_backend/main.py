from flask import Flask,request,redirect
from flask_restful import Api, Resource,reqparse
import dateutil.parser

from conf                       import CONF
from logger                     import logger
from db                         import DATABASE_CONNECTION
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm             import exc
from sqlalchemy                 import Column, String, DateTime, Float,Integer,func

import pandas

import os

from os.path import isfile, join,abspath
from os import listdir

from werkzeug.datastructures import FileStorage
import werkzeug

app = Flask(__name__)
api = Api(app)


Base = declarative_base()

# jira_sla_issues table definition
class sensorMetrics(Base):

    __tablename__               = "metrics"    
    row_id                      = Column("id", Integer, primary_key=True)
    location                    = Column("location")
    datetime                    = Column("datetime", DateTime)
    sensorType                  = Column("sensorType", String)
    value                       = Column("value",Float)
    fetchdate                   = Column("fetchdate", DateTime, default=func.utc_timestamp(), onupdate=func.utc_timestamp())

# Test database connection
db_conn = DATABASE_CONNECTION()
db_conn.dispose_engine()
del db_conn


def ValidateData(row):

    # check location
    if row['location']:
        if not isinstance(row['location'],str):
            row['location'] = None

    # validate sensors
    if row['sensorType']:
        if row['sensorType'] not in ['rainFall','temperature','pH']:
            return None



    #check datetime
    if row['datetime']:
        if not isinstance(row['datetime'],str):
            row['datetime'] = None

    #check other values
    if row['value']:
        if not isinstance(row['value'],float):
            row['value'] = None
        
        # validate value rules
        else:
            if row['sensorType'] == 'rainFall' and row['value'] >= 0 and row['value'] <=500:
                pass
            if row['sensorType'] == 'temperature' and row['value'] >= -50 and row['value'] <=100:
                pass
            if row['sensorType'] == 'pH' and row['value'] >= 0 and row['value'] <=14:
                pass
            else:
                return None

    DBRow = {
                    "location": row['location'],
                    "datetime": dateutil.parser.isoparse(row['datetime'])  if row['datetime'] else None,
                    "sensorType": row['sensorType'],
                    "value": row['value'] if isinstance( row['value'], float) else None
                }

    return DBRow






# Check if there source files to DB
def writeRecordsToDB(session, table):


    files  = [f for f in listdir(CONF.CSV_INPUT) if isfile(join(CONF.CSV_INPUT, f))]
    for i in files:
        print(i)


        with open(os.path.abspath(f"{CONF.CSV_INPUT}/{i}"), mode='r') as csv_file:
            csv_reader = pandas.read_csv(csv_file)
            
            commit_counter = 0

            for row in csv_reader.to_dict(orient="records"):
                # create object to match DB object
                DBRow = ValidateData(row=row)
                
                # skip unvalid rows
                if not DBRow:
                    continue
                

                # Form sqlalchemy object
                DBObject = table(
                    **DBRow
                )
                
                session.add(DBObject)
                
                
                if commit_counter == 300:
                    logger.debug("Database commit")
                    session.commit()
                    commit_counter = 0
                
                commit_counter += 1
            
            # Final database commit
            session.commit()




    
class Locations(Resource):
    def get(self):

        parser = reqparse.RequestParser()  # initialize
        # Database connection and table reflection
        db_conn = DATABASE_CONNECTION()

        # Check database connection status and return 500 connection failed
        if not db_conn.status_ok:
            logger.error("Database connection failed. Exit")


        Base.metadata.create_all(db_conn.engine)

        db_conn.init_session()
        _table = sensorMetrics   

        if not db_conn.status_ok:
            logger.error("Database connection failed.")


        last_modification = db_conn.db_session.query(_table)

        for i in last_modification:
            print(i.row_id,i.location)

        return


class ImportFiles(Resource):
    def get(self):

        db_conn = DATABASE_CONNECTION()

        # Check database connection status and return 500 connection failed
        if not db_conn.status_ok:
            logger.error("Database connection failed. Exit")


        Base.metadata.create_all(db_conn.engine)

        db_conn.init_session()
        
        writeRecordsToDB(session=db_conn.db_session, table=sensorMetrics)
        
   
        return {'data': 'asd'}, 200  # return data and 200 OK code

class FileStorageArgument(reqparse.Argument):
    """This argument class for flask-restful will be used in
    all cases where file uploads need to be handled."""
    
    def convert(self, value, op):
        if self.type is FileStorage:  # only in the case of files
            # this is done as self.type(value) makes the name attribute of the
            # FileStorage object same as argument name and value is a FileStorage
            # object itself anyways
            return value

        # called so that this argument class will also be useful in
        # cases when argument type is not a file.
        super(FileStorageArgument, self).convert(*args, **kwargs)


# for some reason the resfull wont work with posting files.. have to test again
class ForBetaAndUpload(Resource):

   def post(self):
    parse = reqparse.RequestParser()
    print(parse)
    print(parse.__dict__)
    test = parse.add_argument('file', type = werkzeug.datastructures.FileStorage, location = 'file')
    print(test)
    args = parse.parse_args()
    print(args)
    image_file = args['file']
    image_file.save("your_file_name.jpg")
        

api.add_resource(ForBetaAndUpload, '/upload')

# create endpoints
api.add_resource(Locations, '/locations')
api.add_resource(ImportFiles, '/import')









if __name__ == '__main__':
    app.run()  # run our Flask app
