from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


# Apis work with resources where each resource is a class

class Student(Resource):
    def get(self, name):
        return {'student': name}

api.add_resource(Student, '/student/<string:name>') # http://localhost/student/rolf

app.run(port=5000)