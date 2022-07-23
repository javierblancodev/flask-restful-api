from email import message
from flask import Flask, request
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
        # for item in items:
        #     if item["name"] == name:
        #         return item
        # A cleaner way to do exactly the same as above is to use the filter function
        # Its first parameter may take a lambda function that defines the condition, the second parameter is the iterable
        # The filter function return a filter object that can been converted into a list 
        item = list(filter(lambda x: x['name'] == name, items))
        # But also into a single item with the next function, which will return the first item that meet the condition
        # We can chain multiple next functions as many time as we want to get the second item, third or the like 
        item = next(filter(lambda x: x['name'] == name, items), None)
        # Next will raise an error if there is not item that meet the given condition. The sencond argument None prevent it, simply returning None
        return {"item": item}, 200 if item else 404 # This is the ternary operator in Python

    def post(self, name):

        if next(filter(lambda x: x['name'] == name, items)) is not None:
            return {message: "An item with name {} already exists".format(name)}, 400

        # request, which must be imported, is a variable that contains the request from the client
        # its get_json method will bring us the request payload/body in json 
        # if the header or body is not of json type, we will enconter an error
        # To prevent it, we use force=True so that the body is formatted anyway regarless of the Content-Type in the header
        # data = request.get_json(force=True) This may be dangerous, since if things are not done rigth it will keep going anyway
        # Better to use silence=True which will simply return None in case there is an error
        data = request.get_json(silent=True)
        item = {"name": name, "price": data['price']}
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