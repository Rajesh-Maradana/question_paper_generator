from flask import Flask, render_template, session, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required
from sqlalchemy import text
from xhtml2pdf import pisa
from io import BytesIO
from db import engine, SessionLocal
import datetime
import models
import pandas as pd

app = Flask(__name__)

app.config["SECRET_KEY"] = 'okaytest'

models.Base.metadata.create_all(engine)

db = SessionLocal()
# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'


@login_manager.user_loader
def load_user(user_id):
    return db.query(models.User).filter(models.User.id == int(user_id)).first()


@app.route('/')
def index():
    # error = request.args.get("error")
    return render_template('login.html')


@app.route('/login',  methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    try:
        user = db.query(models.User).filter(models.User.username == username).first()
        if user and user.password == password:
            login_user(user)
            session['user'] = username
            session['LoggedIn'] = True
            return jsonify({'status': 'success', 'redirect_to': 'home'}), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Invalid credentials',
                'redirect_to': 'index'
            }), 401
    except Exception:
        return jsonify({
            'status': 'errorsd',
            'message': "User Doesn't Exists"
        }), 500
    finally:
        db.close()


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    print('fdfdfd')
    session.pop('LoggedIn', None)
    session.pop('user', None)
    logout_user()
    return jsonify({'status': 'success'}), 200


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/create', methods=['POST'])
def create_questions():
    try:
        file = request.files.get('file')
        if file and file.filename[-4:] == '.csv':
            df = pd.read_csv(file)
            for i in df.to_dict('records'):
                print(i)
                data_created = datetime.datetime.now()
                new_question = models.Questions(question=i['question'],
                                                subject=i['subject'],
                                                semester=i['semester'],
                                                branch=i['branch'],
                                                marks=i['marks'],
                                                difficulty=i['difficulty'],
                                                date_created=data_created)
                db.add(new_question)
                db.commit()
            return jsonify({"status": "success"}), 201

        else:
            data = request.json
            question = data['question']
            subject = data['subject']
            semester = data['semester']
            branch = data['branch']
            marks = data['marks']
            difficulty = data['difficulty']
            date_created = datetime.datetime.now()
            new_question = models.Questions(question=question, subject=subject,
                                            semester=semester, branch=branch,
                                            marks=marks, difficulty=difficulty,
                                            date_created=date_created)
            db.add(new_question)
            db.commit()
            return jsonify({"status": "success"}), 201
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({"message": str(e)}), 500
    finally:
        # Close the session
        db.close()


@app.route('/show', methods=['GET'])
def show_questions():
    try:
        data = db.query(models.Questions).all()
        questions_list = []
        for question in data:
            questions_list.append({
                'id': question.id,
                'subject': question.subject,
                'semester': question.semester,
                'branch': question.branch,
                'difficulty': question.difficulty,
                'marks': question.marks,
                'date': question.date_created,
                'question': question.question
            })
        return jsonify({'status': 'success', 'data': questions_list}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        db.close()


@app.route("/delete", methods=['POST'])
def delete_question():
    q_id = request.form.get('id')
    if not q_id:
        return jsonify({"status": "error", "message": "No ID provided"}), 400
    try:
        data = db.query(models.Questions).filter(models.Questions.id == q_id).first()
        if data:
            db.delete(data)
            db.commit()
            return jsonify({'status': 'success', 'message': "Deleted the record"}), 200
        else:
            return jsonify({"status": "error", "message": "Item not found"}), 404
    except Exception as e:
        db.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/generate', methods=['POST'])
def generate_questions():
    data = request.json
    subject = data['subject']
    semester = data['semester']
    branch = data['branch']
    questions_d = {}
    try:
        query = """
            SELECT question FROM questions
            WHERE subject = :subject
            AND semester = :semester
            AND branch = :branch
            AND marks = :marks
            ORDER BY RANDOM()
            LIMIT 7;
            """ 
        with engine.connect() as conn:
            print('f')
            filters_ = {
                'subject': subject,
                'semester': semester,
                'branch': branch,
                'marks': 0
            }
            marks_ = [8, 4, 2]
            for i in marks_:
                filters_['marks'] = i   
                result = conn.execute(text(query), filters_)
                s = []
                for questions in result.fetchall():
                    s.append(questions[0])
                    questions_d['Part_'+str(i)] = s

        context = {
            'branch': branch,
            'semester': semester,
            'subject': subject,
            'date': datetime.date.today(),
            'questions_d': questions_d
        }

        rendered_html = render_template('test.html', **context)
        try:
            pdf_output = BytesIO()
            pisa.CreatePDF(rendered_html, dest=pdf_output, encoding='utf-8')
            with open(f"{subject}_question_paper.pdf", "wb") as pdf_file:
                pdf_file.write(pdf_output.getvalue())
            return jsonify({'status': 'success', 'message': 'Generated Successfully'}), 200
        except Exception as e:
            return str(e), 500
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)
