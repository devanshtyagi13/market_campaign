from flask import Flask, render_template, request
import oracledb
# import requests
 
app = Flask(__name__)
 
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
    return render_template('index.html', tables = tables)
   
@app.route('/table/<table_name>')
def view_table(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM user_tables")
    query = f"SELECT * FROM {table_name}"
 
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return render_template('info.html', column_names= columns, rows=rows,table_name=table_name)
 
 
@app.route('/edit/<table_name>/<string:row_id>', methods=['GET', 'POST'])
def edit_row(table_name, row_id):
    if request.method == 'POST':
        # Process form submission and update row in the database
        connection = get_db_connection()
        cursor = connection.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        update_query = f"UPDATE {table_name} SET "
        update_params = []
        for key, value in request.form.items():
            if key != 'submit':
                column_name = key
                update_query += f"{column_name} = :{column_name}, "
                update_params.append(value)
        update_query = update_query.rstrip(', ') + f" WHERE {columns[0]} = '{row_id}'"
        '''print(update_query)
        print(update_params)'''
        cursor.execute(update_query, update_params)
        connection.commit()
        cursor.close()
       
        return('/')
   
    # Fetch row data for editing
    connection = get_db_connection()
    cursor = connection.cursor()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    index_row=columns[0]
    cursor.close()  
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name} WHERE {index_row} = :row_id", {'row_id': row_id})
    row = cursor.fetchone()
    cursor.close()
    row=list(row)
    dic=dict(zip(columns,row))
    return render_template('edittable.html', table_name=table_name, dic=dic)
 
if __name__ == '__main__':
    app.run(debug=True)