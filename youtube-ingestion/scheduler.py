import logging
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from config import Config
from monitor_agent import MonitorAgent
from process_agent import ProcessAgent

logger = logging.getLogger(__name__)

class Scheduler:
    """Manages scheduled tasks for the ingestion pipeline."""

    def __init__(self):
        self.scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Kolkata'))
        self.monitor_agent = MonitorAgent()
        self.process_agent = ProcessAgent()

    def _monitor_task(self):
        """Task to run monitoring agent."""
        try:
            logger.info("=" * 50)
            logger.info(f"Running monitor task at {datetime.now(pytz.timezone('Asia/Kolkata'))}")
            self.monitor_agent.run()
        except Exception as e:
            logger.error(f"Monitor task failed: {str(e)}")

    def _process_task(self):
        """Task to run processing agent."""
        try:
            logger.info("=" * 50)
            logger.info(f"Running process task at {datetime.now(pytz.timezone('Asia/Kolkata'))}")
            self.process_agent.run()
        except Exception as e:
            logger.error(f"Process task failed: {str(e)}")

    def start(self):
        """Start the scheduler with configured tasks."""
        logger.info("Setting up scheduled tasks...")

        # Schedule monitoring at morning and evening IST
        self.scheduler.add_job(
            self._monitor_task,
            'cron',
            hour=Config.MORNING_CHECK_TIME.hour,
            minute=Config.MORNING_CHECK_TIME.minute,
            id='morning_check',
            name='Morning Channel Check (IST)'
        )

        self.scheduler.add_job(
            self._monitor_task,
            'cron',
            hour=Config.EVENING_CHECK_TIME.hour,
            minute=Config.EVENING_CHECK_TIME.minute,
            id='evening_check',
            name='Evening Channel Check (IST)'
        )

        # Schedule processing every 5 minutes
        self.scheduler.add_job(
            self._process_task,
            'interval',
            minutes=5,
            id='continuous_processing',
            name='Continuous Transcript Processing'
        )

        self.scheduler.start()
        logger.info("Scheduler started successfully")
        logger.info(f"Morning check: {Config.MORNING_CHECK_TIME}")
        logger.info(f"Evening check: {Config.EVENING_CHECK_TIME}")
        logger.info("Processing: Every 5 minutes")

    def stop(self):
        """Stop the scheduler."""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")

    def get_scheduled_jobs(self):
        """Get list of scheduled jobs."""
        return self.scheduler.get_jobs()


if __name__ == "__main__":
    logging.basicConfig(
        level=Config.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(Config.LOG_FILE),
            logging.StreamHandler()
        ]
    )

    scheduler = Scheduler()
    scheduler.start()

    try:
        logger.info("Ingestion pipeline started. Press Ctrl+C to stop.")
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping ingestion pipeline...")
        scheduler.stop()
