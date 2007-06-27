
import db.base

class Category(db.base.Object):
    def __init__(self, id = -1):
        super(Category, self).__init__(id)        
        self._name = ''
    
