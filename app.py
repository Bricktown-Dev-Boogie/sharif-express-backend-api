from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from flask_cors import CORS 
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Init CORS
CORS(app)
 
 # Item Model   
class Item(db.Model):
    __tablename__='item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    imgUrl = db.Column(db.String)
    productKey = db.Column(db.Integer, db.ForeignKey('product.id'))
    
    def __init__(self, name, price, imgUrl, productKey):
      self.name = name 
      self.price = price
      self.imgUrl = imgUrl  
      self.productKey = productKey


# Item Schema
class ItemSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'price', 'imgUrl', 'productKey')
 
# Init Item Schema
Item_schema = ItemSchema()
Items_schema = ItemSchema(many=True)

# Product Model
class Product(db.Model):
  __tablename__ = 'product'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  title = db.Column(db.String(200))
  routeName = db.Column(db.String(200))
  items = db.relationship("Item", backref="product")
  
  def __init__(self, name, title, routeName):
    self.name = name
    self.title = title
    self.routeName = routeName
    
    
# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'title', 'routeName', 'items')
  items = ma.Nested(Items_schema)
  
 
 
# Init Product Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Get Single Product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return product_schema.jsonify(product)

# Get All Products
@app.route('/product', methods=['GET'])
def get_products():
  all_products = Product.query.all()
  return jsonify(products_schema.dump(all_products))

# Create a Product
@app.route('/product', methods=['POST'])
def add_product():
  name = request.json['name']
  title = request.json['title']
  routeName = request.json['routeName']
  items = request.json['items']
  
  new_product =[]

  new_product = Product(name, title, routeName)

  db.session.add(new_product)
  db.session.commit()

  for item in items:
        name = item['name']
        price = item['price']
        imgUrl = item['imgUrl']
        
        new_item = Item(name, price, imgUrl, new_product.id)
        db.session.add(new_item)
        db.session.commit()

  return jsonify(product_schema.dump(new_product))

# Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)

  name = request.json['name']
  title = request.json['title']
  routeName = request.json['routeName']
  items = request.json['items']

  product.name = name
  product.title = title
  product.routeName = routeName
  product.items = items
  
  for item in items:
        
        product.name = name
        product.price = price
        product.imgUrl = imgUrl
        
        db.session.commit()

  return product_schema.jsonify(product)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)