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