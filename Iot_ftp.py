from ftplib import FTP
import datetime
import csv
##import schedule
# pip install firebase-admin google-cloud-firestore
from firebase import firebase
import time


class setUp:
    def __init__(self):
        self._ftp = ''
        self._user =''
        self._password =''
        self._CSV_folder =''
        self._CSV_name =''
        self._date = ''
    def setFTP(self, ftp):
        self._ftp = ftp
    def getFTP(self):
        return self._ftp
    def setUser(self, user):
        self._user = user
    def getUser(self):
        return self._user
    def setPassword(self, password):
        self._password = password
    def getPassword(self):
        return self._password
    def setCSV_folder(self, folder):
        self._CSV_folder = folder
    def getCSV_folder(self):
        return self._CSV_folder
    def setCSV_name(self, name):
        self._CSV_name = name
    def getCSV_name(self):
        return self._CSV_name
    def setDate(self):
        self._date = datetime.datetime.now()
    def getDate(self):
        return str(self._date).replace(':','-').replace(' ','-').replace('.','-').split('-')[:-1]


     

def getFile(ftp, filename):
    try:
        ftp.retrbinary("RETR " + filename ,open(filename, 'wb').write)
    except:
        print("Error")


def job(obj):
    ftp = FTP(obj.getFTP())
    ftp.login(obj.getUser(),obj.getPassword())
    print('Will download:'+obj.getCSV_name())
    ftp.cwd(obj.getCSV_folder())
    data = []
    ftp.dir(data.append)
    for line in data:
        print("-", line)
    getFile(ftp,obj.getCSV_name()+'.csv')
    time.sleep(2)
    # ftp.quit()
    # ftp.close()
def csvfile(file_name):
    file=open(file_name+'.csv','r',encoding='utf-8')
    url='https://monitor-1d512.firebaseio.com/' 
    fb=firebase.FirebaseApplication(url,None)
    csvCursor=csv.reader(file)
    next(csvCursor, None)
    fb.delete(file_name,None)
    for row in csvCursor:
        Voltage=row[6]
        Amphere=row[7]
        B_temp=row[2]
        v=float(Voltage)
        i=float(Amphere)  
        t=float(B_temp)
        back_temp=str(round(t*100/32768,2))
        print(str(v*i))
        
        fb.post(file_name,{'Time':row[1],'Power':str(v*i),'Back_temp':back_temp})
  
    
    # result = fb.get('/users', '1')
    # print(result)
    file.close()
    
def main():
    '''set up here'''
    obj = setUp()
    obj.setFTP('192.72.189.223')
    obj.setUser('admin')
    obj.setPassword('Admin')
    obj.setDate()
    obj.setCSV_folder('/LOG/Folder1/'+obj.getDate()[0]+obj.getDate()[1])
    obj.setCSV_name(obj.getDate()[1]+obj.getDate()[2]+'_'+obj.getDate()[3])
    '''///////////'''
    job(obj)
    file_name=str(obj.getDate()[1]+obj.getDate()[2]+'_'+obj.getDate()[3])
    print('Parsing csv'+file_name)
    csvfile(file_name)
    # upload_date(file_name)    
if __name__ == "__main__":
    main()