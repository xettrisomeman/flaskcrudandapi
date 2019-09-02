from api import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50) , unique=True)
    name = db.Column(db.String(66))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return f'<Product {self.name} >'


