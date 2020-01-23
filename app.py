from flask import Flask, request, jsonify
import mysql.connector
import logging

logging.getLogger().setLevel(logging.DEBUG)
app = Flask(__name__)


class Mysql_connection():
    connection = None
    def __init__(self):
        self.root = 'root'
        self.host = 'localhost'
        self.password = ''
        self.database = 'Student_marks'

        if Mysql_connection.connection is None:
            Mysql_connection.connection = mysql.connector.connect(
                user=self.root,
                password=self.password,
                host=self.host,
                database=self.database
            )

    def get_data(self, sql_query):
        cur = Mysql_connection.connection.cursor()
        cur.execute(sql_query)
        rows = cur.fetchall()
        return rows


logging.error("starting con")


@app.route('/')
def index():
    try:
        mysql_connection = Mysql_connection()
        student_id = request.args.get('student_id')
        subject_id = request.args.get('subject_id')
        class_id = request.args.get('class_id')

        if student_id:
            rows = mysql_connection.get_data(f"select * from mst_student where student_id={student_id}")
        elif subject_id:
            rows = mysql_connection.get_data(
               f"select * from mst_student where subject_id={subject_id}")

        elif class_id:
            rows = mysql_connection.get_data(
                f"select * from mst_student where class_id={class_id}")
        else:
            resp = jsonify({'error': 'User "id" not found in query string'})
            resp.status_code = 500
            return resp
        logging.error(rows)

        resp = jsonify({'ID': rows[0][0], 'Name': rows[0][1],'ClassId': rows[0][2]})  
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        raise e


@app.route("/average")
def average():
    try:
        mysql_connection = Mysql_connection()
        student_id = request.args.get('student_id')
        subject_id = request.args.get('subject_id')
        class_id = request.args.get('class_id')

        if student_id:
            rows = mysql_connection.get_data(
                f"select floor(avg(marks_scored)),mst_student.student_name from mst_marks INNER JOIN mst_student ON mst_marks.mst_student_id= mst_student.student_id where mst_student_id={student_id}")

        elif subject_id:
            rows = mysql_connection.get_data(
                f"select floor(avg(marks_scored)),mst_subject.subject_name from mst_marks INNER JOIN mst_subject ON mst_marks.mst_subject_id= mst_subject.subject_id where mst_subject_id={subject_id}")

        elif class_id:
            rows = mysql_connection.get_data(
                f"select floor(avg(marks_scored)),mst_class.class_name from mst_marks INNER JOIN mst_class ON mst_marks.mst_class_id= mst_class.class_id where mst_class_id={class_id}")

        else:
            resp = jsonify({'error': 'User "id" not found in query string'})
            resp.status_code = 500
            return resp
        logging.error(rows)

        resp = jsonify({'Name': rows[0][1], 'Average': rows[0][0]})  # {"studentName":"Jasmine", "average": 98}
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        raise e




if __name__ == "__main__":
    app.run(debug=True, port=8888)
