import os
import logging

logger = logging.getLogger(__name__)

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "cristianmiguelrubio@gmail.com")
EMAIL_FROM = os.getenv("EMAIL_FROM", "Oposiciones del Estado <noreply@oposapp.es>")


def email_configurado():
    return bool(RESEND_API_KEY)


def _enviar(destinatario: str, asunto: str, html: str) -> bool:
    if not email_configurado():
        logger.warning("RESEND_API_KEY no configurada")
        return False
    try:
        import resend
        resend.api_key = RESEND_API_KEY
        resend.Emails.send({
            "from": EMAIL_FROM,
            "to": [destinatario],
            "subject": asunto,
            "html": html,
        })
        logger.info(f"Email enviado a {destinatario}: {asunto}")
        return True
    except Exception as e:
        logger.error(f"Error enviando email a {destinatario}: {type(e).__name__}: {e}")
        return False


def enviar_codigo_recuperacion(destinatario: str, codigo: str) -> bool:
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
      <p style="color: #aaa; font-size: 12px;">Oposiciones del Estado</p>
    </div>
    """
    return _enviar(destinatario, "Recuperación de contraseña — Oposiciones del Estado", html)


def enviar_notificacion_sugerencia(texto: str, usuario_email: str) -> bool:
    html = f"""
    <div style="font-family: sans-serif; max-width: 480px; margin: auto; padding: 24px;">
      <h2 style="color: #1e3a5f;">💡 Nueva sugerencia</h2>
      <p style="color: #444;">De: <strong>{usuario_email}</strong></p>
      <div style="background: #f0f4ff; border-left: 4px solid #1e3a5f; padding: 16px;
                  border-radius: 8px; margin: 16px 0; color: #333; font-size: 15px;">
        {texto}
      </div>
      <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
      <p style="color: #aaa; font-size: 12px;">Oposiciones del Estado · Panel admin: /admin</p>
    </div>
    """
    return _enviar(ADMIN_EMAIL, "💡 Nueva sugerencia recibida — Oposiciones del Estado", html)
