
import pyodbc
from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)

server = 'khalibsql.database.windows.net'
database = 'KSUGradeDB'
username = 'kmorton'
password = '{Administrator!}'
driver= '{ODBC Driver 17 for SQL Server}'


fileout = open("templates/results.html", "w")



def getAvg(data):
    values = []
    for numbers in data: 
        values.append(numbers[1])
    
    
    sum = 0; 
    for num in values: 
        sum += num
    
    return sum/len(values)
#Flask 
@app.route('/index', methods = ['POST', 'GET'])
def index(): 
    if request.method == 'POST': 
        form_class = request.form['class']
        form_grade = request.form['grade']
        return redirect(url_for('send_data', classid = form_class, grade = form_grade))
    else:
        return redirect(url_for('display_data'))

@app.route('/send_data/<classid>/<grade>')
def send_data(classid, grade): 
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO CLASS(id, grade) VALUES (?, ?)",(str(classid), grade))

    return redirect(url_for('index'))

@app.route('/display_data')
def display_data():
    colNames = []
    db_data = []
    html_data = []
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
     with conn.cursor() as cursor:
        cursor.execute("SELECT CLASS.ID, CLASS.GRADE FROM CLASS")
        #Return Data
        for row in cursor.fetchall(): 
            db_data.append(row)

        #Get Row Names
        table = cursor.columns(table = "CLASS")
        for row in table:
            colNames.append(row.column_name)
        
    colNames = ','.join(colNames)
    #Create HTML Table
    html_table = "<table>\n"
    header = colNames.split(',')
    html_table += "  <tr>\n"
    for column in header:
        html_table +="   <th>{0}</th>\n".format(column.strip())
    html_table += "  </tr>\n"

    #Add Data
    for data in db_data:
        html_table += "  <tr>\n"
        html_table += "  <td>{0}</td>\n".format(data[0])
        html_table += "  <td>{0}</td>\n".format(data[1])

    html_table += "  <tr>\n"
    html_table += " <td>Average</td>\n"
    html_table += " <td>{0}</td>\n".format(getAvg(db_data))

    html_table += '<style>\n'
    html_table+= '  table, th, td {\n'
    html_table +='  border: 1px solid white;\n'
    html_table += ' border-collapse: collapse; }\n'
    html_table += 'th, td {\n'
    html_table += ' background-color: #96D4D4; }\n'
    html_table += '</style>\n'

    html_table += "</table>\n"
    fileout.writelines(html_table)
    fileout.close()

    return render_template('results.html')
if __name__ == '__main__':
    app.run(debug = True)
