from database import SessionLocal, Opportunity, init_db
import datetime

def seed_data():
    init_db()
    db = SessionLocal()
    
    # Check if data already exists
    if db.query(Opportunity).count() > 0:
        print("Database already has data. Skipping seed.")
        db.close()
        return

    opportunities = [
        # 8 Grants
        {
            "title": "SBIR Phase I: Startup Innovation Grant",
            "type": "Grant",
            "organizer": "National Science Foundation",
            "location": "USA / Remote",
            "deadline": "2026-08-15",
            "source_link": "https://seedfund.nsf.gov/apply/",
            "source_name": "NSF",
            "description": "The NSF SBIR program provides up to $275,000 in equity-free funding for R&D.",
            "funding_range": "$275,000",
            "startup_stage": "Early",
            "remote_or_onsite": "Remote",
            "tags": "R&D, Deep Tech, Federal"
        },
        {
            "title": "Google for Startups Cloud Program",
            "type": "Grant",
            "organizer": "Google",
            "location": "Global",
            "deadline": "2026-12-31",
            "source_link": "https://cloud.google.com/startup",
            "source_name": "Google",
            "description": "Get up to $100,000 in Google Cloud credits and technical support.",
            "funding_range": "$100K Credits",
            "startup_stage": "Early",
            "remote_or_onsite": "Remote",
            "tags": "Cloud, Infrastructure"
        },
        {
            "title": "AWS Activate Founders",
            "type": "Grant",
            "organizer": "Amazon Web Services",
            "location": "Global",
            "deadline": "2026-12-01",
            "source_link": "https://aws.amazon.com/activate/",
            "source_name": "AWS",
            "description": "AWS credits, business support, and technical training for early stage startups.",
            "funding_range": "$1,000 - $100,000 Credits",
            "startup_stage": "Early",
            "remote_or_onsite": "Remote",
            "tags": "Cloud, AWS"
        },
        {
            "title": "Microsoft for Startups Founders Hub",
            "type": "Grant",
            "organizer": "Microsoft",
            "location": "Global",
            "deadline": "2026-11-15",
            "source_link": "https://foundershub.startups.microsoft.com/",
            "source_name": "Microsoft",
            "description": "Access to Azure credits, OpenAI Service, and expert mentorship.",
            "funding_range": "$150K Credits",
            "startup_stage": "Early",
            "remote_or_onsite": "Remote",
            "tags": "AI, Cloud, Microsoft"
        },
        {
            "title": "EIC Accelerator Grant",
            "type": "Grant",
            "organizer": "European Innovation Council",
            "location": "Europe",
            "deadline": "2026-09-10",
            "source_link": "https://eic.ec.europa.eu/eic-funding-opportunities_en",
            "source_name": "EU",
            "description": "Funding and equity for small and medium-sized enterprises with high impact.",
            "funding_range": "€2.5M Grant + €15M Equity",
            "startup_stage": "Growth",
            "remote_or_onsite": "Hybrid",
            "tags": "EU, Innovation, Scaling"
        },
        {
            "title": "Antler Global Startup Grant",
            "type": "Grant",
            "organizer": "Antler",
            "location": "Global",
            "deadline": "2026-10-01",
            "source_link": "https://www.antler.co/",
            "source_name": "Antler",
            "description": "Pre-seed funding for individual founders and early teams.",
            "funding_range": "$100K - $200K",
            "startup_stage": "Early",
            "remote_or_onsite": "On-site",
            "tags": "Pre-seed, Founders"
        },
        {
            "title": "Cartier Women's Initiative",
            "type": "Grant",
            "organizer": "Cartier",
            "location": "Global",
            "deadline": "2026-07-30",
            "source_link": "https://www.cartierwomensinitiative.com/",
            "source_name": "Cartier",
            "description": "Funding and support for women impact entrepreneurs.",
            "funding_range": "$30K - $100K",
            "startup_stage": "Any",
            "remote_or_onsite": "Hybrid",
            "tags": "Female Founders, Social Impact"
        },
        {
            "title": "Unicef Innovation Fund",
            "type": "Grant",
            "organizer": "UNICEF",
            "location": "Global",
            "deadline": "2026-08-01",
            "source_link": "https://www.unicefinnovationfund.org/",
            "source_name": "UNICEF",
            "description": "Funding for open-source technology solutions for children.",
            "funding_range": "$100K",
            "startup_stage": "Early",
            "remote_or_onsite": "Remote",
            "tags": "Open Source, Social Good"
        },

        # 6 Conferences
        {
            "title": "Web Summit 2026",
            "type": "Conference",
            "organizer": "Web Summit",
            "location": "Lisbon, Portugal",
            "deadline": "2026-11-01",
            "source_link": "https://websummit.com/",
            "source_name": "Web Summit",
            "description": "The world's largest technology conference bringing together founders and investors.",
            "funding_range": "Networking",
            "startup_stage": "Any",
            "remote_or_onsite": "On-site",
            "tags": "Networking, Tech, Lisbon"
        },
        {
            "title": "Slush 2026",
            "type": "Conference",
            "organizer": "Slush",
            "location": "Helsinki, Finland",
            "deadline": "2026-11-20",
            "source_link": "https://www.slush.org/",
            "source_name": "Slush",
            "description": "The world's most founder-focused event with thousands of investors.",
            "funding_range": "Pitch Competitions",
            "startup_stage": "Any",
            "remote_or_onsite": "On-site",
            "tags": "VC, Startups, Helsinki"
        },
        {
            "title": "TechCrunch Disrupt 2026",
            "type": "Conference",
            "organizer": "TechCrunch",
            "location": "San Francisco, USA",
            "deadline": "2026-09-15",
            "source_link": "https://techcrunch.com/events/disrupt-2026/",
            "source_name": "TechCrunch",
            "description": "The premiere startup event where next-gen startups are introduced.",
            "funding_range": "$100K Battlefield Prize",
            "startup_stage": "Early",
            "remote_or_onsite": "On-site",
            "tags": "San Francisco, Media, Pitch"
        },
        {
            "title": "SXSW 2027 Startup Track",
            "type": "Conference",
            "organizer": "SXSW",
            "location": "Austin, Texas",
            "deadline": "2027-03-10",
            "source_link": "https://www.sxsw.com/",
            "source_name": "SXSW",
            "description": "Annual conglomeration of parallel film, interactive media, and music festivals.",
            "funding_range": "Awards",
            "startup_stage": "Any",
            "remote_or_onsite": "On-site",
            "tags": "Interactive, Music, Austin"
        },
        {
            "title": "Collision 2026",
            "type": "Conference",
            "organizer": "Web Summit",
            "location": "Toronto, Canada",
            "deadline": "2026-06-15",
            "source_link": "https://collisionconf.com/",
            "source_name": "Collision",
            "description": "The fastest-growing tech conference in North America.",
            "funding_range": "Networking",
            "startup_stage": "Any",
            "remote_or_onsite": "On-site",
            "tags": "Toronto, Tech, Growth"
        },
        {
            "title": "CES 2027 Eureka Park",
            "type": "Conference",
            "organizer": "CTA",
            "location": "Las Vegas, USA",
            "deadline": "2027-01-05",
            "source_link": "https://www.ces.tech/",
            "source_name": "CES",
            "description": "The most influential tech event in the world — the proving ground for breakthrough technologies.",
            "funding_range": "Exhibition",
            "startup_stage": "Any",
            "remote_or_onsite": "On-site",
            "tags": "Hardware, Consumer Tech"
        },

        # 6 Accelerators
        {
            "title": "Y Combinator Summer 2026",
            "type": "Accelerator",
            "organizer": "Y Combinator",
            "location": "San Francisco / Remote",
            "deadline": "2026-03-25",
            "source_link": "https://www.ycombinator.com/apply",
            "source_name": "YC",
            "description": "The world's most successful startup accelerator program.",
            "funding_range": "$500,000",
            "startup_stage": "Early",
            "remote_or_onsite": "Hybrid",
            "tags": "Pre-seed, Seed, Tier 1"
        },
        {
            "title": "Techstars Global Accelerator",
            "type": "Accelerator",
            "organizer": "Techstars",
            "location": "Global (Multiple Cities)",
            "deadline": "2026-05-10",
            "source_link": "https://www.techstars.com/accelerators",
            "source_name": "Techstars",
            "description": "Techstars accelerators help entrepreneurs succeed through mentorship and funding.",
            "funding_range": "$120,000",
            "startup_stage": "Early",
            "remote_or_onsite": "On-site",
            "tags": "Mentorship, Network"
        },
        {
            "title": "500 Global Accelerator",
            "type": "Accelerator",
            "organizer": "500 Global",
            "location": "San Francisco, USA",
            "deadline": "2026-08-01",
            "source_link": "https://500.co/accelerator",
            "source_name": "500 Global",
            "description": "Venture capital firm that invests early in founders building fast-growing technology companies.",
            "funding_range": "$150,000",
            "startup_stage": "Early",
            "remote_or_onsite": "On-site",
            "tags": "Growth, Marketing"
        },
        {
            "title": "Entrepreneur First (EF) LDN20",
            "type": "Accelerator",
            "organizer": "Entrepreneur First",
            "location": "London, UK",
            "deadline": "2026-09-01",
            "source_link": "https://www.joinef.com/",
            "source_name": "EF",
            "description": "Invests in individuals before they have a team or an idea.",
            "funding_range": "Stipend + £80K Investment",
            "startup_stage": "Early",
            "remote_or_onsite": "On-site",
            "tags": "Talent, Pre-team"
        },
        {
            "title": "Plug and Play Tech Center",
            "type": "Accelerator",
            "organizer": "Plug and Play",
            "location": "Sunnyvale, CA",
            "deadline": "Rolling",
            "source_link": "https://www.plugandplaytechcenter.com/",
            "source_name": "Plug and Play",
            "description": "Innovation platform, bringing together startups, corporations, and investors.",
            "funding_range": "Variable Investment",
            "startup_stage": "Growth",
            "remote_or_onsite": "Hybrid",
            "tags": "Corporate, Scaling"
        },
        {
            "title": "Seedcamp XI",
            "type": "Accelerator",
            "organizer": "Seedcamp",
            "location": "London / Europe",
            "deadline": "2026-10-15",
            "source_link": "https://seedcamp.com/",
            "source_name": "Seedcamp",
            "description": "Europe's seed fund, investing early in world-class founders.",
            "funding_range": "$100K - $500K",
            "startup_stage": "Early",
            "remote_or_onsite": "Hybrid",
            "tags": "Europe, Seed"
        },

        # 5 Competitions
        {
            "title": "Global Student Entrepreneur Awards",
            "type": "Competition",
            "organizer": "Entrepreneurs' Organization",
            "location": "Global",
            "deadline": "2026-12-15",
            "source_link": "https://gsea.org/",
            "source_name": "GSEA",
            "description": "Premier global competition for students who own and operate a business.",
            "funding_range": "$50K Prize Pool",
            "startup_stage": "Early",
            "remote_or_onsite": "On-site",
            "tags": "Student, Founders"
        },
        {
            "title": "MIT $100K Entrepreneurship Competition",
            "type": "Competition",
            "organizer": "MIT",
            "location": "Cambridge, MA",
            "deadline": "2026-04-01",
            "source_link": "https://www.mit100k.org/",
            "source_name": "MIT",
            "description": "One of the world's most famous student startup competitions.",
            "funding_range": "$100K Grand Prize",
            "startup_stage": "Early",
            "remote_or_onsite": "On-site",
            "tags": "Academic, Deep Tech"
        },
        {
            "title": "Rice Business Plan Competition",
            "type": "Competition",
            "organizer": "Rice University",
            "location": "Houston, Texas",
            "deadline": "2027-01-10",
            "source_link": "https://rbpc.rice.edu/",
            "source_name": "Rice",
            "description": "The world’s largest and richest graduate-level student startup competition.",
            "funding_range": "$1M+ Total Prizes",
            "startup_stage": "Early",
            "remote_or_onsite": "On-site",
            "tags": "Student, Rich Prizes"
        },
        {
            "title": "Hult Prize 2027",
            "type": "Competition",
            "organizer": "Hult Prize Foundation",
            "location": "Global",
            "deadline": "2026-12-30",
            "source_link": "https://www.hultprize.org/",
            "source_name": "Hult Prize",
            "description": "Global challenge for student social entrepreneurs.",
            "funding_range": "$1,000,000",
            "startup_stage": "Early",
            "remote_or_onsite": "On-site",
            "tags": "Social Impact, UN"
        },
        {
            "title": "Milken-Penn GSE Education Business Plan Competition",
            "type": "Competition",
            "organizer": "UPenn",
            "location": "Philadelphia, PA",
            "deadline": "2026-05-20",
            "source_link": "https://www.educationcompetition.org/",
            "source_name": "Milken-Penn",
            "description": "The most prestigious competition for EdTech startups.",
            "funding_range": "$100K+ Prizes",
            "startup_stage": "Any",
            "remote_or_onsite": "Hybrid",
            "tags": "EdTech, Innovation"
        }
    ]

    for opp_data in opportunities:
        opp = Opportunity(**opp_data)
        db.add(opp)
    
    db.commit()
    print(f"Successfully seeded {len(opportunities)} opportunities.")
    db.close()

if __name__ == "__main__":
    seed_data()
