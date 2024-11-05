from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),   
 nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)   

    # Add other fields as needed (e.g., image_url, quantity_in_stock)