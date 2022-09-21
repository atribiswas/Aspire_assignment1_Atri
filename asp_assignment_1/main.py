from maker import Maker
from concurrent import Concurrent,Checker
import time
def main():
    print("Welcome to my Large CSV File Uploader\n\n")
    input_string=input('Specify the number of rows in the csv file (15,000 rows is approximately 1 MB of data)\n')
    try:
        obj=Maker(int(input_string))
        obj.make_csv()
    except Exception as e:
        print('An error occured while creating the file:',e)
        return
    while True:
        cred=input('\nEnter DB details in format \'host,user,password,db_name\': ')
        cred=cred.split(',')
        cred_dict={
            'host':cred[0],
            'user':cred[1],
            'password':cred[2],
            'db_name':cred[3]
        }

        if(Checker.check_connection(**cred_dict)):
            break
        else:
            continue


    input_string=input('\nConfirm Insertion(Press enter)\n10,000 rows are inserted concurrently in chunks. Enter a number to insert select number of rows from csv(optional)\n')
    
    try:
        if(input_string==""):
            obj=Concurrent(all=True)
        elif(input_string.isnumeric()):
            obj=Concurrent(int(input_string))
        start_time =time.time()
        obj.make_concurrent(**cred_dict)
        print("--- processing took %s seconds ---" % (time.time() - start_time))
    except Exception as e:
        print('An error occured while uploading:',e)
        return
        

if __name__=="__main__":
    main()
        