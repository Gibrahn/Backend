
from os import abort
from flask import Flask, request
import json
from mock_data import mock_catalog
from config import db
from bson import ObjectId
from flask import Flask, request, abort
from flask_cors import CORS

app = Flask('server')
CORS(app) # disable CORS policy

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

  
  if  not "title" in product or len(product["title"]) < 6:
    return abort(400, "Title must exist and should be longer than 5")

  if not "price" in product:
    return abort(400, "price is required")

  if type(product["price"]) != float and type(product["price"]) != int:
    return abort(400, "price must be a valid number")

  if product["price"] <= 0:
    return abort(400, "price must be greater than zero")

  if not "image" in product or len(product["category"]) < 1:
    return abort(400, "there needs to be an image")

  if not "category" in product:
    return abort(400, "there needs to be a category")  

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
    cursor = db.products.find({})
    total = 0

    for prod in cursor:
        total += prod["price"]

    return json.dumps(total) 

@app.route("/api/products/<id>")
def find_product(id):
    prod = db.products.find_one({"_id": ObjectId(id)})
    prod["_id"] = str(prod["_id"])

    if not ObjectId.is_valid(id):
      return abort(400, "id must be a valid object")

    return json.dumps(prod)
            
    

@app.route("/api/products/categories")
def get_categories():
    categories = []
    cursor = db.products.find({})

    for prod in cursor:
        cat = prod["category"]
        if cat not in categories:
            categories.append(cat)

    return json.dumps(categories)

@app.route("/api/products/categories/<cat_name>")
def get_by_category(cat_name):
    results = []
    cursor = db.products.find({"category": cat_name})

    for prod in cursor:
      prod["_id"] = str(prod["_id"])
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


##########################################
#############  Coupon Codes  #############
##########################################

#1 - get /api/couponCodes
@app.route("/api/couponCodes")
def get_coupon_codes():
    cursor = db.couponCodes.find({}) #get all 
    results = []

    for coupon in cursor:
      coupon["_id"] = str(coupon["_id"])
      results.append(coupon)


    return json.dumps(results)



#2 - get /api/couponCodes/<code>
@app.route("/api/couponCodes/<code>")
def get_coupon(code):
    coupon = db.couponCodes.find_one({"code": code})
    if not coupon:
      return abort(400, "error: code does not exist")

    coupon["_id"] = str(coupon["_id"])

    return json.dumps(coupon)



#3 - POST /api/couponCodes
@app.route("/api/couponCodes", methods=["post"])
def save_coupon():
  coupon = request.get_json()

  # validate that code exist and contains at least 5 chars
  if not "code" in coupon or len(coupon["code"]) < 5:
    return abort(400, "Code is required and should contain at least 5 chars")

  if not "discount" in coupon:  
    return abort(400, "Discount is required")
  
  if type(coupon["discount"]) != int and type(coupon["discount"]) != float:
    return abort(400, "Discount should be a valid number")

  if coupon ["discount"] < 0 or coupon ["discount"] > 31 :
    return abort(400, "Discount should be between 0 and 31")


  db.couponCodes.insert_one(coupon)
  coupon["_id"] = str(coupon["_id"])

  return json.dumps(coupon)




app.run(debug=True)