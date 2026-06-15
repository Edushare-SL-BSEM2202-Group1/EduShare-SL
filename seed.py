import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models

mock_data = [
    {
        "title": "BECE Mathematics Past Papers 2020–2024",
        "description": (
            "[Subject: Mathematics | Grade: JSS 1–3 | Type: Past Exam Paper | Author: Mr. Kamara, Bo District] "
            "Complete collection of BECE mathematics past examination papers with marking schemes.\n\n"
            "EXAM REVISION HIGHLIGHTS:\n"
            "* Number Bases: Master conversions from Base 10 to Base 2 (Binary) and back.\n"
            "* Geometry: Review parallel line angles, alternate angles, and corresponding angles.\n"
            "* Business Math: Remember the Simple Interest formula: I = (P * R * T) / 100."
        )
    },
    {
        "title": "Primary Science: Human Body & Health",
        "description": (
            "[Subject: Science | Grade: Primary 4–6 | Type: Lesson Plan | Author: Mrs. Bangura, Freetown] "
            "6-week lesson plan series on human biology, hygiene, and disease prevention aligned to MBSSE curriculum.\n\n"
            "STUDY NOTES:\n"
            "* Digestive Stages: Mouth (chewing/saliva) -> Esophagus (food pipe) -> Stomach (acid breakdown) -> Small Intestine (nutrient absorption) -> Large Intestine (water balance).\n"
            "* Health Rule: Always boil drinking water and wash hands with soap to prevent waterborne germs like Cholera."
        )
    },
    {
        "title": "English Grammar Workbook – SSS Level",
        "description": (
            "[Subject: English Language | Grade: SSS 1–3 | Type: Textbook | Author: Mr. Conteh, Makeni] "
            "Comprehensive grammar workbook covering tenses, sentence construction, comprehension, and essay writing.\n\n"
            "GRAMMAR RULES:\n"
            "* Subject-Verb Agreement: Singular subjects take singular verbs (The teacher writes). Plural subjects take plural verbs (The teachers write).\n"
            "* Active vs Passive: Active layout puts the doer first (Abu kicked the ball). Passive layouts flip it (The ball was kicked by Abu)."
        )
    },
    {
        "title": "Sierra Leone Geography: Physical Features",
        "description": (
            "[Subject: Social Studies | Grade: JSS 1–3 | Type: Notes | Author: Ms. Koroma, Kenema] "
            "Study notes covering Sierra Leone's rivers, mountains, districts, and climate zones with maps.\n\n"
            "GEOGRAPHY SUMMARY:\n"
            "* Highest Peak: Mount Bintumani, located in the Loma Mountains range.\n"
            "* Major Rivers: The Rokel, Sewa, Moa, and Jong rivers provide vital water resources.\n"
            "* Climate: Tropical climate featuring two distinct seasons: Rainy (May to October) and Dry (November to April)."
        )
    },
    {
        "title": "Agricultural Practices for Rural Communities",
        "description": (
            "[Subject: Agriculture | Grade: All Levels | Type: Textbook | Author: Dr. Sesay, Njala University] "
            "Practical guide to subsistence farming, soil management, and crop rotation suited to Sierra Leone's climate.\n\n"
            "AGRICULTURE CORE NOTE:\n"
            "* Soil Nutrients: Crop rotation prevents soil exhaustion by changing plant types seasonally.\n"
            "* Shifting Cultivation: Clearing a plot of land, farming it for a few seasons, then leaving it fallow to naturally regain fertility."
        )
    },
    {
        "title": "Introduction to ICT: Computers & the Internet",
        "description": (
            "[Subject: ICT | Grade: JSS 1–3 | Type: Lesson Plan | Author: Mr. Fofanah, Limkokwing University] "
            "Beginner ICT lessons covering hardware, software, internet safety, and basic Microsoft Office skills.\n\n"
            "ICT BASICS:\n"
            "* Hardware: Physical parts you can touch (CPU, Keyboard, Mouse, Monitor).\n"
            "* Software: Digital programs you cannot touch (Windows, Microsoft Word, Web Browsers).\n"
            "* Data Safety: Never share account passwords or open suspicious web download links."
        )
    },
    {
        "title": "WASSCE Mathematics Revision Guide",
        "description": (
            "[Subject: Mathematics | Grade: SSS 1–3 | Type: Notes | Author: Mrs. Turay, Freetown] "
            "Comprehensive revision covering algebra, geometry, statistics, and trigonometry for WASSCE candidates.\n\n"
            "TRIGONOMETRY & CIRCLES:\n"
            "* SOH CAH TOA: Sin = Opp/Hyp, Cos = Adj/Hyp, Tan = Opp/Adj.\n"
            "* Circle Theorem: The angle at the center of a circle is always twice the angle at the circumference when subtended by the same arc."
        )
    },
    {
        "title": "Primary English: Reading & Comprehension",
        "description": (
            "[Subject: English Language | Grade: Primary 1–3 | Type: Exercise Sheet | Author: Ms. Mansaray, Port Loko] "
            "Fun reading passages and comprehension exercises suitable for Primary 1 to 3 learners.\n\n"
            "READING FOUNDATIONS:\n"
            "* Punctuation: Capital letters begin sentences. Full stops (.) end statements. Question marks (?) end queries.\n"
            "* Vocabulary: Practice identifying context clues in short stories to discover definitions of unfamiliar words."
        )
    },
    {
        "title": "Basic Science: Experiments for Rural Schools",
        "description": (
            "[Subject: Science | Grade: JSS 1–3 | Type: Lesson Plan | Author: Mr. Jalloh, Kailahun] "
            "Low-cost science experiments designed for schools with no laboratory facilities.\n\n"
            "EXPERIMENTAL NOTES:\n"
            "* Photosynthesis: Demonstrate how green leaves produce food by trapping sunlight with chlorophyll.\n"
            "* Density Experiment: Show how a heavy iron nail sinks in a bucket of water while a light wooden stick floats gracefully on top."
        )
    },
    {
        "title": "Civics & Governance in Sierra Leone",
        "description": (
            "[Subject: Social Studies | Grade: SSS 1–3 | Type: Textbook | Author: Mrs. Koroma, Freetown] "
            "Covers Sierra Leone's constitution, government structures, elections, and citizens' rights.\n\n"
            "CIVICS STRUCTURE:\n"
            "* The Executive: Enforces state laws (The President and Cabinet).\n"
            "* The Legislature: Debates and passes state laws (Parliament and Paramount Chiefs).\n"
            "* The Judiciary: Interprets state laws and dispenses justice (The Chief Justice and Courts)."
        )
    },
    {
        "title": "Mathematics for Primary 4–6: Fractions & Decimals",
        "description": (
            "[Subject: Mathematics | Grade: Primary 4–6 | Type: Exercise Sheet | Author: Mr. Bangura, Bonthe District] "
            "Structured worksheet series on fractions, decimals, and percentages with answer keys.\n\n"
            "FRACTIONS QUICK SUMMARY:\n"
            "* Numerator: The top number showing active parts counted.\n"
            "* Denominator: The bottom number showing the total slices in the whole item.\n"
            "* Percentages: Expressing values out of 100 (e.g., 0.50 equals exactly 50%)."
        )
    },
    {
        "title": "ICT and Digital Safety for Students",
        "description": (
            "[Subject: ICT | Grade: All Levels | Type: Notes | Author: Limkokwing ICT Dept.] "
            "Covers cybersecurity basics, online privacy, digital rights, and responsible internet use.\n\n"
            "DIGITAL REVISION NOTE:\n"
            "* Cyber Hygiene: Use strong passwords mixing uppercase letters, numbers, and symbols.\n"
            "* Digital Public Goods (DPG): Open software solutions designed ethically to support global sustainable development goals (SDG 4)."
        )
    },
    {
        "title": "Agriculture: Rice Farming in Sierra Leone",
        "description": (
            "[Subject: Agriculture | Grade: All Levels | Type: Textbook | Author: Ministry of Agriculture SL] "
            "Detailed guide to upland and swamp rice cultivation, the staple crop of Sierra Leone.\n\n"
            "CROP MANIFESTO:\n"
            "* Swamp Rice (Ecological): Grown in low-lying flooded valleys (Inland Valley Swamps), producing incredibly high annual crop yields.\n"
            "* Upland Rice: Grown on dry hillsides dependent completely on seasonal rainy downpours."
        )
    },
    {
        "title": "English Literature: African Short Stories",
        "description": (
            "[Subject: English Language | Grade: SSS 1–3 | Type: Textbook | Author: Mrs. Koroma, Fourah Bay College] "
            "Anthology of African short stories by Sierra Leonean and West African authors with study guides.\n\n"
            "LITERARY ANALYSIS METRICS:\n"
            "* Theme: The underlying main message or moral lesson of a book narrative.\n"
            "* Plot Structure: Introduction -> Rising Action -> Climax (turning point) -> Resolution (ending)."
        )
    }
]

def seed_database():
    db = SessionLocal()
    try:
        print("Clearing out old database tables...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

        print("Seeding all 14 educational resource profiles into SQLite with curriculum notes...")
        for item in mock_data:
            resource_record = models.Resource(
                title=item["title"],
                description=item["description"],
                file_path="uploads/demo_resource.pdf"
            )
            db.add(resource_record)

        db.commit()
        print("✅ Success! All 14 custom-noted resources written cleanly to edushare.db.")
    except Exception as e:
        print(f"❌ Error during database seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()