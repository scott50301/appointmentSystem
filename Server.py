from flask import Flask, render_template, request, jsonify;
from flask_sqlalchemy import SQLAlchemy;
import sys;
import MySQLdb

con = "";
    
    
app = Flask(__name__);


f = open(r'./dbinformation.dat')
account = ""
pwd = ""
ip = ""
port = ""
db = ""
for line in f:
    x = line.split(":")
    if x[0] == "account":
        account = x[1].strip()
    elif x[0] == "password":
        pwd = x[1].strip()
    elif x[0] == "ip":
        ip = x[1].strip()
    elif x[0] == "port":
        port = x[1].strip()
    elif x[0] == "db":
        db = x[1].strip()
        
f.close()
con = "mysql+pymysql://"+account+":"+pwd+"@"+ip+":"+port+"/"+db;
#print(con, file=sys.stderr);
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
app.config['SQLALCHEMY_DATABASE_URI'] = con;

db = SQLAlchemy(app);
  
@app.route('/')
def index():
  
    #return 'ok'
    return render_template('index.html');

@app.route('/getAvail', methods= ["POST"])
def getAvail():

    sql_cmd = "UPDATE timeslots SET status = 0 WHERE status = 2 AND timeout < NOW()";
    db.engine.execute(sql_cmd);
    
    sql_cmd = "SELECT slots, status FROM timeslots WHERE `date` ='"+request.form['date']+"'";
    #print(sql_cmd, file=sys.stderr);
    query_data = db.engine.execute(sql_cmd);
    result = query_data.fetchall()

    d, a = {}, []
    for rowproxy in result:
        i = 0
        for column, value in rowproxy.items():
            # build up the dictionary
            if i%2==0:
                value = str(value);
            d = {**d, **{column: value}}
        a.append(d)
    #print(a, file=sys.stderr);
    
    return jsonify(res = a)

@app.route('/update', methods= ["POST"])
def update():
    sql_cmd = "SELECT status FROM timeslots WHERE `date` ='"+request.form['date']+"' AND slots ='"+request.form['time']+"'";
    res = db.engine.execute(sql_cmd).fetchone();
    if res[0] == 1:
        return "Oops someone has already maken the appointment!"
    sql_cmd = "UPDATE timeslots SET status = 2, timeout = DATE_ADD(NOW(), INTERVAL 15 MINUTE) WHERE `date` ='"+request.form['date']+"' AND slots ='"+request.form['time']+"'";
    print(sql_cmd, file=sys.stderr);
    db.engine.execute(sql_cmd);
   
    if request.form['pre'] != -1:
        sql_cmd = "UPDATE timeslots SET status = 0 WHERE `date` ='"+request.form['date']+"' AND slots ='"+request.form['pre']+"'";
        db.engine.execute(sql_cmd);
        print(sql_cmd, file=sys.stderr);
        
    return "success"

@app.route('/submit', methods= ["POST"])
def submit():
    sql_cmd = "SELECT status FROM timeslots WHERE `date` ='"+request.form['date']+"' AND slots ='"+request.form['time']+"'";
    print(sql_cmd, file=sys.stderr);
    res = db.engine.execute(sql_cmd).fetchone();
    if res[0] == 1:
        return "Oops someone has already maken the appointment!"

    sql_cmd = "UPDATE timeslots SET status = 1 WHERE `date` ='"+request.form['date']+"' AND slots ='"+request.form['time']+"'";
    
    db.engine.execute(sql_cmd);
        
    return "success"

if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0');