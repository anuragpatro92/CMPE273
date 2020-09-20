from sqlitedict import SqliteDict
from Bookmark import Bookmark



mydict = SqliteDict('./test_db.sqlite', autocommit=True)



mydict['1'] = Bookmark(1,"book1","https://www.pinterest.com/pin/27373510214883341/","Innovation Engine")
  # prints the new value
 # etc... all dict functions work
#mydict.close()