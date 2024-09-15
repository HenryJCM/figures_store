import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.v1.utils.config import settings

# Configura los detalles del servidor SMTP de SendGrid
smtp_server = settings.smtp_server
smtp_port = settings.smtp_port
smtp_username = settings.smtp_username
smtp_password = settings.smtp_password
from_address = settings.from_address

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_email
    msg['Subject'] = subject

    # Agregar contenido
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Conecta al servidor SMTP de SendGrid usando TLS
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Inicia cifrado TLS
        server.login(smtp_username, smtp_password)  # Autenticarse con la API Key

        # Envía el correo
        text = msg.as_string()
        server.sendmail(from_address, to_email, text)

        print("El correo se envió con éxito!")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
    finally:
        server.quit()  # Cierra la conexión SMTP