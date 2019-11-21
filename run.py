# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)

from flask import Flask, render_template_string, request, flash, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_user import login_required, UserManager, UserMixin, current_user
from apscheduler.schedulers.background import BackgroundScheduler
from snarkscript import snarkscript
# change func print_date_time to custom func with isekai library TODO
# scheduler = BackgroundScheduler()
# scheduler.add_job(func=snarkscript, trigger="interval", seconds=10)
# scheduler.start()



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
    app = Flask(__name__)
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
    class MultiOffer(db.EmbeddedDocument):
        MOffer = db.ListField(db.EmbeddedDocumentField(ExchangeOffer))
        def addvalue(self, offer: ExchangeOffer):
            self.MOffer.append(offer)

    class ExchangeOffer(db.EmbeddedDocument):
        value1 = db.IntField(default= 0)
        value2 = db.IntField(default= 0)
        namecash1 = db.StringField(default= '')
        namecash2 = db.StringField(default= '')
        fromUserID = db.StringField(default= '')
        toUserID = db.StringField(default= '')
        
    # ExchangeOffer1 = ExchangeOffer(value1 = 1, value2 = 2, namecash1= 'cash1', namecash2= 'cash2')
    # ExchangeOffer1.save()
    # ExchangeOffer2 = ExchangeOffer(value1 = 3, value2 = 4, namecash1= 'cash3', namecash2= 'cash4')
    # ExchangeOffer2.save()


    class MultiTransaction(db.Document):
        MTrans = db.ListField(db.StringField(default=''))

    class Transaction(db.Document):

        fromUser_ID = db.StringField(default= '')
        toUser_ID = db.StringField(default='')
        value = db.IntField(default= 0)
        nameCash = db.StringField(default= '')
        


    # Transaction1 = Transaction(fromUser_ID='1', toUser_ID='2', value=1, nameCash='cash1')
    # Transaction1.save()
    # Transaction2 = Transaction(fromUser_ID='2', toUser_ID='1', value=2, nameCash='cash2')
    # Transaction2.save()
    # Transaction.
    # Transaction1.cash1 = '10'
    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, User)

    # The Home page is accessible to anyone
    @app.route('/')
    def home_page():
        # String-based templates
        return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>Home page</h2>
                <p><a href={{ url_for('user.register') }}>Register</a></p>
                <p><a href={{ url_for('user.login') }}>Sign in</a></p>
                <p><a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)</p>
                <p><a href={{ url_for('member_page') }}>Member page</a> (login required)</p>
                <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
            {% endblock %}
            """)
    @app.route('/transaction', methods=["POST"])
    def transaction_page():
        # if somebody accept the exchange offer we create 2 transactions
        Transaction1 = Transaction(fromUser_ID = ExchangeOffer.objects.get(pk=request.form.get("offer_id")).fromUserID,
                                    toUser_ID =  str(current_user.id) ,
                                    value = ExchangeOffer.objects.get(pk=request.form.get("offer_id")).value1,
                                    nameCash = ExchangeOffer.objects.get(pk=request.form.get("offer_id")).namecash1)
        Transaction1.save()
        Transaction2 = Transaction( toUser_ID = ExchangeOffer.objects.get(pk=request.form.get("offer_id")).fromUserID,
                                    fromUser_ID = str(current_user.id),
                                    value = ExchangeOffer.objects.get(pk=request.form.get("offer_id")).value2,
                                    nameCash = ExchangeOffer.objects.get(pk=request.form.get("offer_id")).namecash2)
        Transaction2.save()                                    
        return render_template_string("""
            {% block content %}
            <h1>Your accept changing</h1>
            <area>change {{details}} of {{details2}} </area>
            <area> to {{details1}} of {{details3}}</area><br />
            <h1>Go to member page to make another changing</h1>
            {% endblock %}
            """, details = ExchangeOffer.objects.get(pk=request.form.get("offer_id")).value1,
            details1 = ExchangeOffer.objects.get(pk=request.form.get("offer_id")).value2,
            details2 = ExchangeOffer.objects.get(pk=request.form.get("offer_id")).namecash1,
            details3 = ExchangeOffer.objects.get(pk=request.form.get("offer_id")).namecash2
            )

        

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

        MultiTransaction1 = MultiTransaction
        for item in range(len(fromusers)):
            ExchangeOffer1 = ExchangeOffer( value1 = values[item*2 ],
                                            value2 = values[item*2+1],
                                            namecash1 = namecashes[item*2],
                                            namecash2 = namecashes[item*2+1],
                                            fromUserID = fromusers[item],
                                            toUserID = tousers[item])
            ExchangeOffer1.save()
            str1 = values[item*2 ] + "," + values[item*2+1] + "," + namecashes[item*2] + "," + namecashes[item*2+1] + "," + fromusers[item] + "," + tousers[item]
            MultiTransaction1.addvalue(ExchangeOffer1)

            print('blablabla', item)
        



        # ExchangeOffer1 =ExchangeOffer(value1 = request.form.get("value1"),
        #                               value2 = request.form.get('value2'),
        #                               namecash1 = request.form.get('namecash1'),
        #                               namecash2= request.form.get('namecash2'))
        # ExchangeOffer1.save()                              
        # return redirect("/members") 
        return render_template_string ("""
            {% block content %}
            <area> offer </area><br/>
            <area> {{fromUserId1}} {{toUserId1}} {{value0}} {{value1}} {{namecash0}} {{namecash1}} </area><br/>
            <area> {{fromUserId2}} {{toUserId2}} {{value2}} {{value3}} {{namecash2}} {{namecash3}} </area><br/>
            <area> {{fromUserId3}} {{toUserId3}} {{value4}} {{value5}} {{namecash4}} {{namecash5}} </area><br/>
           
            {% endblock %}
            """, fromUserId1 = request.form.get('fromUserId1'), toUserId1 = request.form.get('toUserId1'),
             value0 = request.form.get('value0'), value1 = request.form.get('value1'), value2 = request.form.get('value2'), namecash1 = request.form.get('namecash1'), namecash2= request.form.get('namecash2'), fromUserId2 = request.form.get('fromUserId2'), toUserId2 = request.form.get('toUserId2'), value3 = request.form.get('value3'), value4 = request.form.get('value4'), namecash3 = request.form.get('namecash3'), namecash4= request.form.get('namecash4'), fromUserId3 = request.form.get('fromUserId3'), toUserId3 = request.form.get('toUserId3'), value5 = request.form.get('value5'), value6 = request.form.get('value6'), namecash5 = request.form.get('namecash5'), namecash0 = request.form.get('namecash0'),namecash6= request.form.get('namecash6'))
            
        

        



    # The Members page is only accessible to authenticated users via the @login_required decorator
    @app.route('/members')
    @login_required    # User must be authenticated
    def member_page():
        offers = ExchangeOffer.objects.all()
        transaction = Transaction.objects.all()
        print(offers[0].value1)
        # String-based templates
        return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                
                <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.js"></script>
                <h2>Members page</h2>

                {% for flash_message in get_flashed_messages() %}
                    <h1>{{flash_message}}</h1>
                {% endfor %}
                <h1>Your cash is:</h1>
                <area>cash1={{  cash1}}<br /> cash2={{cash2}}<br /> cash3={{cash3}}<br /> cash4={{cash4}}</area>
                <h1>Offer your exchange:</h1>
                <button onclick = "hello()"> +++ </button>
                <form action="/offer" method="POST" class = "newTransaction">
                <div id = "1">
                  
                    <area> From User Id </area>                 
                    <input type="text" name="fromUserId1">  
                    <area> Value </area>       
                    <input type="text" name="value0">
                    <select id="3" name="namecash0">
                        <option>cash1</option>
                        <option>cash2</option>
                        <option>cash3</option>
                        <option>cash4</option>
                    </select> 
                    <area> To User Id </area> 
                    <input type="text" name="toUserId1">
                    <area> From User Id </area> 
                    <input type="text" name="value1">
                    <select id="4" name="namecash1" >
                        <option>cash1</option>
                        <option>cash2</option>
                        <option>cash3</option>
                        <option>cash4</option>
                    </select>
                    
                    <br/ >  
                </div>
                <button type="submit">add this shit</button><br/>
                </form>



                <script>
                    const ValueId = createId();
                    const NamecashId = createId();
                    const FromUserId = createId();
                    const ToUserId = createId();
                        function createId(){
                            var val =1;
                            return function() {
                                return ++val;
                            }
                        }
                        function tmp () { 
                            return `
                                
                                <area> From User Id </area>                 
                                <input type="text" name="fromUserId${FromUserId()}">  
                                <area> Value </area>       
                                <input type="text" name="value${ValueId()}">
                                <select id="3" name="namecash${NamecashId()}">
                                    <option>cash1</option>
                                    <option>cash2</option>
                                    <option>cash3</option>
                                    <option>cash4</option>
                                </select> 
                                <area> To User Id </area> 
                                <input type="text" name="toUserId${ToUserId()}">
                                <area> From User Id </area> 
                                <input type="text" name="value${ValueId()}">
                                <select id="4" name="namecash${NamecashId()}" >
                                    <option>cash1</option>
                                    <option>cash2</option>
                                    <option>cash3</option>
                                    <option>cash4</option>
                                </select>
                                
                                
                                <br/>`;
                                }

                function hello () {
                   document.getElementById("1").innerHTML += tmp()
                }
                
                </script>            


              
                <h1>You can make those change:</h1>
                {%for item in offers%}
                <form action="/transaction" method="POST">
                    <input type="hidden" value="{{ item.id }}" name="offer_id">
                    <span>exchange: {{ item.value1 }} {{ item.namecash1 }} to: {{ item.value2 }} {{ item.namecash2 }}</span>
                    <button type="submit">fuck this shit</button><br/ >
                </form>
                {% endfor %}   

                <h1>Transaction on stack:</h1>
                {%for item in transaction%}
                    <span> fromUser_ID  {{ item.fromUser_ID }} toUser_ID  {{ item.toUser_ID }} value {{ item.value }} namecash {{ item.nameCash }}</span><br />
                {% endfor %}    

                <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
            {% endblock %}
            """, cash1=User.objects.get(pk = current_user.id).cash1,
                 cash2 = User.objects.get(pk = current_user.id).cash2,
                 cash3= User.objects.get(pk = current_user.id).cash3, 
                 cash4 = User.objects.get(pk = current_user.id).cash4,
                 offers = offers, transaction = transaction)


    return app


# Start development web server
if __name__=='__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
