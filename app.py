from flask import Flask
from dotenv import load_dotenv
from neo4j import GraphDatabase
import os

load_dotenv()

app = Flask(__name__)

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(uri, auth=(username, password))

# Import routes
from routes import *

if __name__ == '__main__':
    app.run(debug=True)








# import os
# from flask import Flask, jsonify
# from werkzeug.exceptions import HTTPException as WerkzeugHTTPException
# from webargs import fields, validate
# from webargs.flaskparser import FlaskParser
# from neo4j import GraphDatabase
# from dotenv import load_dotenv
# from neo4j.exceptions import ClientError
# from datetime import datetime

# load_dotenv()

# app = Flask(__name__)



# parser = CustomFlaskParser()


# uri = os.getenv("NEO4J_URI")
# username = os.getenv("NEO4J_USERNAME")
# password = os.getenv("NEO4J_PASSWORD")
# driver = GraphDatabase.driver(uri, auth=(username, password))




# if __name__ == '__main__':
#     app.run(debug=True)
