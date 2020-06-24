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

class BitState():
   
   @staticmethod
   def hasBit( binValue, binCompare ):
      return binValue & binCompare != 0
   
   @staticmethod
   def setBit( binValue, binCompare ):
      if BitState.hasBit( binValue, binCompare ):
         return binValue
      return binValue | binCompare
   
   @staticmethod
   def delBit( binValue, binCompare ):
      if not BitState.hasBit( binValue, binCompare ):
         return binValue
      return binValue ^ binCompare