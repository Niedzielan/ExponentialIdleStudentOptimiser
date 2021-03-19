from flask import Flask, request
from flask_swagger_ui import get_swaggerui_blueprint
import StudentOptimiser
import json

app = Flask(__name__)
# Add swagger to the API
swagger_url = '/swagger'
api_url = '/static/swagger3.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    swagger_url,
    api_url,
    config={
        'app-name': "Student Optimiser"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix = swagger_url)

@app.route("/OptimiseStudents", methods = ['POST'])
def OptimiseStudents():
    response = StudentOptimiser.calcJSON(json.dumps(request.get_json()))
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)