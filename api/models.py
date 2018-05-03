from __future__ import unicode_literals

from django.db import models
from mongoengine import Document,StringField,IntField,ListField,DateTimeField,connect
from datetime import *
connect('k_law')


# Create your models here.
#table with user account information
class Account(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    accttype = models.IntegerField(default=0)
    lastrenewaldate = models.DateTimeField('last date renewed')
    nextrenewaldate = models.DateTimeField('next date renewed')
    createdate = models.DateTimeField('date created')

#table containing accounttype
class AccountType(models.Model):
    id = models.AutoField(primary_key=True)
    validity = models.IntegerField(default=0)
    name = models.CharField(max_length=500)

#table containing annotations
class Annotations(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    case_id = models.IntegerField(default=0)
    ratio_title = models.TextField(default="")
    ratio_body = models.TextField(default="")
    position = models.IntegerField(default=0)
    comment = models.TextField(default="")
    createdate = models.DateTimeField('date created')


#table containing clients
class Clients(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(default="")
    phone = models.TextField(default="")
    email = models.TextField(default="")
    address = models.TextField(default="")
    facetime = models.TextField(default="")
    skype = models.TextField(default="")


#table containing device types
#web,mobile,desktop
class DeviceTypes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

#table containing notes
class Notes(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    case_id = models.IntegerField(default=0)
    ratio_title = models.TextField(default="")
    ratio_body = models.TextField(default="")
    position = models.IntegerField(default=0)
    comment = models.TextField(default="")
    createdate = models.DateTimeField('date created')

#table containing packages names
#package name
class Package(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


#table containing packages access
#package access
class PackageAccess(models.Model):
    id = models.AutoField(primary_key=True)
    packageid = models.IntegerField(default=0)
    deviceid=models.IntegerField(default=0)
    resourceid=models.IntegerField(default=0)


#table containing packages names
#package name
class PackageInfo(models.Model):
    id = models.AutoField(primary_key=True)
    packageid = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    numconcurrency = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=20,decimal_places=2)


#table containing packages data
#package data
class PackageData(models.Model):
    id = models.AutoField(primary_key=True)
    packageid = models.IntegerField(default=0)
    tablename=models.CharField(max_length=100)
    fulltablename=models.CharField(max_length=100)


#table with user profile information
class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=25)
    skype = models.CharField(max_length=200)
    facetime = models.CharField(max_length=200)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.IntegerField(default=0)
    city_other = models.CharField(max_length=200)
    state = models.IntegerField(default=0)
    state_other = models.CharField(max_length=200)
    town = models.IntegerField(default=0)
    town_other = models.CharField(max_length=200)
    country = models.IntegerField(default=0)
    createdate = models.DateTimeField('date created')



#table containing resource
class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    tablename = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    resourcename = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    createdate = models.DateTimeField('date created')


#table with user login details
class Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    assignee = models.CharField(max_length=500)
    description = models.TextField(default="")
    due = models.CharField(max_length=500)
    status = models.CharField(max_length=500)
    completed = models.CharField(max_length=500)
    case_title = models.TextField(default="")
    notes = models.TextField(default="")


#table with user login details
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=500)
    secret = models.CharField(max_length=500)
    status = models.IntegerField(default=0)
    is2faverified = models.IntegerField(default=0)
    isemailverified = models.IntegerField(default=0)
    role = models.IntegerField(default=0)
    createdate = models.DateTimeField('date created')

#table for user roles
#1= normal user
#2= normal admin user
#3= super admin user
class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


#table for user group
#A group a user can be subscribed to
class UserGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


#table for user group
#A group a user can be subscribed to
class UserGroupList(models.Model):
    id = models.AutoField(primary_key=True)
    groupid = models.IntegerField(default=0)
    uid =   models.IntegerField(default=0)

#table containing user access
#user access
class UserAccess(models.Model):
    id = models.AutoField(primary_key=True)
    packageid = models.IntegerField(default=0)
    uid=models.IntegerField(default=0)


#table containing access types web,android,ios
class UserValidity(models.Model):
    id = models.AutoField(primary_key=True)
    uid=models.IntegerField(default=0)
    lastrenewdate = models.DateTimeField("")
    nextrenewdate = models.DateTimeField("")

#table containing subject matters
class UserAccessList(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    accesstype = models.IntegerField(default=0)





#table containing countries
class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)


#table containing sms
class SMS(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    sender = models.CharField(max_length=20)
    recepient = models.CharField(max_length=2400)
    message = models.CharField(max_length=1000)

#table containing outbound emails
class Email(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(default=0)
    sender = models.CharField(max_length=200)
    recepient = models.CharField(max_length=2400)
    message = models.CharField(max_length=1000)

#table containing states
class State(models.Model):
    id = models.AutoField(primary_key=True)
    countryid = models.IntegerField(default=0)
    name = models.CharField(max_length=500)

#table containing cities
class City(models.Model):
    id = models.AutoField(primary_key=True)
    stateid = models.IntegerField(default=0)
    countryid = models.IntegerField(default=0)
    title = models.CharField(max_length=500)
    name = models.CharField(max_length=500)

class Admin(models.Model):
    db_table = 'admin'
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)
    role = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    createdate = models.DateTimeField('date created')

class AdminRole(models.Model):
    db_table = 'adminrole'
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    createdate = models.DateTimeField('date created')


#table containing sections oflaws of the federation
#has relationship law table
class Sections(models.Model):
    id = models.AutoField(primary_key=True)
    part = models.CharField(max_length=1000)
    lawid = models.IntegerField(default=0)
    partschedule = models.CharField(max_length=100)
    title = models.CharField(max_length=1000)
    body = models.TextField(default="")
    postdate = models.DateTimeField('post date')
    updatedate = models.DateTimeField('update date')


#table containing laws of the federation
class Laws(models.Model):
    id = models.AutoField(primary_key=True)
    cover = models.CharField(max_length=5000)
    title = models.CharField(max_length=1000)
    number = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    description = models.TextField(default="")
    postdate = models.DateTimeField('post date')
    updatedate = models.DateTimeField('update date')


#table containing laws of the federation
class SubsidiaryLegislation(models.Model):
    id = models.AutoField(primary_key=True)
    lawid = models.IntegerField(default=0)
    cover = models.CharField(max_length=5000)
    title = models.CharField(max_length=1000)
    number = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    description = models.TextField(default="")
    postdate = models.DateTimeField('post date')
    updatedate = models.DateTimeField('update date')


#table containing sections oflaws of the federation
#has relationship law table
class SubsidiaryLegislationSections(models.Model):
    id = models.AutoField(primary_key=True)
    lawid = models.IntegerField(default=0)
    partschedule = models.CharField(max_length=100)
    title = models.CharField(max_length=1000)
    body = models.TextField(default="")
    postdate = models.DateTimeField('post date')
    updatedate = models.DateTimeField('update date')


#table containing sections oflaws of the federation
#has relationship law table
class SubsidiaryLegislationSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    lawid = models.IntegerField(default=0)
    partschedule = models.CharField(max_length=100)
    title = models.CharField(max_length=1000)
    body = models.TextField(default="")
    postdate = models.DateTimeField('post date')
    updatedate = models.DateTimeField('update date')

#table containing chapters
#has relationship with sections
class Chapter(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(default="")

#table containing sections
#has relationship with chapters and subsection
class Section(models.Model):
    id = models.AutoField(primary_key=True)
    chapterid = models.IntegerField(default=0)
    code = models.IntegerField(default=0)
    sectiontitle = models.TextField(default="")

#table containing subsections
#has relationship with sections
class SubSection(models.Model):
    id = models.AutoField(primary_key=True)
    sectionid = models.IntegerField(default=0)
    subsectioncode = models.IntegerField(default=0)
    subsectiontitle = models.TextField(default="")

#table containing subsubsections
#has relationship with subsections
class SubSubSection(models.Model):
    id = models.AutoField(primary_key=True)
    subsectionid = models.IntegerField(default=0)
    subsubsectioncode = models.IntegerField(default=0)
    subsubsectiontitle = models.TextField(default="")

#table containing subsubsections
#has relationship with subsections
class SubSubSectionItem(models.Model):
    id = models.AutoField(primary_key=True)
    subsubsectionid = models.IntegerField(default=0)
    subsubsectionitemcode = models.IntegerField(default=0)
    subsubsectionitemtitle = models.TextField(default="")

#table containing transaction information
class Transactions(models.Model):
    db_table = 'transactions'
    id = models.AutoField(primary_key=True)
    packageinfo = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    uid = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=20,decimal_places=2)
    description = models.CharField(max_length=1000)
    otherref = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    tax = models.DecimalField(max_digits=20,decimal_places=2)
    commission = models.DecimalField(max_digits=20,decimal_places=2)
    voucher_code = models.CharField(max_length=20)
    status = models.IntegerField(default=0)
    createdate = models.DateTimeField('date created')


#table containing updates
class Updates(models.Model):
    id = models.AutoField(primary_key=True)
    packageid = models.IntegerField(default=0)
    updateid = models.CharField(max_length=1000)
    viewmodels = models.TextField(default="")
    generateddate = models.DateTimeField('date created')


def searchResultToJson(result):
    searchlist=[]
    for a in result:
        data={}
        data['id']=a.lawid
        data['label']=a.lawtitle
        searchlist.append(data)
    return searchlist

def getPackageDict(package):
    packagelist=[]
    for p in package:
        data={}
        data['id']=p.id
        data['name']=p.name
        packagelist.append(data)
    return packagelist



def transactionsToJson(transactions):
    transactionlist=[]
    for s in transactions:
        data={}
        data['id']=s.id
        data['username']=s.username
        data['amount']=s.amount
        data['description']=s.description
        data['paymentdate']=s.paymentdate
        data['status']=s.status
        transactionlist.append(data)
    return transactionlist


def sectionsToJson(id,sections):
    sectionlist=[]
    for s in sections:
        data={}
        data['id']="id"+str(s.id)
        data['text']=s.title.replace("\t"," ")
        data['parent']=id
        sectionlist.append(data)
    sorted(sectionlist)
    return sectionlist


def sectionDetailToJson(section):
    data={}
    data['id']=section.id
    data['title']=section.title
    data['body']=section.body.replace("\n","<br>")
    data['schedule']=section.partschedule
    data['postdate']=str(section.postdate.strftime('%Y-%m-%d'))
    return data


def lawdataToJson(laws):
    lawlist=[]
    for l in laws:
        data={}
        data['id']=l.id
        data['title']=l.title
        lawlist.append(data)
    return lawlist


def sectiondataToJson(sections):
    lawlist=[]
    for l in sections:
        data={}
        data['id']=l.id
        data['title']=l.title
        data['body']=l.body.replace("\n","<br>")
        lawlist.append(data)
    return lawlist


def lawsviewToJson(laws):
    lawlist=[]
    for l in laws:
        data={}
        data['id']=l.id
        data['title']=l.title.replace("\t"," ")
        lawlist.append(data)
    return lawlist



def lawsToJson(laws):
    lawlist=[]
    for l in laws:
        data={}
        data['id']=l.id
        data['parent']="#"
        data['text']=l.title.replace("\t"," ")
        data['children']=True
        data['type']='root'
        lawlist.append(data)
    return lawlist

def lawfullToJson(l):
    data={}
    data['id']=l.id
    data['cover']=l.cover.replace("\t"," ").replace("\n","<br/>")
    data['title']=l.title.replace("\t"," ")
    return data

def adminToJson(admin):
    adminlist=[]
    for a in admin:
        data={}
        data['id']=a.id
        data['username']=a.username
        data['status']=a.status
        data['role']=a.role
        adminlist.append(data)
    return adminlist


def accountToJson(account):
    resourcelist=[]
    for r in account:
        data={}
        data['id']=r.id
        data['name']=r.name
        data['resourcename']=r.resourcename
        data['description']=r.description
        data['title']=r.title
        resourcelist.append(data)
    return resourcelist


def getAccountDict(account):
    resourcelist=[]
    for r in account:
        data={}
        data['id']=r.id
        data['name']=r.name
        data['resourcename']=r.resourcename
        data['description']=r.description
        data['title']=r.title
        resourcelist.append(data)
    return resourcelist


def resourceToJson(resource):
    resourcelist=[]
    for r in resource:
        data={}
        data['id']=r.id
        data['name']=r.name
        data['resourcename']=r.resourcename
        data['description']=r.description
        data['title']=r.title
        data['createdate']=r.createdate
        resourcelist.append(data)
    return resourcelist



def notesToJson(notes):
    notelist=[]
    for n in notes:
        data={}
        data['id']=n.id
        data['case_id']=n.case_id
        data['ratio_title']=n.ratio_title
        data['uid']=n.uid
        data['position']=n.position
        data['comment']=n.comment
        notelist.append(data)
    return notelist

def annotationToJson(annotations):
    annotationlist=[]
    for n in annotations:
        data={}
        data['id']=n.id
        data['case_id']=n.case_id
        data['ratio_title']=n.ratio_title
        data['uid']=n.uid
        data['position']=n.position
        data['comment']=n.comment
        annotationlist.append(data)
    return annotationlist

def usersToJson(users):
    clist=[]
    for u in users:
        data={}
        data['id']=u.id
        data['firstname']=u.firstname
        data['lastname']=u.lastname
        data['email']=u.email
        data['username']=u.username
        data['status']=u.status
        clist.append(data)
    return clist

def accounttypeToJson(accounttypes):
    clist=[]
    for a in accounttypes:
        data={}
        data['id']=a.id
        data['name']=a.name
        data['validity']=a.validity
        clist.append(data)
    return clist


def getAccounttypeDict(accounttypes):
    alist=[]
    for c in accounttypes:
        data={}
        data['id']=c.id
        data['name']=c.name
        data['validity']=c.validity
        alist.append(data)
    return alist


def dictionaryToJson(dictionary):
    clist=[]
    for d in dictionary:
        data={}
        data['id']=d.id
        data['title']=d.title
        data['content']=d.content
        clist.append(data)
    return clist

def maximToJson(maxims):
    clist=[]
    for m in maxims:
        data={}
        data['id']=m.id
        data['title']=m.title
        data['content']=m.content
        clist.append(data)
    return clist


