import requests
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_admin_notification(booking):
    subject = f"New Book: {booking.tour.title}"
    message = render_to_string(
        "emails/booking_notification.txt",
        {
            "booking": booking,
        },
    )
    html_message = render_to_string(
        "emails/booking_notification.html",
        {
            "booking": booking,
        },
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        html_message=html_message,
    )

    telegram_message = (
        f"📌 Nueva reserva recibida:\n\n"
        f"🏖 Tour: {booking.tour.title}\n"
        f"📅 Fecha: {booking.date}\n"
        f"👥 Adultos: {booking.adults}\n"
        f"🧒 Niños: {booking.kids}\n"
        f"👶 Bebés: {booking.children}\n"
        f"💰 Total: ${booking.total_price}\n"
        f"👤 Cliente: {booking.full_name}\n"
        f"📞 Teléfono: {booking.phone}"
    )

    send_telegram_notification(telegram_message)


def send_telegram_notification(message):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
    }
    requests.post(url, data=data)
