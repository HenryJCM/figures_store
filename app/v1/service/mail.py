import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.v1.utils.config import settings

# Configura los detalles del servidor SMTP de SendGrid
smtp_server = settings.smtp_server
smtp_port = settings.smtp_port
smtp_username = settings.smtp_username
smtp_password = settings.smtp_password

# Crea el mensaje
from_address = settings.from_address
to_address = ""

msg = MIMEMultipart()
msg['From'] = from_address
msg['To'] = to_address
msg['Subject'] = "Test Email from Python"

# Agregar contenido de texto o HTML
body = "This is a test email sent"
msg.attach(MIMEText(body, 'plain'))  # Usa 'html' para contenido HTML

try:
    # Conecta al servidor SMTP de SendGrid usando TLS
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Inicia cifrado TLS
    server.login(smtp_username, smtp_password)  # Autenticarse con la API Key

    # Envía el correo
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)

    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
finally:
    server.quit()  # Cierra la conexión SMTP