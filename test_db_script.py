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
        # fromCash = []
        # toCash = []   
        transaction = [] 
        # fromCashBack = []
        # toCashBack = []
        
        transac = db.multi_transaction.find_one({'_id': IDs })['MTrans']
        j= 0
        for item in range(0,len(transac),6):
            value1.append(transac[item])
            value2.append(transac[item+1])
            namecash1.append(transac[item+2])
            namecash2.append(transac[item+3])
            fromUser.append(transac[item+4])
            toUser.append(transac[item+5])
            
            # us = db.user.find_one( {'_id': ObjectId(fromUser[j]) })
            
            # fromCash.append(us[namecash1[j]])
            # fromCashBack.append(us[namecash2[j]])
            
            # us = db.user.find_one( {'_id': ObjectId(toUser[j]) })
            # toCash.append(us[namecash1[j]])
            # toCashBack.append(us[namecash2[j]])
        
            transaction.append(fromUser[j])
            transaction.append(toUser[j])
            # transaction.append(fromCash[j])
            # transaction.append(toCash[j])
            transaction.append(value1[j])
            transaction.append(namecash1[j])

            transaction.append(toUser[j])
            transaction.append(fromUser[j])
            # transaction.append(toCashBack[j])
            # transaction.append(fromCashBack[j])
            transaction.append(value2[j])
            transaction.append(namecash2[j])
            j+=1
         
    return(transaction)

def getWallet(userFromID,cashId):
    #connect to db
    client = pymongo.MongoClient('mongodb://localhost:27017/')

    #make smth with db
    with client:

        db = client.tst_app
        us = db.user.find_one( {'_id': ObjectId(userFromID) })
    
    return (us[cashId])




def updateDB(fromCash, toCash, fromID, toID, cashID):
    print('update data')
    print(fromCash, toCash, fromID, toID, cashID)
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    with client:
        db = client.tst_app
        db.user.update_one({'_id': ObjectId(fromID)}, {'$set': {cashID : int(fromCash)}})
        db.user.update_one({'_id': ObjectId(toID)}, {'$set': {cashID : int(toCash)}})
    # users_list = list(db.user.find())
    # df = pd.DataFrame(users_list)
    # print(df)
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