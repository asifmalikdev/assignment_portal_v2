from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from assignments.models import Assignment


@receiver(post_save, sender=Assignment)
def send_assignment_notification(sender, instance, created, **kwargs):
    if created:
        subject ="New Assignment Submitted"
        teacher = instance.teacher.get_full_name()
        class_anme = instance.assigned_class.name
        print("in notifications")
        message= (
            f"A new Assignment was created.\n\n"
            f"Title : {instance.title}\n"
            f"Teacher : {teacher}\n"
            f"Class : {class_anme}"
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            ['asifhameed8944@gmail.com']
        )