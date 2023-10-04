
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone

from orders.models import Order
from robots.models import Robot


@receiver(post_save, sender=Robot)
def notify_client(sender, instance, created, **kwargs):
    if created:
        orders = Order.objects.all()
        for order in orders:
            if instance.serial == order.robot_serial:
                subject = 'Ваш робот доступен'
                message = 'Добрый день!\n Недавно вы интересовались нашим роботом модели X, версии Y.\n Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами'
                from_email = 'your@example.com'
                recipient_list = [str(order.customer)]  # Заменить на адрес клиента
                print(subject)
                print(message)
                print(from_email)
                print(recipient_list)
                send_mail(subject, message, from_email, recipient_list)