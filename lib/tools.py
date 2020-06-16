import time


EMPTY_STRING = ""

def getMsTimestamp():
   return int(round(time.time() * 1000))

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