from objs import objlist

class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
class Animal(object):
    def __init__(self, name, legs):
        self.name = name
        self.legs = legs
        self._id = 0
        
class TestObjList(object):

    #---------------------------------------------------------------------------
    def test_types(self):
        ol = objlist.ObjList(class_name = Person)
        
        ol.append(Person('jorgen', 35))
        ol.append(Person('dewey', 1))       
        
        try:
            ol.append('Test')
            assert False
        except objlist.ObjListException:
            pass

        try:
            ol.append(1)
            assert False
        except objlist.ObjListException:
            pass

        try:
            ol.append(Animal('fly', 6))
            assert False
        except objlist.ObjListException:
            pass

    #---------------------------------------------------------------------------
    def test_add(self):
        ol = objlist.ObjList(class_name = Person)
        
        ol.append(Person('jorgen', 35))
        ol.append(Person('dewey', 1))       

        assert ol.count() == 2

        ol = objlist.ObjList(class_name = Animal)
        
        ol.append(Animal('bird', 2))
        ol.append(Animal('fly', 6))       
        
        assert ol.count() == 2
        
    #---------------------------------------------------------------------------
    def test_delete(self):
        ol = objlist.ObjList(class_name = Person)
        
        p = Person('jorgen', 35)
        ol.append(p)
        pp = Person('dewey', 1)
        ol.append(pp)       

        assert ol.count() == 2

        ol.remove(p)
        assert ol.count() == 1
            
        ol.remove(pp)
        assert ol.count() == 0

    #---------------------------------------------------------------------------
    def test_clear(self):
        ol = objlist.ObjList(class_name = Person)
        
        ol.append(Person('jorgen', 35))
        ol.append(Person('dewey', 1))       

        assert ol.count() == 2
        
        ol.clear()
        
        assert ol.count() == 0

    #---------------------------------------------------------------------------
    def test_unmanaged(self):
        ol = objlist.ObjList(class_name = Person)
        
        p = Person('jorgen', 35)
        ol.append(p)
        ol.append(Person('dewey', 1))       
        
        ulist = ol.unmanaged_list()
        ulist.remove(p)
        
        assert len(ulist) == 1
        assert ol.count() == 2
        
    #---------------------------------------------------------------------------
    def test_iterator(self):
        items = [ ('fly', 6), 
                  ('fish', 0),
                  ('dog', 4),
                  ('human', 2),
                  ('chimp', 2),
                  ('bird', 2) ]
        
        ol = objlist.ObjList(class_name = Animal)
        for name, legs in items:
            ol.append(Animal(name, legs))
            
        idx = 0
        for i in ol:
            tup = items[idx]
            assert i.name == tup[0]
            assert i.legs == tup[1]
            idx += 1 
        
        assert idx == 6
        assert ol.count() == 6
        
    #---------------------------------------------------------------------------
    def test_find_id(self):
        items = [ ('fly', 6, 1), 
                  ('fish', 0, 2),
                  ('dog', 4, 3),
                  ('human', 2, 7),
                  ('chimp', 2, 10),
                  ('bird', 2, 20) ]
        
        ol = objlist.ObjList(class_name = Animal)
        for name, legs, id in items:
            a = Animal(name, legs)
            ol.append(a)
            a._id = id
                    
        assert ol.count() == 6
        
        o = ol.find_id(7)
        assert o <> None
        assert o.name == 'human'
        assert o._id == 7
        
        o = ol.find_id(20)
        assert o <> None
        assert o.name == 'bird'
        assert o._id == 20

        o = ol.find_id(128)
        assert o == None

        o = ol.find_id(1)
        assert o <> None
        assert o.name == 'fly'
        assert o._id == 1

    #---------------------------------------------------------------------------
    def test_append_many(self):
        items = [ ('fly', 6), 
                  ('fish', 0),
                  ('dog', 4),
                  ('human', 2),
                  ('chimp', 2),
                  ('bird', 2) ]
        
        lst = []
        for name, legs in items:
            lst.append(Animal(name, legs))
        
        ol = objlist.ObjList(class_name = Animal)
        assert ol.count() == 0
        
        ol.append_many(lst)
        assert ol.count() == 6
        
        ol.append_many(lst)
        assert ol.count() == 6
         
        idx = 0
        for i in ol:
            tup = items[idx]
            assert i.name == tup[0]
            assert i.legs == tup[1]
            idx += 1 
        
        assert idx == 6
        assert ol.count() == 6

    #---------------------------------------------------------------------------
    def test_has_item(self):
        ol = objlist.ObjList(class_name = Person)
        
        p = Person('jorgen', 35)
        ol.append(p)
        pp = Person('dewey', 1)
        ol.append(pp)       
        
        assert ol.has_item(p) == True
        assert ol.has_item(pp) == True
        
        pp = Person('dewey', 1)
        assert ol.has_item(pp) == False
               
    #---------------------------------------------------------------------------
    def test_get(self):
        items = [ ('fly', 6), 
                  ('fish', 0),
                  ('dog', 4),
                  ('human', 2),
                  ('chimp', 2),
                  ('bird', 2) ]
        
        ol = objlist.ObjList(class_name = Animal)
        for name, legs in items:
            ol.append(Animal(name, legs))
            
        idx = 0
        for i in xrange(0, ol.count()):
            tup = items[idx]
            assert ol[i].name == tup[0]
            assert ol[i].legs == tup[1]
            idx += 1 
        
        assert idx == 6
        assert ol.count() == 6
        
        assert ol[20] == None
        assert ol[-1] == None
        
