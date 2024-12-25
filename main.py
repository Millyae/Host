from flask import Flask, jsonify, request, send_from_directory
import mysql.connector
import os
import logging

app = Flask(__name__)

# Секретный ключ для работы с сессиями
app.secret_key = os.urandom(24)

# Конфигурация базы данных
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'SQL123',
    'database': 'mydb',
}

# Настройка логирования
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return "Welcome to the Flask Server!"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/schedule/<int:day_id>', methods=['GET'])
def get_schedule(day_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            d.day_week,
            np.number_pair,
            c.name_cabinet,
            t.name_teacher,
            s.name_subject,
            sl.name_of_type_lesson,
            sg.name_group
        FROM
            pair p
        JOIN day d ON p.id_day = d.id_day
        JOIN number_pair np ON p.id_shedule_number = np.id
        JOIN cabinet c ON p.id_cabinet = c.id_cabinet
        JOIN teacher t ON p.id_teacher = t.id_teacher
        JOIN studentgroup sg ON p.id_group = sg.id_group
        JOIN subject s ON p.id_subject = s.id_subject
        JOIN subjectlesson sl ON p.id_type_lesson = sl.id_typeless
        WHERE d.id_day = %s;
        """
        cursor.execute(query, (day_id,))
        schedule = cursor.fetchall()

        cursor.close()
        connection.close()

        if not schedule:
            return jsonify({'message': 'No schedule found for this day'}), 404

        return jsonify(schedule)
    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/groups', methods=['GET'])
def get_groups():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = "SELECT id_group, name_group, course FROM studentgroup;"
        cursor.execute(query)
        groups = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(groups)
    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/teachers', methods=['GET'])
def get_teachers():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = "SELECT id_teacher, name_teacher, is_active FROM teacher;"
        cursor.execute(query)
        teachers = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(teachers)
    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/cabinets', methods=['GET'])
def get_cabinets():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT
            c.id_cabinet,
            c.name_cabinet,
            ct.Type_Cabinet
        FROM
            cabinet c
        JOIN cabinettype ct ON c.id_type = ct.id_type;
        """
        cursor.execute(query)
        cabinets = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(cabinets)
    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
