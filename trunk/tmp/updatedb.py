import sqlite3

sql = """
                /* alter table song add column relpath TEXT; */
                update song set relpath = '{artist}\{title}';                                   
      """
                                      
#c = sqlite3.connect(r"c:\Documents and Settings\Jorg\Application Data\GuitarPortFolio\guitarportfolio.db")
#c = sqlite3.connect(r"E:\Documents and Settings\Jorgen.CARDIO\Application Data\GuitarPortFolio\guitarportfolio.db")
c = sqlite3.connect(r"D:\personal\appdata\guitarportfolio\guitarportfolio.db ")
c.executescript(sql)
c.commit()
