from celery_app import send_notification

def test_celery_task():
    res = send_notification.delay(1, {'t':'hi'})
    assert res is not None
