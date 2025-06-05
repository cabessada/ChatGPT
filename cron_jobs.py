from apscheduler.schedulers.background import BackgroundScheduler
from services.github_service import commit_and_push

def start_cron():
    scheduler = BackgroundScheduler()
    scheduler.add_job(commit_and_push, 'interval', minutes=30)
    scheduler.start()
