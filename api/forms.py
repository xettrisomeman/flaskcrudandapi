from flask_wtf import FlaskForm
from wtforms import StringField , IntegerField , BooleanField
from wtforms.validators import DataRequired , ValidationError
from .models import Product



class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(message="Name should not be empty")])
    price = IntegerField('price' , validators=[DataRequired(message='Price is required')])
    quantity = IntegerField('quantity' , validators = [DataRequired(message='Quantity is required')])
    edited = BooleanField()


    def validate_name(self,field):
        name = Product.query.filter_by(name=field.data.lower()).first()
        if name and not self.edited:
            raise ValidationError('Name already exists')
        return name
    

