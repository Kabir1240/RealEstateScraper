from RealEstateScraper.models import Property
from RealEstateScraper import db


def setup_database(properties):
    db.drop_all()
    db.create_all()
    for prop in properties:
        add_data = Property(title=prop.title, address=prop.address, postcode=prop.postcode,
                            price=prop.price, url=prop.url, image_uri=prop.image)
        db.session.add(add_data)
    db.session.commit()
    