class Person:

    def __init__(self, name, email, photo_link, po_num, place):
        self.name = name
        self.email = email
        self.photo_link = photo_link
        self.po_num = po_num
        self.place = place

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_photo_link(self):
        return self.photo_link

    def get_po_num(self):
        return self.po_num

    def get_place(self):
        return self.place

    name = property(get_name)
