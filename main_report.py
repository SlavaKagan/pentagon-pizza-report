import datetime
from Utils.Functions.status_checker import get_live_status_text
from Configs.emailer import send_email
from Infrastructure.Logging.logger import logger
from Utils.locations import LOCATIONS
from Utils.Functions.email_validator import is_valid_email

def generate_and_send_report(to_email: str):
    if not is_valid_email(to_email):
        logger.error(f"מייל לא תקין: {to_email}")
        print("❌ כתובת המייל אינה תקינה. נסה שוב.")
        return

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summaries = []
    busy_count = 0
    total_locations = len(LOCATIONS)

    for place in LOCATIONS:
        name = place["name"]
        url = place["url"]

        logger.info(f"בודק את {name}...")
        status_text = get_live_status_text(url)

        if status_text:
            lower = status_text.lower()
            if any(k in lower for k in ["closed", "סגור"]):
                summaries.append(generate_html_row(name, status_text, "🚪", "#455a64"))
            elif any(k in lower for k in ["less busy", "not busy", "רגוע", "לא עמוס"]):
                summaries.append(generate_html_row(name, status_text, "✅", "#2e7d32"))
            else:
                summaries.append(generate_html_row(name, status_text, "📈", "#d32f2f"))
                if not any(k in lower for k in ["closed", "סגור"]):  # רק אם לא סגור
                    busy_count += 1
        else:
            summaries.append(generate_html_row(name, "אין מידע בזמן אמת", "❓", "#999"))

    if summaries:
        subject = "📡 דוח סטטוס יומי - Pentagon Pizza"
        body_text = f"דוח סטטוס לכל הסניפים נכון ל־{now}"
        body_html = generate_summary_html(now, summaries, busy_count, total_locations)
        send_email(subject, body_text, body_html, to_email)
    else:
        logger.info("אין תוצאות לשלוח.")


def generate_html_row(place_name, status, icon, color):
    return f"""
        <tr>
            <td style='padding:4px 6px; border:1px solid #ccc; text-align: center; font-size: 14px;'>{icon} {place_name}</td>
            <td style='padding:4px 6px; border:1px solid #ccc; text-align: center; color:{color}; font-size: 14px;'>{status}</td>
        </tr>
    """


def generate_summary_html(timestamp, rows, busy_count, total_locations):
    html_content = f"""
    <html>
      <body style='font-family: Arial, sans-serif; direction: rtl; text-align: right;'>
        <h2 style='color:#1976d2;'>📋 דוח סטטוס סניפים</h2>
        <p><strong>🕒 זמן הבדיקה:</strong> {timestamp}</p>
        <table style='border-collapse: collapse; width: 100%; margin-top: 20px;'>
            <tr style='background-color:#f0f0f0; font-size: 15px; text-align: center;'>
                <th style='padding:6px 8px; border:1px solid #ccc;'>שם המקום</th>
                <th style='padding:6px 8px; border:1px solid #ccc;'>סטטוס</th>
            </tr>
            {''.join(rows)}
        </table>
    """

    if busy_count > total_locations / 2:
        html_content += """
            <p style='color: #d32f2f; font-weight: bold; margin-top: 20px; font-size: 18px; text-align: center;'>
                רוב הפיצריות עמוסות ויש סיכוי למשהו שמתרחש בתוך הפנטגון וצפי לאירוע בשעות הקרובות, יש להיערך בהתאם!
            </p>
            """
    else:
        html_content += """
            <p style='color: #2e7d32; font-weight: bold; margin-top: 20px; font-size: 18px; text-align: center;'>
                כרגע, אין צפי לאירוע שמתרחש בפנטגון
            </p>
            """

    html_content += """
        <hr>
        <p style='font-size: 0.9em; color: #888;'>נשלח אוטומטית ממערכת Pentagon Pizza Alerts</p>
        <img src='cid:PizzaLogo' width='200' alt='Pizza Logo' style='margin-top: 20px; border-radius: 12px; display: block; margin-right: auto; margin-left: auto;'>
      </body>
    </html>
    """
    return html_content


if __name__ == "__main__":

    while True:
        input_email = input("הזן כתובת מייל לקבלת הדוח: ").strip()
        if is_valid_email(input_email):
            break
        print("❌ כתובת המייל אינה תקינה. נסה שוב.\n")

    generate_and_send_report(input_email)
