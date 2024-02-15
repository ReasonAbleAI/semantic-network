from flask import jsonify
from werkzeug.exceptions import HTTPException as WerkzeugHTTPException
from webargs.flaskparser import FlaskParser

class CustomFlaskParser(FlaskParser):
    def handle_error(self, error, req, schema, *, error_status_code, error_headers):
        message = error.messages
        status_code = error_status_code or 400
        response = jsonify({"error": message})
        response.status_code = status_code
        raise WerkzeugHTTPException(response=response)
