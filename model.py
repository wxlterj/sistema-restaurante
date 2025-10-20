class Client:
    def __init__(self, id, name, type, n_order, order=[]):
        self.id = id
        self.name = name
        self.type = type
        self.n_order = n_order
        self.order = order

class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price
        self.img_path = f"./assets/{id}.png"