from api import app , ma , db
from flask import render_template,request , jsonify , flash, redirect , url_for , request
from .models import Product
import uuid
from .forms import MyForm

class ProductSchema(ma.Schema):

    class Meta:
        model = Product
        fields = ('public_id' ,  'name' , 'price' , 'quantity')

#init_schema
product_schema = ProductSchema(strict=True) 
products_schema = ProductSchema(many=True , strict=True)

#create a product

@app.route('/product' , methods=['POST'])
def add_products():
    data = request.get_json() #get typed json

    new_product = Product(public_id= str(uuid.uuid4()) ,
    name=data['name'] ,
     price=data['price'] , 
     quantity=data['quantity']) #public id bee the id to show to public

    db.session.add(new_product)
    db.session.commit()

    # return jsonify({'message':"new user has been created"})
    #or
    return product_schema.dump(new_product) #show new product after posting


#get all products
@app.route('/' , methods=['GET'])
def get_all_products():
    products = Product.query.all()
    result = products_schema.dump(products)
    return jsonify({'products':result.data})


#get single product
@app.route('/<public_id>' , methods=['GET'])
def get_single_product(public_id):
    product = Product.query.filter_by(public_id=public_id).first()
    one_product = product_schema.dump(product)
    return jsonify({'product':one_product.data})

#update product
@app.route('/<public_id>' , methods=['PUT'])
def update_product(public_id):
    product = Product.query.filter_by(public_id=public_id).first()
    data = request.get_json()
    product.name = data['name']
    product.price = data['price']
    product.quantity = data['quantity']
    
    db.session.commit() #save
    return jsonify({'messsage':'Product has been changed'})


#delete product
@app.route('/<public_id>' , methods=['DELETE'])
def delete_product(public_id):
    product = Product.query.filter_by(public_id=public_id).first()
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message":f"Product {product.name} has been deleted"})


#products route
@app.route('/products' , methods=['GET'])
def products():
    products = Product.query.all()
    return render_template('product_list.htm' , products=products)


#add product form
@app.route('/add_product' , methods=['GET' , 'POST'])
def add_product():
    form = MyForm()
    if form.validate_on_submit():
        public_id = str(uuid.uuid4())
        name = form.name.data 
        price= form.price.data
        quantity = form.quantity.data 
        new_product = Product(public_id=public_id , name=name , price=price , quantity=quantity)
        db.session.add(new_product)
        db.session.commit()      
        flash('New product has been added!')
        return redirect(url_for('products'))  
    return render_template('add_product.htm' , form=form)


#product detail
@app.route('/product/<public_id>' , methods=['GET'])
def product_detail(public_id):
    product = Product.query.filter_by(public_id=public_id).first()
    return render_template('product_detail.htm' , product=product)

#update product
@app.route('/update_product/<public_id>' , methods=['GET', 'POST'])
def product_edit(public_id):
    product = Product.query.filter_by(public_id=public_id).first()
    form= MyForm()
    form.name.data = product.name
    form.price.data = product.price
    form.quantity.data = product.quantity
    if form.validate_on_submit():
        product.name =form.name.data 
        product.price = form.price.data
        product.quantity = form.quantity.data
        form.edited.data = True       
        db.session.commit()
        flash('Product has been updated')
        return redirect(url_for('product_detail' , public_id=product.public_id))
    return render_template('product_edit.htm' , form=form,product=product)


#delete product
@app.route('/delete_product/<public_id>' , methods=['GET' , 'POST'])
def product_delete(public_id):
    product = Product.query.filter_by(public_id=public_id).first()
    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        flash(f'{product.name} has been deleted')
        return redirect(url_for('products'))
    return render_template('delete_product.htm' , product=product)

