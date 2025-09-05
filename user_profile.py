from datetime import datetime, timedelta

# ==============================
# User Profile (Dummy Example)
# ==============================
user_profile = {
    "name": "John Doe",
    "dob": "15-08-1998",
    "Age": "27",
    "phone": "xxxxxxxxxx",
    "email": "john.doe@example.com",
    "password": "YourPassword123!",   # 🔑 update with real password before using
    "education": {
        "degree": "B.Tech",
        "branch": "Computer Science and Engineering",
        "institute": "ABC Institute of Technology",
        "cgpa": "8.2",
        "year": "2016-2020"
    },
    "work_experience": [
        {
            "company": "Tech Solutions Ltd",
            "role": "Software Engineer",
            "duration": "Jul 2022 - Present",
            "skills": ["Python", "Django", "REST APIs", "AWS", "Docker", "CI/CD"]
        },
        {
            "company": "CodeWorks Inc",
            "role": "Backend Developer",
            "duration": "Jan 2021 - Jun 2022",
            "skills": ["Node.js", "Express", "MongoDB", "Microservices"]
        },
        {
            "company": "Freelance Projects",
            "role": "Full Stack Developer",
            "duration": "Jul 2020 - Dec 2020",
            "skills": ["React", "Django", "MySQL", "API Integration"]
        }
    ],
    "skills": {
        "languages": ["C", "C++", "Python", "JavaScript", "Java"],
        "frameworks": ["Django", "React", "Next.js", "Flask"],
        "tools": ["Git", "Postman", "Docker", "JIRA", "VS Code"],
        "databases": ["MySQL", "PostgreSQL", "SQLite"],
        "Cloud": ["AWS", "GCP"]
    },
    "preferences": {
        "current_ctc": "6 LPA",
        "expected_ctc": "10 LPA",
        "notice_period": "30 days",
        "relocation": "Yes",
        "preferred_location": "Bangalore",
        "employment_type": "Full-time"
    },
    "achievements": [
        "Winner - CodeFest Hackathon 2022",
        "Runner-up - AI Challenge 2021",
        "Best Project Award - College Tech Fest"
    ]
}

# Date of joining = next 15 days from now
JOINING_DATE = (datetime.now() + timedelta(days=15)).strftime("%d-%m-%Y")
