from django.core.mail import send_mail


def send_confirmation_mail(email, activation_code):
    message = f"""Спасибо за заказ. Подтвердите бронь по ссылке:
    http://127.0.0.1:8000/api/v1/confirmation/?u={activation_code}"""
    send_mail(
        'Подтверждение брони',
        message,
        'admin@gmail.com',
        [email, ]
    )
