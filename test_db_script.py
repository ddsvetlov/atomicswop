import pprint
import pandas as pd
import pymongo
import bson
from bson.objectid import ObjectId

def getQuantityMultiTransaction():
    
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    with client:
        db = client.tst_app
        quantity = db.multi_transaction.find().count()
        transactionIds =[]
        for t in db.multi_transaction.find():
            transactionIds.append(t['_id'])
       
    return (quantity,transactionIds)

def addBackupData():
     
     client = pymongo.MongoClient('mongodb://localhost:27017/')
     with client:
        db =client.tst_app
        for item in db.user.find():
            
            db.userBackup.insert(item)

def getData(i,IDs): 
    
    #connect to db
    client = pymongo.MongoClient('mongodb://localhost:27017/')

    #make smth with db
    with client:

        db = client.tst_app
        
        value1 = []
        value2= []
        namecash1= []
        namecash2= []
        fromUser= []
        toUser = []
        fromCash = []
        toCash = []   
        transaction = [] 
        
        transac = db.multi_transaction.find_one({'_id': IDs })['MTrans']
        for item in range(0,len(transac),6):
            print("catcatcatctactactac")
            print(len(transac))
            value1.append(transac[item])
            value2.append(transac[item+1])
            namecash1.append(transac[item+2])
            namecash2.append(transac[item+3])
            fromUser.append(transac[item+4])
            print('get data')
            print('get data')
            print(fromUser)
            toUser.append(transac[item+5])
    
            
            us = db.user.find_one( {'_id': ObjectId(fromUser[i]) })
            
            print(us)
            fromCash.append(us[namecash1[i]])
            print(fromCash)
            us = db.user.find_one( {'_id': ObjectId(toUser[i]) })
            toCash.append(us[namecash2[i]])

            transaction.append(fromUser[i])
            transaction.append(toUser[i])
            transaction.append(fromCash[i])
            transaction.append(toCash[i])
            transaction.append(value1[i])
            transaction.append(namecash1[i])

            transaction.append(toUser[i])
            transaction.append(fromUser[i])
            transaction.append(toCash[i])
            transaction.append(fromCash[i])
            transaction.append(value2[i])
            transaction.append(namecash2[i])
        print('balblalblalblalbla')
        print(transac) 
    return(transaction)
    
def updateDB(fromCash, toCash, fromID, toID, cashID):
    print('update data')
    print(fromCash, toCash, fromID, toID, cashID)
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    with client:
        db = client.tst_app
        db.user.update_one({'_id': ObjectId(fromID)}, {'$set': {cashID : int(fromCash)}})
        db.user.update_one({'_id': ObjectId(toID)}, {'$set': {cashID : int(toCash)}})
    users_list = list(db.user.find())
    df = pd.DataFrame(users_list)
    print(df)
    # pprint.pprint(list(db.user.find()))

def callBackup():
    
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    with client:
        db = client.tst_app
        db.user.drop()
        db.user.insert_many(db.userBackup.find())
        db.userBackup.drop()

def deleteBackupData():
    
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    with client:
        db = client.tst_app
        db.userBackup.drop()
    
# def printDB():
    
#     client = pymongo.MongoClient('mongodb://localhost:27017/')
#     with client:
#         db = client.tst_app
#         users_list = list(db.users.find())
#         df = pd.DataFrame(users_list)
#         print("result DB after transaction")
#         print(df)
#         print("----------------------------")

# def cleanUpForTesting():
    
#     client = pymongo.MongoClient('mongodb://localhost:27017/')
#      #add test data
#     users = [
#     {'user_ID':1 , 'cash1':10 , 'cash2':20 , 'cash3':0 , 'cash4':0 },
#     {'user_ID':2 , 'cash1':10 , 'cash2':20 , 'cash3':0 , 'cash4':0 },
#     {'user_ID':3 , 'cash1':10 , 'cash2':20 , 'cash3':30 , 'cash4':0 },
#     {'user_ID':4 , 'cash1':0 , 'cash2': 20, 'cash3':30 , 'cash4':0 },
#     {'user_ID':5 , 'cash1':0 , 'cash2':20 , 'cash3':30 , 'cash4':40 },
#     {'user_ID':6 , 'cash1':0 , 'cash2':0 , 'cash3':30 , 'cash4':40 },
#     {'user_ID':7 , 'cash1':0 , 'cash2':0 , 'cash3':30 , 'cash4':40 },
#     {'user_ID':8 , 'cash1':0 , 'cash2':0 , 'cash3':0 , 'cash4':40 },
#     {'user_ID':9 , 'cash1':10 , 'cash2':0 , 'cash3':0 , 'cash4':40 },
#     {'user_ID':10 , 'cash1':10 , 'cash2':0, 'cash3':0 , 'cash4':40 }
#     ]

#     testtransactions = [
#     {'transaction_ID':1 , 'fromUser_ID':1 , 'toUser_ID':2 , 'value':10 , 'nameCash':'cash1' },
#     {'transaction_ID':2 , 'fromUser_ID':4 , 'toUser_ID':9 , 'value':5 , 'nameCash':'cash3' },
#     {'transaction_ID':3 , 'fromUser_ID': 10, 'toUser_ID':1 , 'value':5 , 'nameCash':'cash4' },
#     {'transaction_ID':4 , 'fromUser_ID': 10, 'toUser_ID':3 , 'value':10 , 'nameCash':'cash4' }
#     # {'transaction_ID':5 , 'fromUser_ID': , 'toUser_ID': , 'value': , 'nameCash': }
#     # {'transaction_ID':6 , 'fromUser_ID': , 'toUser_ID': , 'value': , 'nameCash': }
#     # {'transaction_ID':7 , 'fromUser_ID': , 'toUser_ID': , 'value': , 'nameCash': }
#     # {'transaction_ID':8 , 'fromUser_ID': , 'toUser_ID': , 'value': , 'nameCash': }
#     # {'transaction_ID':9 , 'fromUser_ID': , 'toUser_ID': , 'value': , 'nameCash': }
#     # {'transaction_ID':10 , 'fromUser_ID': , 'toUser_ID': , 'value': , 'nameCash': }
#     # {'transaction_ID':11 , 'fromUser_ID': , 'toUser_ID': , 'value': , 'nameCash': }
#     # {'transaction_ID':12 , 'fromUser_ID': , 'toUser_ID': , 'value': , 'nameCash': }
#     # {'transaction_ID':13 , 'fromUser_ID': , 'toUser_ID': , 'value': , 'nameCash': }
#     # {'transaction_ID':14 , 'fromUser_ID': , 'toUser_ID': , 'value': , 'nameCash': }
#     ]

#     with client:
#         db = client.tst_app
#         db.transaction.drop()
#         db.transaction.insert_many(testtransactions)
#         db.users.drop()
#         db.users.insert_many(users)
#         db.usersBackup.drop()

#         users_list = list(db.users.find())
#         df = pd.DataFrame(users_list)
#         print("cleanUpForTesting")
#         print(df)
#         print("------------------------------------------")