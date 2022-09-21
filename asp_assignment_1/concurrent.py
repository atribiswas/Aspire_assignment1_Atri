from cmath import exp
import mysql.connector
from datetime import datetime,timedelta
import pandas as pd


#CHECKER CLASS USED TO CHECK IF DB CONNECTION IS VALID
class Checker:
    @staticmethod
    def check_connection(**kwargs):
        try:
            mysql.connector.connect(
            host=kwargs['host'],
            user=kwargs['user'],
            password=kwargs['password'],
            database=kwargs['db_name']
            )
            print("Good Connection")
            return True

        except Exception as e:
            print("Bad Connection. Try Again- %s"%e)
            return False
        
#CONCURRENT CLASS CREATES AND OBJECT TO CREATE CONCURRENT INSERTS INTO REGISTERED DATABASE

class Concurrent:
    def __init__(self,end=1000,cs=1000, **kwargs) -> None:
        self.cs=cs
        self.end=end
        if(kwargs):
            if(kwargs['all']==True):
                self.allitems=True
        else:
            self.allitems=False
    
    #BELOW FUNCTION CHECK IF THE TEST TABLE EXISTS IN THE GIVEN DATABASE AND RETURNS FALSE IF IT DOESN'T
    
    def checkTableExists(self,dbcon, tablename):
        print("Checking for existence of table- ",tablename)
        dbcur = dbcon.cursor()
        dbcur.execute(
            "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = \"%s\""%tablename)
        if dbcur.fetchall()[0][0] > 1:
            dbcur.close()
            return True

        dbcur.close()
        return False


    #THIS FUNCTION IS USED TO CREATE TEST TABLE IN DATABASE IF NO SUCH TABLE ALREADY EXISTS
    
    def makeTable(self,dbcon):
        cursor=dbcon.cursor()
        cursor.execute(
           " CREATE TABLE `emp` ("
           " `id` int NOT NULL AUTO_INCREMENT,"
           " `f_name` varchar(45) DEFAULT NULL,"
           " `l_name` varchar(45) DEFAULT NULL,"
           " `email` varchar(45) DEFAULT NULL,"
           " `city` varchar(45) DEFAULT NULL,"
           " `state` varchar(45) DEFAULT NULL,"
           " `gender` varchar(20) DEFAULT NULL,"
           " `dept` varchar(20) DEFAULT NULL,"
           " `ctc` decimal(12,2) DEFAULT NULL,"
           " `doj` date DEFAULT NULL,"
           " `active` tinyint(1) DEFAULT NULL,"
           " PRIMARY KEY (`id`)"
           " ) ENGINE=InnoDB AUTO_INCREMENT=25001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"
            )
        
    
    #THIS CORE FUNCTION CREATES THE CONNECTION, CALLS THE CHECKERS AND CREATES THE INSERT QUERY AND VALUES FROM THE CSV IN O(N) TIME.

    def make_concurrent(self,**kwargs):
        db = mysql.connector.connect(
        host=kwargs['host'],
        user=kwargs['user'],
        password=kwargs['password'],
        database=kwargs['db_name']
        )
        tablename='emp'
        if(self.checkTableExists(db,tablename)):
            print("Found test table in %s!\n"%kwargs['db_name'])
            pass
        else:
            print("Test table not detected in %s!\n"%kwargs['db_name'])
            self.makeTable(db)
            db.commit()
            print("New Table made\n")
        cursor = db.cursor()
        query = 'INSERT INTO emp(f_name,l_name,email,city,state,gender,dept,ctc,doj,active) VALUES(%s, %s, %s, %s,%s,%s, %s, %s, %s,%s)'                                                         

        my_data = []
        it=1
        flag=False
        fileObject=open('emp.csv')
        row_count = sum(1 for row in fileObject)
        
        
        #EVEN THOUGH THIS LOOKS LIKE O(N^2) TIME, IT'S BASICALLY O(A*B) COMPLEXITY WHERE N=A*B BECAUSE OF CHUNKING FEATURE OF PANDAS
        for df in pd.read_csv('emp.csv', iterator=True, chunksize=self.cs):
            rows=df.values.tolist()
            for row in rows:
                if(row[8]=='doj'):
                    continue
                row[8]=datetime.strptime(row[8],'%d/%m/%Y')
                my_data.append(tuple(row))
                if(self.allitems==False):
                    print('processed %d rows [%f%%]\t EST TIME:%s\r'%(it,it/self.end*100,str(timedelta(seconds=round(self.end*0.00026117)))),end='')
                else:
                    print('processed %d rows [%f%%]\t EST TIME:%s\r'%(it,it/row_count*100,str(timedelta(seconds=round(row_count*0.00026117)))),end='')

                it=it+1
                if it>self.end and self.allitems==False:
                    flag=True
                    break
            if flag==True:
                break
        print(f'{it-1} rows proccessed successfully!')
        cursor.executemany(query, my_data)
        print(f'{it-1} rows inserted into table concurrently')
        cursor.close()
        db.commit()
