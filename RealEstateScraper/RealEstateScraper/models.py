from RealEstateScraper import db


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(20), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)
    price = db.Column(db.String(10), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    image_uri = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Property('{self.title}', '{self.address}', '{self.postcode}', '{self.price}', '{self.url}', " \
               f"'{self.image_uri}')"
