from flask import *
import pymongo
from flask_session import Session
import random
import smtplib
from email.message import EmailMessage
import datetime
import re
import base64
from twilio.rest import Client


def new_uploaded(email,user_phone):
    sender_email = "chanleeip.4@gmail.com"
    sender_password = "akeiwvxfkcqttchq"
    receiver_email = email
    message_text = "A new file is uploaded .    if not you kindly acknowledge it to us."
    server = smtplib.SMTP('smtp.gmail.com', 587)
    
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email,receiver_email,message_text)

    account_sid = 'ACf3d301275aa863d7d816a4ce5643d03c'
    auth_token = '4737964cc2144e216bac2bee80bdcb25'
    client = Client(account_sid, auth_token)
    to_number = "+91"+user_phone
    from_number = '+17209244387'
    message = client.messages.create(
    body='A new file is uploaded .    if not you kindly acknowledge it to us.',
    from_="+17209244387",
    to=to_number
    )


    return 1



def otps(user_email, user_phone):
    new_otp = random.randint(100000, 999999)
    sender_email = "chanleeip.4@gmail.com"
    sender_password = "akeiwvxfkcqttchq"
    receiver_email = user_email
    message_text = f"The OTP is {new_otp}"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email,receiver_email,message_text)

    account_sid = 'ACf3d301275aa863d7d816a4ce5643d03c'
    auth_token = '4737964cc2144e216bac2bee80bdcb25'
    client = Client(account_sid, auth_token)
    to_number = "+91"+user_phone
    from_number = '+17209244387'
    message = client.messages.create(
    body='Your OTP is ' + str(new_otp)+' Please Donot share with anyone else',
    from_="+17209244387",
    to=to_number
    )

    return new_otp


def add_user():
    project_user.insert_one({"Name":session['cr_name'], "Email":session['cr_email'], "Phone":session['cr_phone'], "Password":session['cr_password'], "Gender":session['cr_gender'], "Role":'user'})
    return 1

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
   
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


project_server = pymongo.MongoClient('mongodb+srv://Naveen:Best2ismangodb@project1.y2jgh2e.mongodb.net/?retryWrites=true&w=majority')
project_db = project_server["LDMS"]
project_user = project_db["users"]
project_document = project_db["document"]
project_home_ad = project_db["homeads"]


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
sess = Session()

@app.route('/',methods=['GET','POST'])
def home():
    msg = ""
    image_display=[]
    all_image_doc = project_home_ad.find()
    for image in all_image_doc:
        image_data = image['file']
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        image_display.append(image_b64)
    return render_template('home.html',msg=msg, image_data=image_display)


@app.route('/signin',methods=['GET','POST'])
def signin():
    msg=" "
    if request.method == 'POST':
        details = request.form 
        name = details['username']
        password = details['password']
        user = project_user.find_one({"$or":[{'Name':name,'Password':password},{'Phone':name,'Password':password}]})
        if user:
            session['name'] = user['Name']
            session['role'] = user['Role']
            session['email'] = user['Email']
            session['phone'] = user['Phone']
            return redirect('/dashboard')
        else:
            msg = "Password you entered is wrong"
    return render_template('signin.html',msg=msg)

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        details = request.form
        # name 
        name = details['cr_name']
        session['cr_name'] = details['cr_name']
        # Password
        password = details['cr_password']
        session['cr_password'] = details['cr_password']
        # Gender
        gender = details['cr_gender']
        session['cr_gender'] = details['cr_gender']
        # Dob
        # dob = details['cr_dob']
        # session['cr_dob'] = details['cr_dob']
        # Email
        phone = details['cr_phone']
        session['cr_phone'] = details['cr_phone']
        email = details['cr_email']
        session['cr_email'] = details['cr_email']
        session['otp'] = otps(session['cr_email'],phone)
        # Phone
        
        return redirect('/signupotp')
    return render_template('signup.html')

@app.route('/signupotp',methods=['GET','POST'])
def signupotp():
    msg = ""
    if request.method == 'POST':
        details = request.form 
        cr_otp = details['cr_otp']
        if session['otp'] == int(cr_otp):
            msg = "Registered Successfully"
            add_user()
            return redirect('/signin')
        else:
            msg="wrong OTP"
    return render_template('Otp_page.html',msg=msg)

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    # names = project_user.find({"Name":session['name']})
    # profile_pic = None
    # for user in names:
    #     if 'Profile_pic' in user:
    #         profile_pic = Response(user['Profile_pic'], mimetype="image/jpg")
    #         break
    # docs = project_document.find({"Name":session['name']})
    # return render_template('dashboard.html',users=names,docs=docs,pic = profile_pic)
    names = project_user.find({"Name":session['name']})
    docs = project_document.find({"Name":session['name']})
    return render_template('dashboard.html',users=names,docs=docs)


@app.route('/upload_file',methods=['GET','POST'])
def upload_file():
    if request.method == "POST":
        name = request.form['name']
        file = request.files["pdf_file"]
        discription = request.form["file_desc"]
        pdf_binary = file.read()
        pdf_data = {"Name":session['name'],"name":name, "data": pdf_binary, "Discription":discription, "date": datetime.datetime.utcnow()} #, "ext" : file_extension
        result = project_document.insert_one(pdf_data)
        new_uploaded(session['email'],session['phone'])
        return redirect('/dashboard')
    return render_template('upload_file.html')


@app.route('/preview_file/<string:id>', methods=['GET', 'POST'])
def preview_file(id):
    pdf_data = project_document.find_one({"name":id})  #{"Name":session['name']}
    return Response(pdf_data["data"], mimetype="image/jpg")
# , mimetype="image/jpg"

@app.route('/delete_file/<string:id>', methods=['GET', 'POST'])
def delete_file(id):
    project_document.delete_one({"name": id})
    return redirect('/dashboard')

@app.route('/homeads',methods=['GET','POST'])
def homeads():
    if request.method == "POST":
        name = request.form['file_name']
        file = request.files["pdf_file"]
        discription = request.form["file_desc"]
        pdf_binary = file.read()
        data = { "name": name , "file":pdf_binary , "discription" : discription,  "date": datetime.datetime.utcnow() }
        project_home_ad.insert_one(data)
        return redirect('/dashboard')
    return render_template('/upload_home.ad.html')

@app.route('/delete_homeads/<string:id>',methods=['GET','POST'])
def delete_homeads(id):
    project_home_ad.delete_one({"name": id})
    return redirect('/')

@app.route('/logout')
def logout():
    session['name'] = None 
    session['role'] = None 
    return redirect('/')  


@app.route('/users',methods=['GET','POST'])
def users():
    all_users = project_user.find()
    return render_template('users.html',users = all_users)

if __name__=='__main__':
    app.run(debug=True)