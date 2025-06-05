from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
from resume_parser import parse_resume, extract_resume_info
from question_generator import generate_questions
from evaluator import evaluate_answer
from dotenv import load_dotenv
import os
load_dotenv()


app = Flask(__name__)
app.secret_key = os.urandom(24)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return "No file part", 400
        file = request.files['resume']
        if file.filename == '':
            return "No selected file", 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Extract resume text & info
            resume_text = parse_resume(filepath)
            structured_info = extract_resume_info(resume_text)

            # Save info & resume text in session for next steps
            session['structured_info'] = structured_info
            session['resume_text'] = resume_text

            # Generate interview questions based on extracted info
            questions = generate_questions(resume_text)
            session['questions'] = questions
            session['current_question_idx'] = 0
            session['answers'] = []

            # Clean up uploaded file
            os.remove(filepath)
            return render_template('resume_info.html', resume_info=structured_info)
        else:
            return "File type not allowed", 400
    return render_template('index.html')


@app.route('/interview', methods=['GET', 'POST'])
def interview():
    questions = session.get('questions')
    current_idx = session.get('current_question_idx', 0)
    answers = session.get('answers', [])

    if not questions or current_idx >= len(questions):
        return redirect(url_for('index'))

    current_question = questions[current_idx]
    feedback = None

    if request.method == 'POST':
        answer = request.form.get('answer')
        if not answer:
            return render_template('interview.html', question=current_question, feedback="Please enter an answer.")

        # Evaluate answer
        feedback = evaluate_answer(current_question, answer)

        # Save answer and feedback
        answers.append({'question': current_question, 'answer': answer, 'feedback': feedback})
        session['answers'] = answers
        session['current_question_idx'] = current_idx + 1

        # If more questions, show next
        if session['current_question_idx'] < len(questions):
            next_question = questions[session['current_question_idx']]
            return render_template('interview.html', question=next_question, feedback=feedback)
        else:
            return render_template('interview_summary.html', answers=answers)

    # GET method: show current question
    return render_template('interview.html', question=current_question)

if __name__ == '__main__':
    app.run(debug=True)
