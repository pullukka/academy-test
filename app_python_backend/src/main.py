from ast import expr_context
from cmath import exp
import imp
from flask import Flask,jsonify
from flask_restful import Api, Resource,reqparse
import dateutil.parser

from conf                       import CONF
from logger                     import logger
from db                         import DATABASE_CONNECTION
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm             import exc
from sqlalchemy                 import Column, String, DateTime, Float,Integer,func
#import pandas

import os
import werkzeug
from werkzeug.utils             import secure_filename

app = Flask(__name__)
api = Api(app)

# allowed files to upload
app.config["ALLOWED_EXTENSIONS"] = ["csv"]

# allowd file size (16megabytes) .. move this to front
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


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


def ValidateFileType(file):
    
    # We only want files with a . in the filename
    if not "." in file:
        return False

    # Split the extension from the filename
    extension = file.rsplit(".", 1)[1]

    # Check if the extension is in MAX_CONTENT_LENGTH
    if extension.lower() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False

# validata
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
        
        # changed this when removed pandas
        try:
            row['value'] = float(row['value'])
        except:
            row['value'] = None
        
        #if not isinstance(row['value'],float):
        #    row['value'] = None
        
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
    # create object for db
    DBRow = {
            "location": row['location'],
            "datetime": dateutil.parser.isoparse(row['datetime'])  if row['datetime'] else None,
            "sensorType": row['sensorType'],
            "value": row['value'] if isinstance( row['value'], float) else None
            }

    return DBRow





import csv
# Check if there source files to DB
def writeRecordsToDB(session, table, file):

    if file:
        #with open(os.path.abspath(f"{file}"), mode='r') as csv_file:
                #csv_reader = pandas.read_csv(csv_file)
                
        commit_counter = 0
        rowsAdded = 0
        
        with open(os.path.abspath(f"./input/{file}"), mode='r') as f:
            reader = csv.DictReader(f)
            a = list(reader)
            

            

        for row in a:
        #for row in csv_reader.to_dict(orient="records"):
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
            rowsAdded += 1
            
            # add try expect
            if commit_counter == 300:
                logger.debug("Database commit")
                session.commit()
                commit_counter = 0
            
            commit_counter += 1
        
        # Final database commit
        session.commit()
        session.close()
        return rowsAdded

  

    
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


        last_modification = db_conn.db_session.query(_table).all()

        for i in last_modification:
            print(i.row_id,i.location)

        return jsonify(last_modification), 201





class UploadCSV(Resource):
   def post(self):
    parse = reqparse.RequestParser()
    parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
    args = parse.parse_args()
    csv_file = args['file']
    
    # newer trust input
    filename = secure_filename(csv_file.filename)
    
    # store to disk, check if doable in memory 
    csv_file.save(f"./input/{filename}")

    response = {'rowsToDB': None , 'message':None}
    
    # upload file if have one
    if filename and ValidateFileType(file=filename):
        db_conn = DATABASE_CONNECTION()

        # Check database connection status
        if not db_conn.status_ok:
            logger.error("Database connection failed. Exit")

        Base.metadata.create_all(db_conn.engine)
        db_conn.init_session()
        
        # write valid rows to DB
        writeResults = writeRecordsToDB(session=db_conn.db_session, table=sensorMetrics, file=filename)
        
        response['rowsToDB'] = writeResults
        response['message'] = 'Ok'
        response = jsonify(response)
        
        response.headers.add('Access-Control-Allow-Origin', '*')
        #print(response.headers)
        if db_conn.db_session:
            db_conn.db_session.close()

        logger.debug(response.data)
        
        # remove file from disk
        if os.path.exists(F"./input/{filename}"):
            os.remove(F"./input/{filename}")
            logger.debug(F"file {filename} removed")
        
        return response
    
    else:
        response = jsonify({'message': 'File not valid csv' })
        response.headers.add('Access-Control-Allow-Origin', '*')
        logger.debug(response.data)
        return response
    
    

        



# create endpoints
api.add_resource(Locations, '/locations')

api.add_resource(UploadCSV, '/upload')







if __name__ == '__main__':
    app.run()  # run our Flask app
