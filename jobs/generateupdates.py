import MySQLdb
import json
import zipfile
from bson import json_util
import os
import sys
import datetime
import uuid
from django.utils import timezone
from django.utils.encoding import *
import pickle
import sys
sys.path.append('..')
import settings
updatesfolder=settings.updatesfolder
class UpdatesManager:
    def __init__(self):
        pass

class DBUtil:
    def __init__(self,name,username,password,tb_prefix,tablelist=None,numupdates=None,packageid=None):
        self.name=name
        self.packageid=packageid
        self.username=username
        self.password=password
        self.prefix=tb_prefix
        self.tablelist=tablelist
        self.numupdates=numupdates
        self.getHandle()

    def getPreviousUpdates(self):
        query="SELECT updateid FROM api_updates WHERE packageid="+str(self.packageid)
        self.rows=self.cursor.execute(query)
        self.result=self.cursor.fetchall()
        for res in self.result:
            self.updateid=res[0]
            data=self.readUpdatesFile(self.updateid)
            print json.loads(data)

    def readUpdatesFile(self,updateid):
        filepath="../tmp/datamodels_"+updateid+".txt"
        data=""
        if os.path.exists(filepath):
            with open(filepath) as f:
                data=f.read()
        return data


   #Database handle
    def getHandle(self):
        self.connection = MySQLdb.connect("localhost",self.username,self.password,self.name)
        self.cursor=self.connection.cursor()
        return self.cursor
    #List tables
    def listTables(self):
        if self.tablelist!=None:
            self.tables=self.tablelist
        else:
            self.tables=[]
            self.query="SHOW TABLES"
            self.rows=self.cursor.execute(self.query)
            self.result=self.cursor.fetchall()
            #print self.result
            for t in self.result:
                table=t[0]
                if self.prefix in table:
                    self.tables.append({"name":table.replace(self.prefix,""),"table":table})
        return self.tables

    def queryObject(self,name):
        self.query="SELECT * from "+name
        self.rows=self.cursor.execute(self.query)
        self.result=self.cursor.fetchall()
        return self.result


    def logupdates(self,packageid,updateid,viewmodels,generatedate):
        self.query="INSERT INTO api_updates(packageid,updateid,viewmodels,generateddate) VALUES('{}','{}','{}','{}')".format(packageid,updateid,viewmodels,generatedate)
        self.cursor.execute(self.query)
        self.connection.commit()
        return self.result

    #Describe a table
    def describeTable(self,tablename):
        self.query="DESCRIBE "+tablename
        self.rows=self.cursor.execute(self.query)
        self.result=self.cursor.fetchall()
        return self.result


    def splitupdates(self,lst,sz):
        return [
        [lst[i] for i in range(len(lst)) if (i % sz) == r]
        for r in range(sz)
    ]

    def getIds(self,tablename,results):
        data={}
        data['name']=tablename
        listids=[]
        for res in results:
            listids.append(res[0])
        data['ids']=listids
        return data


    def generateUpdates(self,maxresults):
        self.updatename=str(uuid.uuid4())
        self.generateUpdatesFolder()
        jsondata={}
        jsondata['database']=self.name
        jsondata['tables']=[]
        tables=self.listTables()
        print "Number of updates required ",self.numupdates
        tableinfo=[]
        for table in tables:
            objname=table['table']
            tablename=table['name']
            td={}
            td['name']=tablename
            results=self.queryObject(objname)
            tableids=self.describeTable(objname)
            td['ids']=self.getIds(tablename,results)
            td['schema']=tableids
            tablelist=self.splitupdates(results,self.numupdates)
            print "Total records in "+tablename+" "+str(len(results))
            td['data']=tablelist
            tableinfo.append(td)
        views=[]
        for i  in range(self.numupdates):
            outdata=[]
            for t in tableinfo:
                tablename=t['name']
                schema=t['schema']
                records=t['data']
                values={}
                values['name']=tablename
                if len(records[i])>0:
                    values['data']=self.generateStructuredData(schema,records[i])
                else:
                    values['data']={}
                views.append(t['ids'])
                outdata.append(values)
            self.makeUpdate(i,outdata,self.updatename,self.updatename)
        viewmodels=str(pickle.dumps(views))
        if not os.path.exists("../tmp"):
            os.makedirs("../tmp")
        with open(updatesfolder+self.updatename+"/datamodels_"+self.updatename+".txt","w+") as f:
            f.write(viewmodels)
        currenttime=datetime.datetime.now()
        self.logupdates(self.packageid,self.updatename,self.updatename,currenttime.strftime('%Y-%m-%d %H:%M:%S'))
        print "Completed"

    def generateUpdatesFolder(self):
        if not os.path.exists(updatesfolder):
            os.makedirs(updatesfolder)
        if not os.path.exists(updatesfolder+self.updatename):
            os.makedirs(updatesfolder+self.updatename)

    def makeUpdate(self,i,data,filename,viewmodels):
        outfile=updatesfolder+self.updatename+"/"+str(i)+".json"
        outfilezip=updatesfolder+self.updatename+"/"+str(i)+".zip"
        with open(outfile,"w+") as f:
            f.write(json.dumps(data))
        zf = zipfile.ZipFile(outfilezip,'w',zipfile.ZIP_DEFLATED)
        try:
            zf.write(outfile)
        finally:
            print 'closing'
            zf.close()
            os.remove(outfile)


    def generateStructuredData(self,fields,dataarrays):
        datalist=[]
        for dataarray in dataarrays:
            data=[]
            for field in fields:
                pos=fields.index(field)
                if isinstance(dataarray[pos],str):
                    #print dataarray[pos]
                    dataval=dataarray[pos].decode('latin-1').encode("utf-8","ignore")
                    #print field[0],dataval[0:1]
                elif isinstance(dataarray[pos],datetime.datetime):
                    dataval='{:%Y-%m-%d %H:%M}'.format(dataarray[pos])
                    #print field[0],dataval[0:1]
                else:
                    dataval=dataarray[pos]
                    #print field[0],dataval
                data.append({field[0]:dataval})
            datalist.append(data)

        return datalist


def split_seq(seq, size):
        newseq = []
        splitsize = 1.0/size*len(seq)
        for i in range(size):
                newseq.append(seq[int(round(i*splitsize)):int(round((i+1)*splitsize))])
        return newseq
#handle previous updates by appending to xml file
if __name__=="__main__":
    maxresults=50000
    numupdates=10
    packageid="1"
    tablelist=[
{"table":"api_laws","name":"laws"},
{"table":"api_sections","name":"sections"}
]
    util=DBUtil("k_law","root","hy76gdgdDssv43Q","api_",tablelist,numupdates,packageid)
    #util.getPreviousUpdates()
    datalist=util.generateUpdates(maxresults)
