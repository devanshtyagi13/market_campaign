from flask import Flask, render_template, request
import oracledb
import random
from faker import Faker
 
 
app = Flask(__name__)
faker = Faker()
 
def get_db_connection():
    # Update these values with your actual database credentials
    dsn = 'localhost:1521/xepdb1'
    conn = oracledb.connect(user="dbuser", password="dbuser", dsn=dsn)
    return conn
 
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
 
    cursor.execute("SELECT table_name FROM user_tables")
 
    tables = [row[0] for row in cursor.fetchall( )]
    cursor.close()
    conn.close()
    return render_template('base.html', tables = tables)
 
 
@app.route('/filtered_customers1')
def filtered_customers1():
    conn = get_db_connection()
    cursor = conn.cursor()
    table='customer_bank_details'
    table2='customer_campaign_data'
    cursor.execute(f"SELECT * FROM {table} INNER JOIN {table2} USING(customer_id) where {'loan'} =: x and {'campaign'}> 2", {'x':'yes'})
    row=cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return render_template('filtered_customers1.html', columns=columns,rows=row)
 
@app.route('/filtered_customers2')
def filtered_customers2():
    conn = get_db_connection()
    cursor = conn.cursor()
    table='customer_bank_details'
    table2='customer_campaign_data'
    cursor.execute(f"select * from {table} INNER JOIN {table2} USING(customer_id) where {'campaign'} >2 and {'poutcome'} ='success'")
    row=cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data=[]
    for i in row:
        con_list=list(i)
        data1=dict(zip(columns,con_list))
        data.append(data1)
    return render_template('filtered_customers2.html', filtered_customers=data,columns=columns,rows=row)
 
@app.route('/filtered_customers3')
def filtered_customers3():
    conn = get_db_connection()
    cursor = conn.cursor()
    table='customer_bank_details'
    table2='customer_campaign_data'
    cursor.execute(f"select * from {table} INNER JOIN {table2} USING(customer_id) where {'campaign'} >2 and {'poutcome'} ='failure' and {'month'}='jun' ")
    row=cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data=[]
    for i in row:
        con_list=list(i)
        data1=dict(zip(columns,con_list))
        data.append(data1)
    return render_template('filtered_customers3.html', filtered_customers=data,columns=columns,rows=row)
 
@app.route('/filtered_customers4')
def filtered_customers4():
    conn = get_db_connection()
    cursor = conn.cursor()
    table='customer_bank_details'
    table2='customer_campaign_data'
    cursor.execute(f"select state_code,count(Customer_id) from {table} group by {'state_code'} order by {'state_code'}")
    row=cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data=[]
    for i in row:
        con_list=list(i)
        data1=dict(zip(columns,con_list))
        data.append(data1)
    return render_template('filtered_customers4.html', filtered_customers=data,columns=columns,rows=row)
 
@app.route('/getDetails')
def getDetails():
    return render_template('name.html')
 
@app.route('/details',methods=['POST'])
def search(table='customer_details'):
    conn = get_db_connection()
    cursor = conn.cursor()
    customer_id = request.form.get('customer_id')
    #print(customer_name)
    row_id='Customer_id'
    cursor.execute(f"SELECT * FROM {table} WHERE {row_id}= :row_id", {'row_id':customer_id})
    row=cursor.fetchone()
    columns = [desc[0] for desc in cursor.description]
    row=list(row)
    dic=dict(zip(columns,row))
    print(dic)
    return render_template('display.html',columns_rows=dic)
 
if __name__ == '__main__':
    app.run(debug=True)
