from datetime import datetime, timedelta

# ==============================
# User Profile (Dynamic)
# ==============================
user_profile = {
    "name": "Udaysantoshkumar Burlu",
    "dob": "25-07-2003",
    "Age": "22",
    "phone": "9705795884",
    "email": "your_email@gmail.com",
    "password": "PASSWORD",   # 🔑 update
    "education": {
        "degree": "B.Tech",
        "branch": "Computer Science and Engineering",
        "institute": "Lendi Institute of Engineering and Technology",
        "cgpa": "8.9",
        "year": "2020-2024"
    },
    "work_experience": [
        {
            "company": "Think Future Technologies",
            "role": "Software Engineer L1",
            "duration": "Sep 2024 - Present",
            "skills": ["Python", "Django", "Apache Solr", "Kubernetes", "Celery", "Redis", "AWS", "GCP", "Talend", "Dataform`"]
        },
        {
            "company": "Reform (Freelance)",
            "role": "Python/Django Developer",
            "duration": "Jan 2024 - Apr 2025",
            "skills": ["Django", "CRM", "Backend Development", "Python"]
        },
        {
            "company": "AlignAV",
            "role": "NextJS + Django Developer",
            "duration": "Dec 2023 - Feb 2024",
            "skills": ["NextJS", "Django", "API Optimization", "Full stack", "Python"]
        }
    ],
    "skills": {
        "languages": ["C", "C++", "Python", "HTML+CSS", "Java", "JavaScript"],
        "frameworks": ["Django", "ReactJS", "NextJS", "Java EE"],
        "tools": ["PowerBI", "Postman", "Git", "JIRA", "Photoshop"],
        "databases": ["MySQL", "PostgreSQL", "SQLite", "Firebase", "AWS"],
        "Cloud": ["AWS", "GCP"]
    },
    "preferences": {
        "current_ctc": "7 LPA",
        "expected_ctc": "12 LPA",
        "notice_period": "15 days",
        "relocation": "Yes",
        "preferred_location": "Hyderabad",
        "employment_type": "Full-time"
    },
    "achievements": [
        "2nd Prize - INNO EXPO 360 Hackathon",
        "1st Prize - App Design Contest",
        "Jury Award - HackTriad"
    ]
}

# Date of joining = next 15 days from now
JOINING_DATE = (datetime.now() + timedelta(days=15)).strftime("%d-%m-%Y")
