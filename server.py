


from flask import Flask, request
import json
from mock_data import mock_catalog
from config import db

app = Flask('server')

@app.route("/home")
def home():
    return "Hello there!!"

#####################################################################
########################## API CATALOG ##############################
#####################################################################


@app.route("/api/about", methods=["POST"])
def about():
    me = {
        "first": "Gibrahn",
        "last": "Duarte"
    }

    return json.dumps(me) # parse into json, then return


@app.route("/api/catalog")
def get_catalog():
    cursor = db.products.find({}) #get all 
    all_products = []

    for prod in cursor:
      prod["_id"] = str(prod["_id"])
      all_products.append(prod)


    return json.dumps(all_products)


@app.route("/api/catalog", methods=["post"])
def save_product():
  product = request.get_json()
  db.products.insert_one(product)

  print ("Product Saved")
  print(product)

  #fix the _id issue
  product["_id"] = str(product["_id"])

  return json.dumps(product)




@app.route("/api/catalog/cheapest")
def get_cheapest():
    cursor = db.products.find({})
    cheapest = cursor[0]

    for prod in cursor:
        if (prod["price"] < cheapest["price"]):
            cheapest = prod 

    cheapest["_id"] = str(cheapest["_id"])
    return json.dumps(cheapest)

@app.route("/api/catalog/total")
def get_total():
    total = 0

    for prod in mock_catalog:
        total += prod["price"]

    return json.dumps(total) 

@app.route("/api/products/<id>")
def find_product(id):
    for prod in mock_catalog:
        if  prod["_id"] == id:
            
            return json.dumps(prod)

@app.route("/api/products/categories")
def get_categories():
    categories = []

    for prod in mock_catalog:
        cat = prod["category"]
        if not cat in categories:
            categories.append(cat)

    return json.dumps(categories)

@app.route("/api/products/categories/<cat_name>")
def get_by_category(cat_name):
    results = []

    for prod in mock_catalog:
        if  prod["category"].lower() == cat_name.lower():
            results.append(prod)
    return json.dumps(results)

@app.route("/api/products/search/<text>")
def search_by_text(text):
    results = []
    text = text.lower()

    for prod in mock_catalog:
        title = prod["title"].lower()
        if text in title:
            results.append(prod)

    return json.dumps(results)

#start the server
app.run(debug=True)