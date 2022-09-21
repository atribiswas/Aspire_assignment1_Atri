import pandas
import random
from pathlib import Path
import os
class Maker:
    def __init__(self,amt):
        self.df=self.make_df(amt)
    f_name_list=['John','Jacob','Piyush','Mary','Atri','Rohan','Anushka','Ayush','Joy','Niladri']
    l_name_list=['Marston','Colierre','Halder','Burnham','Biswas','Joshi','Sharma','Roy','Sen']
    email='abc@google.com'
    city='Kolkata'
    state='West Bengal'
    gender=['male','female','not listed']
    dept=['Sales','Development','Marketing','Analytics']
    ctclow,ctchigh,ctcbreak=100000,3000000,100000
    doj=['10/10/2022','10/8/2022','10/7/2022']
    active=[0,1]
    def make_df(self,amt):
        data = {'f_name': [random.choice(self.f_name_list) for i in range(0,amt)],
                'l_name': [random.choice(self.l_name_list) for i in range(0,amt)],
                'email':[self.email for i in range(0,amt)],
                'city':[self.city for i in range(0,amt)],
                'state':[self.state for i in range(0,amt)],
                'gender':[random.choice(self.gender) for i in range(0,amt)],
                'dept':[random.choice(self.dept) for i in range(0,amt)],
                'ctc':[random.randrange(self.ctclow,self.ctchigh,self.ctcbreak) for i in range(0,amt)],
                'doj':[random.choice(self.doj) for i in range(0,amt)],
                'active':[random.choice(self.active) for i in range(0,amt)]
        }
        df=pandas.DataFrame(data)
        return df
    def make_csv(self):
        filepath=Path('emp.csv')
        filepath.parent.mkdir(parents=True, exist_ok=True)  
        self.df.to_csv(filepath, index=False)
        file_stat = os.stat('emp.csv')
        print('Successfully Created file of ',self.convert_bytes(file_stat.st_size))

    def convert_bytes(self,bytes_number):
        tags = [ "Byte", "Kilobyte", "Megabyte", "Gigabyte", "Terabyte" ]
    
        i = 0
        double_bytes = bytes_number
    
        while (i < len(tags) and  bytes_number >= 1024):
                double_bytes = bytes_number / 1024.0
                i = i + 1
                bytes_number = bytes_number / 1024
    
        return str(round(double_bytes, 2)) + " " + tags[i]