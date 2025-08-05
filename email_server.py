from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from main_report import generate_and_send_report
from Infrastructure.Logging.logger import logger  # Assuming logger is available

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Serve the email input form."""
    return render_template('email_input.html')

@app.route("/send_report", methods=["POST"])
def send_report():
    """Handle POST request to send the status report email."""
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"message": "לא התקבלה כתובת מייל"}), 400

    try:
        generate_and_send_report(email)
        logger.info(f"Report successfully sent to {email}")
        return jsonify({"message": f"הדוח נשלח בהצלחה אל {email}"}), 200
    except Exception as e:
        logger.error(f"Error sending report to {email}: {str(e)}")
        return jsonify({"message": f"שגיאה בשליחה: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)  # For local testing only