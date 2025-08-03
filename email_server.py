from flask import Flask, request, jsonify
from flask_cors import CORS
from main_report import generate_and_send_report

app = Flask(__name__)
CORS(app)

@app.route("/send_report", methods=["POST"])
def send_report():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"message": "לא התקבלה כתובת מייל"}), 400

    try:
        generate_and_send_report(email)
        return jsonify({"message": f"הדוח נשלח בהצלחה אל {email}"}), 200
    except Exception as e:
        return jsonify({"message": f"שגיאה בשליחה: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000)
