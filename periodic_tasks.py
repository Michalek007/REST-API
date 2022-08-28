from flask_apscheduler import APScheduler
from app import app
from db_schema import db, Performance
import psutil
from datetime import datetime

scheduler = APScheduler()


@scheduler.task("cron", id="save_performance", minute="*")
def save_performance():
    parameters = Performance(date=str(datetime.now()), memory_usage=psutil.virtual_memory()[2],
                             CPU_usage=psutil.cpu_percent(), disk_usage=psutil.disk_usage('/')[3])
    with app.app_context():
        db.session.add(parameters)
        db.session.commit()
    print("Performance saved!")


scheduler.init_app(app)
scheduler.start()

# @scheduler.task("interval", id="check_cpu_usage", seconds=10, misfire_grace_time=900)
# check_cpu_usage():
#     print(psutil.cpu_percent())
# @scheduler.task("cron", id="do_job_3", week="*", day_of_week="sun")
# def job3():
#     print("Job 3 executed")


# __all__ = [
#     "scheduler"
# ]
