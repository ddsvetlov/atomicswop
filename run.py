# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)

from flask import Flask, render_template_string, request, flash, redirect, url_for, render_template
from flask_mongoengine import MongoEngine
from flask_user import login_required, UserManager, UserMixin, current_user
from apscheduler.schedulers.background import BackgroundScheduler
from snarkscript import snarkscript
import json
# change func print_date_time to custom func with isekai library TODO
scheduler = BackgroundScheduler()
scheduler.add_job(func=snarkscript, trigger="interval", seconds=10)
scheduler.start()



# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-MongoEngine settings
    MONGODB_SETTINGS = {
        'db': 'tst_app',
        'host': 'mongodb://localhost:27017/tst_app'
    }

    # Flask-User settings
    USER_APP_NAME = "Fucking app for transactions"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False      # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form


def create_app():
    """ Flask application factory """
    
    # Setup Flask and load app.config
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(__name__+'.ConfigClass')

    # Setup Flask-MongoEngine
    db = MongoEngine(app)


    # Define the User document.
    # NB: Make sure to add flask_user UserMixin !!!
    class User(db.Document, UserMixin):
        active = db.BooleanField(default=True)

        # User authentication information
        username = db.StringField(default='')
        password = db.StringField()

        # User information
        first_name = db.StringField(default='')
        last_name = db.StringField(default='')
        cash1 = db.IntField(default= 1)
        cash2 = db.IntField(default= 2)
        cash3 = db.IntField(default= 3)
        cash4 = db.IntField(default= 4)


        # Relationships
        roles = db.ListField(db.StringField(), default=[])

    class ExchangeOffer(db.Document):
        value1 = db.IntField(default= 0)
        value2 = db.IntField(default= 0)
        namecash1 = db.StringField(default= '')
        namecash2 = db.StringField(default= '')
        fromUserID = db.StringField(default= '')
        toUserID = db.StringField(default= '')
        
    class MultiOffer(db.Document):
        MOffer = db.ListField(db.StringField(), default=list)
        def addvalue(self, offer: ExchangeOffer):
            values = offer.split(",")
            for value in values:
                self.MOffer.append(value)

    class MultiTransaction(db.Document):
        MTrans = db.ListField(db.StringField(default=''))

    # class Transaction(db.Document):
    #     fromUser_ID = db.StringField(default= '')
    #     toUser_ID = db.StringField(default='')
    #     value = db.IntField(default= 0)
    #     nameCash = db.StringField(default= '')

    class OfferStatus(db.Document):
        Status = db.ListField(db.StringField(), default=list)
        UserID = db.ListField(db.StringField(), default=list)
        offerId = db.StringField(default = '')
        def addstatus(self, status):
            values = status.split(",")
            for value in values:
                self.Status.append(value)    
        def addid(self, status):
            values = status.split(",")
            for value in values:
                self.UserID.append(value)     
        
    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, User)

    # The Home page is accessible to anyone
    @app.route('/')
    def home_page():
        return render_template('home.html')

    @app.route('/transaction', methods=["POST"])
    def transaction_page():
        offer_id = request.form.get("offer_id")
        user_id = request.form.get("user_id")
        # fill status collection by user_id and transaction_id
        status = OfferStatus.objects.all()
        for stat in status:
            # find current offer
            if stat.offerId == offer_id:
                print(offer_id)
                print(stat.UserID)
                i=0
                # find and change status
                for elem in stat.UserID:
                    if elem == user_id:
                   
                        old_status = list(OfferStatus.objects(offerId=offer_id).get().Status)
                        old_status[i]='yes'
                        OfferStatus.objects(offerId=offer_id).update_one(set__Status=old_status)  
                    i+=1           
     
        # find accept all status order            
        old_status = list(OfferStatus.objects(offerId=offer_id).get().Status)
        for i in range(len(old_status)):
            if old_status[i]=='yes':
                if (i==len(old_status)-1 and old_status[i]=='yes'):
                # create multitransaction
                   moffer = MultiOffer.objects(pk=offer_id).get().MOffer
                   print('fuckfuck')
                   print(moffer)
                   print('fuckfuck')
                   multiTrans = MultiTransaction()
                   multiTrans.MTrans = moffer
                   multiTrans.save()
                # delete MultiOffer
                   MultiOffer.objects(pk=offer_id).delete()
                #    delete OfferStatus
                   OfferStatus.objects(offerId=offer_id).delete() 
                      
            else:
                break

        return render_template('transaction.html', offer_id = offer_id, user_id = user_id)
        

    @app.route('/offer', methods=["POST"])
    @login_required    # User must be authenticated
    def offer_page():
        values = []
        namecashes = []
        fromusers =[]
        tousers = []
        i=0
        j=1
        value = 'value'+ str(i)
        namecash = 'namecash' + str(i)
        fromuser = 'fromUserId' + str(j)
        touser = 'toUserId' + str(j)

        while (request.form.get(value) != None and request.form.get(namecash) != None):
            values.append(request.form.get(value))
            namecashes.append(request.form.get(namecash))
            i+=1
            print(i)
            value = 'value'+ str(i)
            namecash = 'namecash'+str(i)

        while (request.form.get(fromuser) != None and request.form.get(touser) != None):
            fromusers.append(request.form.get(fromuser))
            tousers.append(request.form.get(touser))
            j+=1
            print(j)
            fromuser = 'fromUserId' + str(j)
            touser = 'toUserId' + str(j)


        print(list(values))
        print(list(namecashes))
        print(list(fromusers))
        print(list(tousers))

        MultiOffer1 = MultiOffer()
        for item in range(len(fromusers)):
            str1 = values[item*2 ] + "," + values[item*2+1] + "," + namecashes[item*2] + "," + namecashes[item*2+1] + "," + fromusers[item] + "," + tousers[item]
            MultiOffer1.addvalue(str1)
            
        MultiOffer1.save()
        id = MultiOffer1.id
       

        print(MultiOffer.objects.values_list())
        OfferStatus1 = OfferStatus(offerId = str(id))
        for item in range(len(fromusers)):
            OfferStatus1.addstatus('no')
            OfferStatus1.addid(fromusers[item])
            OfferStatus1.addstatus('no')
            OfferStatus1.addid(tousers[item])
        OfferStatus1.save()


        return render_template ('offer.html', 
            fromUserId1 = request.form.get('fromUserId1'), toUserId1 = request.form.get('toUserId1'),
            value0 = request.form.get('value0'), value1 = request.form.get('value1'), value2 = request.form.get('value2'),
            namecash1 = request.form.get('namecash1'), namecash2= request.form.get('namecash2'), 
            fromUserId2 = request.form.get('fromUserId2'), toUserId2 = request.form.get('toUserId2'), 
            value3 = request.form.get('value3'), value4 = request.form.get('value4'), 
            namecash3 = request.form.get('namecash3'), namecash4= request.form.get('namecash4'), 
            fromUserId3 = request.form.get('fromUserId3'), toUserId3 = request.form.get('toUserId3'), 
            value5 = request.form.get('value5'), value6 = request.form.get('value6'), 
            namecash5 = request.form.get('namecash5'), namecash0 = request.form.get('namecash0'),namecash6= request.form.get('namecash6'))    
    

    # The Members page is only accessible to authenticated users via the @login_required decorator
    @app.route('/members')
    @login_required    # User must be authenticated
    def member_page():
        offers=[]
        offers = ExchangeOffer.objects.all()
        # TODO view transaction only for current user
        # transaction = Transaction.objects.all()
        mtransaction = []
        mtransaction = MultiTransaction.objects.all()
        # TODO view offer only for current user
        tut =[]
        of_id =[]
        offers1 = MultiOffer.objects.all()
        for offer in offers1:
            for elem in offer.MOffer:
                if str(elem) == str(current_user.id):
                    tut.append(offer.MOffer)
                    of_id.append(str(offer.id))
                    break
           
             
        return render_template("members.html", cash1=User.objects.get(pk = current_user.id).cash1,
                 cash2 = User.objects.get(pk = current_user.id).cash2,
                 cash3= User.objects.get(pk = current_user.id).cash3, 
                 cash4 = User.objects.get(pk = current_user.id).cash4,
                 OFFER = tut, offer_id = of_id, mtransaction=mtransaction)


    return app


# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
