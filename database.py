from sqlalchemy import create_engine, text
import os

# NeonDB Connection String
DB_URL = os.environ['DB_URL']

# Create SQLAlchemy engine
engine = create_engine(DB_URL)

def load_jobs_from_db():
  with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM jobs"))
      jobs = []
      for row in result.fetchall():
          jobs.append(row._asdict())
      return jobs

def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM jobs WHERE id = :val"),
             {"val": id}
        )
        
        rows = result.fetchall()
        if len(rows) == 0:
            return None
        else:
            return rows[0]._asdict()

def add_application_to_db(job_id, data):
    with engine.connect() as conn:
        query = text("""
            INSERT INTO applications 
            (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) 
            VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)
        """)

        params = {
            "job_id": job_id,
            "full_name": data["full_name"],
            "email": data["email"],
            "linkedin_url": data.get("linkedin_url"),  # Use .get() to avoid KeyErrors if missing
            "education": data.get("education"),
            "work_experience": data.get("work_experience"),
            "resume_url": data.get("resume_url")
        }

        conn.execute(query, params)  # ✅ Pass parameters as a dictionary
        conn.commit()  # ✅ Commit changes
