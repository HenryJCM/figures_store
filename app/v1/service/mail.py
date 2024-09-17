import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.v1.utils.config import settings

# Configura los detalles del servidor SMTP de SendGrid
smtp_server = settings.smtp_server
smtp_port = settings.smtp_port
smtp_username = settings.smtp_username
smtp_password = settings.smtp_password
from_address = settings.from_address

templates = Jinja2Templates(directory="templates")

async def send_email(to_email, subject, template, params):
    msg = MIMEMultipart("alternative")
    msg['From'] = from_address
    msg['To'] = to_email
    msg['Subject'] = subject

    # Renderizar la plantilla HTML con los datos
    html_content = templates.TemplateResponse(f"{template}.html", params)
    html_str = await html_content.body()

    # Agregar contenido
    part = MIMEText(html_str, 'html')
    msg.attach(part)

    try:
        # Conecta al servidor SMTP de SendGrid usando TLS
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Inicia cifrado TLS
        server.login(smtp_username, smtp_password)  # Autenticarse con la API Key

        # Envía el correo
        text = msg.as_string()
        server.sendmail(from_address, to_email, text)

        return True
    except Exception:
        return False
    finally:
        server.quit()  # Cierra la conexión SMTP