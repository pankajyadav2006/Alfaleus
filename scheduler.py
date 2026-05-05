from apscheduler.schedulers.background import BackgroundScheduler
from scraper import OpportunityScraper
from database import SessionLocal, Opportunity
from ai_tagger import tagger
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def run_scrape_task(keyword="AI startup"):
    logger.info(f"Starting scheduled scrape at {datetime.now()}")
    scraper = OpportunityScraper()
    new_opportunities = scraper.scrape_all(keyword=keyword)
    
    db = SessionLocal()
    added_count = 0
    
    try:
        for opp_data in new_opportunities:
            # Check if exists
            existing = db.query(Opportunity).filter(Opportunity.source_link == opp_data['source_link']).first()
            if not existing:
                new_opp = Opportunity(**opp_data)
                db.add(new_opp)
                added_count += 1
        
        db.commit()
        logger.info(f"Scrape completed: {added_count} new opportunities added")
        
        # Run AI tagger on entries with null funding_range
        untagged = db.query(Opportunity).filter(Opportunity.funding_range == None).all()
        if untagged:
            logger.info(f"AI Tagging {len(untagged)} opportunities...")
            for opp in untagged:
                tags = tagger.tag_opportunity(opp.title, opp.description, opp.organizer)
                opp.funding_range = tags.get("funding_range", "Unknown")
                opp.startup_stage = tags.get("startup_stage", "Any")
                opp.remote_or_onsite = tags.get("remote_or_onsite", "Unknown")
            db.commit()
            logger.info("AI Tagging completed")
            
    except Exception as e:
        logger.error(f"Error in scheduled task: {e}")
        db.rollback()
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Run immediately
    scheduler.add_job(run_scrape_task, 'date', run_date=datetime.now())
    # Run every 6 hours
    scheduler.add_job(run_scrape_task, 'interval', hours=6)
    scheduler.start()
    logger.info("Scheduler started (every 6 hours)")
    return scheduler
