from distutils.log import debug
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

# Apis work with resources where each resource is a class
# We no longer need to use jsonify when working with flask_restful because this library features will do it for us

# Resource is a class itself (it comes with some methods like get, post, etc.) that can be extended so we can create our own resource
class Item(Resource):
    # The name parameter refer/comes directly to/from the slug in the url
    def get(self, name):
        for item in items:
            if item["name"] == name:
                return item
        return {"message": "Sorry, no matching item has been found"}, 404

    def post(self, name):
        item = {"name": name, "price": 12.99}
        items.append(item)
        return item, 201

class ItemsList(Resource):
    def get(self):
        return {'items': items}

# Add the Item resource to our app 
# The add_resource method from the API object will take two arguments: the resource and the url
api.add_resource(Item, '/item/<string:name>') # http://localhost/item/chair
api.add_resource(ItemsList, '/items')

app.run(port=5000, debug=True) # Debug will return a nice error message in case that the program enconter any