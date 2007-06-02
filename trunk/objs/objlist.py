
class ObjListException(Exception):
    pass

class ObjListIterator(object):
    def __init__(self, objlist):
        self.__objlist = objlist
        self.__idx = 0
    
    #---------------------------------------------------------------------------
    def __iter__(self):
        return self
        
    #---------------------------------------------------------------------------
    def next(self):
        result = None
        if self.__idx >= len(self.__objlist):
            raise StopIteration()
        else:
            result = self.__objlist[self.__idx]
            self.__idx += 1
        return result
   
#===============================================================================
    
""" ObjList - A managed somewhat strong typed list for Python.
    Expects {object}._id to be a property """

class ObjList(object):
    def __init__(self, class_name, add_callback = None, 
                 remove_callback = None, clear_callback = None):
        self.__list = []
        self.__cname = class_name
        self.__add_cb = add_callback
        self.__remove_cb = remove_callback
        self.__clear_cb = clear_callback
        # property to indicate change
        self.__changed = False
        # property to indicate peristence
        self.__restored = False

    #---------------------------------------------------------------------------
    def __iter__(self):
        return ObjListIterator(self.unmanaged_list())
           
    #---------------------------------------------------------------------------
    def __getitem__( self, key): 
        if key < len(self.__list) and key >= 0:
            return self.__list[key]
        return None
     
    #---------------------------------------------------------------------------
    def clear(self):
        if self.__clear_cb:
            self.__clear_cb(self)
        self.__list = []
        self.__changed = True
        
    #---------------------------------------------------------------------------
    def append(self, obj):
        if isinstance(obj, self.__cname):
            if obj not in self.__list:
                self.__list.append(obj)
                if self.__add_cb:
                    self.__add_cb(self, obj)
                self.__changed = True
        else:
          raise ObjListException() 

    #---------------------------------------------------------------------------
    def remove(self, obj):
        if obj in self.__list:
            self.__list.remove(obj)
            if self.__remove_cb:
                self.__remove_cb(self, obj)
                self.__changed = True
           
    #---------------------------------------------------------------------------
    def count(self):
        return len(self.__list)           
         
    #---------------------------------------------------------------------------
    def unmanaged_list(self):
        return self.__list[:]          

    #---------------------------------------------------------------------------
    def find_id(self, id):
        for i in self.__list:
            if i._id == id:
                return i
        return None
        
    #---------------------------------------------------------------------------
    def has_item(self, obj):
        if obj in self.__list:
            return True
        return False
    
    #---------------------------------------------------------------------------
    def append_many(self, lst):
        for l in lst:
            self.append(l)
            
    #---------------------------------------------------------------------------
    def is_restored(self):
        """ Returns true when the list is in a restored state, meaning even 
            empty lists are still the result of what a database peer put in there """
        return self.__restored

    #---------------------------------------------------------------------------
    def is_changed(self):
        """ Returns true when the list is changed by adding, clearing or 
            removing elements. Changes in the objects inside the list is not
            considered a change, only the collection """
        return self.__changed
                    
    #---------------------------------------------------------------------------
    def set_restored(self):
        """ Sets the restored status to true, and sets the changed flag to 
            false. This state indicates a fresh restored collection, but 
            it carries the inforation that was present in the DB even when
            it is an empty list """
        self.__restored = True
        self.__changed = False

    #---------------------------------------------------------------------------
    def set_clean(self):
        """ Sets the changed status to false """
        self.__changed = False

    #---------------------------------------------------------------------------
    def prune(self):
        """ Prune will clear the list, reset the restored status to false so that
            database peers will not consider this a valid list to use in update 
            actions. """
        self.__restored = False
        self.clear()
        self.__changed = False
