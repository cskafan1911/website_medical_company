from datetime import datetime

from celery import shared_task

from appointments.models import Appointment


@shared_task
def check_status_appointment():
    """Проверка даты записи, находящихся в ожидании"""
    active_appointments = Appointment.objects.filter(status_of_appointment='WAITING')

    for appointment in active_appointments:

        if appointment.data <= datetime.now().date():
            if appointment.time <= datetime.now().time():
                appointment.status = 'COMPLETED'
                appointment.save()
