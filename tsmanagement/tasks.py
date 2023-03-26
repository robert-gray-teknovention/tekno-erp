from celery import shared_task


@shared_task
def saying_hello():
    print("just saying hellow")
