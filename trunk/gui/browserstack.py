
class BrowserStack(object):
    """
    A class that maintains the stack of a list of tuples. The history can be 
    maintained or manipulated, or previewed.
    """
    
    def __init__(self, stackSize = 10):
        self._stack = []
        self._index = -1
        self._stackSize = stackSize
        # callback mechanism when stack pointer changes
        # signature: _callbackOnChange(pageTuple)
        self.callbackOnChange = None
        
    # -------------------------------------------------------------------------
    def Reset(self):
        """
        Resets the stack and issues a change
        """
        self._stack = []
        self._index = -1
        self._CallBack(None)

    # -------------------------------------------------------------------------
    def ResetAndPush(self, pageTuple):
        """
        Resets the stack, and push a new one on the stack. 
        """
        self._stack = []
        self._index = -1
        self.Push(pageTuple)
        
    # -------------------------------------------------------------------------
    def Push(self, pageTuple, not_allowed = []):
        """
        Pushes a page on the stack, only when it is not already pointing to 
        that page, also the forward part of the stack is truncated and 
        the stack is trimmed in case it contains more then 'x' items
        """
        if len(self._stack):
            # truncate 
            self._stack = self._stack[0 : self._index + 1]
            if self._index > self._stackSize:
                # attempt removal of excess space            
                self._stack = self._stack[self._stackSize : ]
                self._index = self._index - self._stackSize

        # append if not yet present
        if self.CurrentPage() != pageTuple:
            self._stack.append(pageTuple)
            self._index = len(self._stack) - 1  

        # when we must check for past pages that are not allowed, 
        # remove them from the stack
        if len(self._stack) and len(not_allowed):
            new_stack = []
            last_item = self.CurrentPage()
            for i in xrange(0, self._index):
                if self._stack[i][0] not in not_allowed:
                    new_stack.append(self._stack[i])
                                    
            # here we rely on the fact the index is at the end of the 
            # stack, which is always the case with a push
            if last_item:
                new_stack.append(last_item)
            self._stack = new_stack
            self._index = len(new_stack) - 1
                   
        # always callback
        self._CallBack(pageTuple) 
                      
    # -------------------------------------------------------------------------
    def Truncate(self):
        """
        Truncate the stack, leave the current index as only item
        so that there is no forward or backward navigation. This is 
        done so that deleted songs are not left in the cache
        """
        
        page = self.CurrentPage()
        self._stack = []
        self._index = -1
        # re add one single page
        if page:
            self.Push(page)        
          
    # -------------------------------------------------------------------------
    def CurrentPage(self):
        """
        Returns the current page on the stack, None if there is not any
        """
        if len(self._stack) and self._index >= 0:
            return self._stack[self._index]
        else:
            return None

    # -------------------------------------------------------------------------
    def HistoryBack(self):
        """
        Go one back on the stack if possible, else ignore the request
        Does not emit a callback!
        """
        if len(self._stack) > 0 and self._index >= 1:
            self._index -= 1
            return True
        return False

    # -------------------------------------------------------------------------
    def CanBrowseBack(self):
        """
        Return true when we can browse back
        """
        if len(self._stack) > 0 and self._index >= 1:
            return True
        return False

    # -------------------------------------------------------------------------
    def HistoryForward(self):
        """
        Go one forward on the stack if possible, else ignore the request
        Does not emit a callback!
        """
        if len(self._stack) and self._index < (len(self._stack) - 1):
            self._index += 1
            return True
        return False

    # -------------------------------------------------------------------------
    def CanBrowseForward(self):
        """
        Return true when we can browse forward
        """
        if len(self._stack) and self._index < (len(self._stack) - 1):
            return True
        return False

    # -------------------------------------------------------------------------
    def IsCurrentPage(self, pageTuple):
        """
        Returns True if the curent page displayed is the given pageTuple
        """
        return self.CurrentPage() == pageTuple

    # -------------------------------------------------------------------------
    def _CallBack(self, pageTuple):
        """
        Callback broker
        """
        if self.callbackOnChange:
            self.callbackOnChange(pageTuple)
            
