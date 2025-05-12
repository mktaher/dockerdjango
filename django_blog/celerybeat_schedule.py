from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'update-post-dates-every-30-seconds': {
        'task': 'blog.tasks.update_post_dates',
        'schedule': 30.0,
    },
}
