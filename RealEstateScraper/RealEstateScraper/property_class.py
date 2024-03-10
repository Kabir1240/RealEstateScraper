class Property:
    title = ""
    address = ""
    postcode = ""
    price = ""
    url = ""
    image = ""

    def __init__(self, title, address, postcode, price, url, image):
        self.title = title
        self.address = address
        self.postcode = postcode
        self.price = price
        self.url = url
        self.image = image
