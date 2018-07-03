import time
from celery import Celery, platforms

celery = Celery('tasks', broker='redis://localhost:6379/0')
platforms.C_FORCE_ROOT = True

@celery.task
def sendmail(mail):
    print('sending mail to %s...' % mail['to'])
    time.sleep(2.0)
    print('mail sent.')

# celery -A task worker --loglevel=info
