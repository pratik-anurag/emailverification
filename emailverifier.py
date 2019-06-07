from pymongo import MongoClient
import pprint
import quickemailverification
client = MongoClient('mongodb://localhost:27017/') 
db = client['dbname']
cm = db['collectionname']
#TODO:- create an array of tokens and fetch the array index to validate multiple records
token = 'API TOKEN'
count= 0 
verified_col = { "$set": { "isvalid": "true", "verified": "true" } }
unverified_col = { "$set": { "isvalid": "false", "verified": "false" } }
client = quickemailverification.Client(token)
quickemailverification = client.quickemailverification()
for c in cm.find({'$or':[{'isvalid':{'$exists':False}},{'isvalid':'false'}]},{'email':1,'_id':0}):
    if(c['email']!=''):
        #print(c['email']) ## call wrapper api to validate the email, if email is verified then do the flag changes, add/update flag for c['id']
        response = quickemailverification.verify(c['email'])
        if(response.body['result']!= 'invalid'):
            # print(c['email']+' is '+response.body['result'])
            # print('----------------------------------------')
            # print('updating the collection with flags isvalid as true')
            cm.update_one({'email':c['email']}, verified_col)
        else:
            # print('----------------------------------------')
            # print('updating the collection with flags isvalid as false')
            cm.update_one({'email':c['email']}, unverified_col)
            # print(c['email']+' is '+response.body['result'])
    else:
        pass #email is null
