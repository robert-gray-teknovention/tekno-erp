from celery import shared_task


@shared_task
def saying_hello(**kwargs):
    additional = kwargs['additional']
    main = kwargs['main']
    print(main)
    print(additional)
