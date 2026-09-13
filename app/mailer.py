"""Outgoing e-mail over SMTP (e.g. Gmail with an App Password). Configured through WS_SMTP_* env vars."""
import logging
import os
import smtplib
import ssl
from email.message import EmailMessage

log = logging.getLogger("worksheets.mail")


def configured() -> bool:
    return bool(os.environ.get("WS_SMTP_HOST") and os.environ.get("WS_SMTP_USER") and os.environ.get("WS_SMTP_PASSWORD"))


def send(to: str, subject: str, text: str, html: str = None) -> bool:
    if not configured():
        log.warning("SMTP não configurado; e-mail para %s não enviado (assunto: %s)", to, subject)
        return False
    host = os.environ["WS_SMTP_HOST"]
    port = int(os.environ.get("WS_SMTP_PORT", "587"))
    user = os.environ["WS_SMTP_USER"]
    msg = EmailMessage()
    msg["From"] = os.environ.get("WS_SMTP_FROM", user)
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(text)
    if html:
        msg.add_alternative(html, subtype="html")
    try:
        ctx = ssl.create_default_context()
        if port == 465:
            with smtplib.SMTP_SSL(host, port, context=ctx, timeout=20) as s:
                s.login(user, os.environ["WS_SMTP_PASSWORD"])
                s.send_message(msg)
        else:
            with smtplib.SMTP(host, port, timeout=20) as s:
                s.starttls(context=ctx)
                s.login(user, os.environ["WS_SMTP_PASSWORD"])
                s.send_message(msg)
        log.info("e-mail enviado para %s (%s)", to, subject)
        return True
    except Exception:
        log.exception("falha ao enviar e-mail para %s", to)
        return False
