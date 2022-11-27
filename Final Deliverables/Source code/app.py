from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape
import requests
import json

import ibm_db


conn=ibm_db.connect('DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=yjz09746;PWD=hcHm34Z40BI3Jgy7','','')

print("Connected Successfully !")

app = Flask(__name__)

app.secret_key = 'Done ehhh'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route("/registerrec",methods = ['POST', 'GET'])
def registerrec():
    msg=''
    if request.method == 'POST':

        name = request.form['name']
        number = request.form['number']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM register WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)

        if account:
            return render_template('login.html', msg="You are already a member, please login using your details")
        else:
        
            insert_sql = "INSERT INTO register VALUES (?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, number)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.execute(prep_stmt)
    
        return render_template('login.html', msg="Registered successfuly..login to continue")
#Login

@app.route("/loginrec", methods =['POST','GET'])
def loginrec():
    smsg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        if((email and password) is not None ):
            sql = "SELECT * FROM register WHERE email = ?"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt,1,email)
            prep_stmt = ibm_db.execute(stmt)
            dicto = ibm_db.fetch_assoc(stmt)
            while(dicto != False):
                res1 = dicto["EMAIL"]
                res2 = dicto['PASSWORD']
                res3 = dicto['NAME']
                res4 = dicto['NUMBER']

                if(res1 == email and res2 == password):
                    session['email'] = res1
                    session['pass'] = res2
                    session['name'] = res3
                    session['number'] = res4
                    return render_template('profile.html')
                else:
                    return render_template('login.html', smsg = 'Incorrect username / password !')
            else:
                return render_template('register.html', smsg = 'Not yet registered')
        else:   
            return render_template('login.html', smsg = 'Fill all the details')
    else:
        return render_template('login.html')
            
#contac

@app.route("/jobsrec",methods = ['POST', 'GET'])
def jobsrec():
    jmsg=''

    if request.method == 'POST':
    
        CandidateName = request.form['CandidateName']
        CompanyName = request.form['CompanyName']
        EmployeeRole = request.form['EmployeeRole']
        CandidateMail = request.form['CandidateMail']
        CandidateNumber = request.form['CandidateNumber']
        insert_sql = "INSERT INTO hirerform VALUES (?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, CandidateName)
        ibm_db.bind_param(prep_stmt, 2, CompanyName)
        ibm_db.bind_param(prep_stmt, 3, EmployeeRole)
        ibm_db.bind_param(prep_stmt, 4, CandidateMail)
        ibm_db.bind_param(prep_stmt, 5, CandidateNumber)
        ibm_db.execute(prep_stmt)
    
        return render_template('jobs.html', jmsg="Registered successful!! and We will contact you soon")

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/exploreJobs', methods = ['GET', 'POST'])


def exploreJobs():
	url = "https://indeed11.p.rapidapi.com/"
	payload = {
		"search_terms": "marketing",
		"location": "United States",
		"page": "1"
	}
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": "be7fd5b032msh2de06b9e53f0850p1ce4b9jsna154c022de5a",
		"X-RapidAPI-Host": "indeed11.p.rapidapi.com"
	}

	response = requests.request("POST", url, json=payload, headers=headers)
	#print(response.text)
	job = json.loads(response.content)
	print(job) 
	a=job
    #print(a)
    #json_data = json.loads(job)
	return render_template('exploreJobs.html', jobs =job)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('email', None)
   session.pop('password', None)
   session.pop('name', None)
   session.pop('number', None)
   # Redirect to login page
   return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True) 

    
