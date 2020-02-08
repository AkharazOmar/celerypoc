import ssl
from celery import Celery
from celery.contrib.abortable import AbortableTask


app = Celery("celerypoc", task_cls=AbortableTask)


app.config_from_object(
    {
        "BROKER_URL": "redis://127.0.0.1:6379/0",
        "CELERY_RESULT_BACKEND": "redis://127.0.0.1:6379/0",
        "CELERY_ACCEPT_CONTENT": ['auth'],
        "CELERY_TASK_SERIALIZER": 'auth',
        "CELERY_SECURITY_DIGEST": "sha256",
        "CELERY_SECURITY_CERT_STORE": "/home/oakharaz/dev/python/celery/*.pem",
        "CELERY_SECURITY_CERTIFICATE": "/home/oakharaz/dev/python/celery/worker.pem",
        "CELERY_SECURITY_KEY": "/home/oakharaz/dev/python/celery/worker.key",
        "CELERY_SSL_CERT_REQS": ssl.CERT_REQUIRED,
        "CELERY_RESULT_SERIALIZER": 'auth',
        "CELERY_IMPORTS": ('celerypoc.tasks',),
        "CELERY_RESULT_PERSISTENT": True,
        "CELERY_TASK_RESULT_EXPIRES": 3600,
        "CELERY_TRACK_STARTED": True,
    }
)


app.setup_security()
