from flask import Flask, render_template, request, redirect, flash
from main_report import generate_and_send_report
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        if email and EMAIL_REGEX.match(email):
            try:
                generate_and_send_report(email)
                flash('הדו"ח נשלח בהצלחה!', 'success')
            except Exception as e:
                flash(f'שגיאה בשליחה: {str(e)}', 'danger')
        else:
            flash('כתובת מייל לא תקינה.', 'warning')
        return redirect('/')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
