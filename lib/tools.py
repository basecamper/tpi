import time


EMPTY_STRING = ""


def getMsTimestamp():
   return int(round(time.time() * 1000))

def getNextDictionaryItem( dict : object, key : str ):
   try:
      found = False
      for k in orderedDict.keys():
         if found:
            return g
         if k == key:
            found = True
   except:
      pass
   return None

def getPrevDictionaryItem( dict : object, key : str ):
   try:
      found = False
      last = None
      for k in orderedDict.keys():
         if k == key:
            return last
         last = k
   except:
      pass
   return None

def raiseNotInstanceOf( obj, cl ):
   if isinstance( obj, cl ):
      return obj
   e = TypeError( "{o} is not of class {c}".format(
      o=obj,
      c=cl
   ) )
   raise e