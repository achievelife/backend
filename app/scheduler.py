from app import models, scheduler
from datetime import datetime, timedelta

##########################
# Clear out all sessions #
# every 30 minutes that  #
# are 24 hours old       #
##########################
@scheduler.scheduled_job('cron', id='cleanup_sessions', second=0, minute=30)
def cleanup_sessions():
	print "[CRON] Cleaning up sessions..."
	try:
		ago = datetime.utcnow() - timedelta(hours=24)

		num = models.Session.query.filter(models.Session.time < ago).delete()
		db.session.commit()

		print "[CRON] Cleaned up %d old sessions" % (num)
	except Exception as e:
		print e
		db.session.rollback()

		print "[CRON] Failure - rollback triggered"
