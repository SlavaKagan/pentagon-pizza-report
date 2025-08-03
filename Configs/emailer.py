import smtplib
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from Configs.config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER, SMTP_SERVER, SMTP_PORT, LOGO_PATH
from Infrastructure.Logging.logger import logger

def send_email(subject, body_text, body_html=None, to_email=None):
    try:
        recipient = to_email if to_email else EMAIL_RECEIVER

        msg = MIMEMultipart("related")
        msg['From'] = formataddr(("Pentagon Pizza Alerts", EMAIL_SENDER))
        msg['To'] = recipient
        msg['Subject'] = subject

        alt_part = MIMEMultipart("alternative")
        alt_part.attach(MIMEText(body_text, 'plain'))
        if body_html:
            alt_part.attach(MIMEText(body_html, 'html'))
        msg.attach(alt_part)

        if body_html:
            with open(LOGO_PATH, 'rb') as img:
                img_data = MIMEImage(img.read())
                img_data.add_header('Content-ID', '<PizzaLogo>')
                img_data.add_header('Content-Disposition', 'inline', filename='PizzaLogo.jpg')
                msg.attach(img_data)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        logger.info("המייל (כולל HTML ותמונה מקומית) נשלח בהצלחה.")
    except Exception as e:
        logger.error(f"שגיאה בשליחת המייל: {e}")