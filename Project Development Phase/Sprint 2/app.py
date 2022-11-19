from flask import Flask,render_template, request, redirect, url_for, session

import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cly12872;PWD=9Xh8GywCiKnJXHUL",'','')

app = Flask(__name__)

@app.route("/")
def log():
    return render_template('index.html')

@app.route("/logi")
def logi():
  return render_template('login.html', name="login")


@app.route('/register',methods = ['POST'])
def register():
  if request.method == 'POST':

    name = request.form['username']
    emailid = request.form['email']
    password = request.form['password']
    repassword = request.form['repassword']
    contact = request.form['contact']
    role=request.form['role']
 
    sql = "SELECT * FROM login WHERE emailid =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,emailid)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('login.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO login VALUES (?,?,?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, emailid)
      ibm_db.bind_param(prep_stmt, 3, password)
      ibm_db.bind_param(prep_stmt, 4, repassword)
      ibm_db.bind_param(prep_stmt, 5, contact)
      ibm_db.bind_param(prep_stmt, 6, role)
      ibm_db.execute(prep_stmt)
    
    return render_template('login.html', msg="Data saved successfuly..Please login using your details")

@app.route('/login',methods=['POST'])
def login():
  
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    sql = "SELECT * FROM login WHERE emailid =? AND password=? AND role=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,password)
    ibm_db.bind_param(stmt,3,role)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print(account)
    print(account['ROLE'])
    print(account['ROLE'].strip())
    if (account['ROLE'].strip()=="user"):
            return render_template('user.html') 
    elif(account['ROLE'].strip()=="agent"):
            return render_template('agent.html') 
    elif(account['ROLE'].strip()=="admin"):
            return render_template('admin.html') 
    else:
        return render_template('login.html', msg="Login unsuccessful. Incorrect username / password !") 



@app.route('/usercomplaint',methods=['POST'])
def usercomplaint():
  if request.method == 'POST':
  
    name = request.form['name']
    item = request.form['itemname']
    dateofpurchase= request.form['dateofpurchase']
    complaint = request.form['complaint']
    print("i am in usercomplaint")

    if(name!=""):

            insert_sql = "INSERT INTO complaint VALUES (?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, item)
            ibm_db.bind_param(prep_stmt, 3, dateofpurchase)
            ibm_db.bind_param(prep_stmt, 4, complaint)
            ibm_db.execute(prep_stmt)
    
    return render_template('user.html', msg="Data saved successfuly..Please login using your details")


    

@app.route("/about")
def about():
  return render_template('about.html', name="About")


@app.route("/contact")
def contact():
  return render_template('contact.html', name="Contact")


if __name__ == "__main__":
    app.run(debug=True)
