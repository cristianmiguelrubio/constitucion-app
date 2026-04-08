import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER)


def email_configurado():
    return bool(SMTP_HOST and SMTP_USER and SMTP_PASS)


def enviar_codigo_recuperacion(destinatario: str, codigo: str) -> bool:
    if not email_configurado():
        logger.warning("Email no configurado — SMTP_HOST, SMTP_USER, SMTP_PASS requeridos")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Recuperación de contraseña — Oposiciones del Estado"
        msg["From"] = EMAIL_FROM
        msg["To"] = destinatario

        html = f"""
        <div style="font-family: sans-serif; max-width: 480px; margin: auto; padding: 24px;">
          <h2 style="color: #1e3a5f;">Recuperar contraseña</h2>
          <p>Tu código de recuperación es:</p>
          <div style="font-size: 40px; font-weight: bold; letter-spacing: 12px;
                      color: #1e3a5f; background: #f0f4ff; padding: 20px;
                      border-radius: 12px; text-align: center; margin: 20px 0;">
            {codigo}
          </div>
          <p style="color: #666; font-size: 14px;">
            Válido durante <strong>15 minutos</strong>.<br>
            Si no solicitaste este código, ignora este correo.
          </p>
          <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
          <p style="color: #aaa; font-size: 12px;">Oposiciones del Estado · oposapp.com</p>
        </div>
        """

        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(EMAIL_FROM, destinatario, msg.as_string())

        logger.info(f"Código de recuperación enviado a {destinatario}")
        return True

    except Exception as e:
        logger.error(f"Error enviando email a {destinatario}: {e}")
        return False
