DROP TABLE IF EXISTS job_skills CASCADE;
DROP TABLE IF EXISTS skills CASCADE;
DROP TABLE IF EXISTS jobs CASCADE;
DROP TABLE IF EXISTS locations CASCADE;
DROP TABLE IF EXISTS companies CASCADE;

-- Companies Table
CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Locations Table
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    UNIQUE(city, state)
);

-- Jobs Table
CREATE TABLE jobs (
    job_id SERIAL PRIMARY KEY,
    job_title VARCHAR(255) NOT NULL,
    company_id INT REFERENCES companies(company_id),
    location_id INT REFERENCES locations(location_id),
    job_description TEXT,
    job_url VARCHAR(500) UNIQUE,
    experience_level VARCHAR(50),
    job_type VARCHAR(50),
    salary_min DECIMAL(10, 2),
    salary_max DECIMAL(10, 2),
    posted_date DATE,
    source_portal VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Skills Table
CREATE TABLE skills (
    skill_id SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) UNIQUE NOT NULL,
    skill_category VARCHAR(50)
);

-- Job_Skills Junction Table (Many-to-Many)
CREATE TABLE job_skills (
    job_id INT REFERENCES jobs(job_id) ON DELETE CASCADE,
    skill_id INT REFERENCES skills(skill_id) ON DELETE CASCADE,
    PRIMARY KEY (job_id, skill_id)
);

-- Indexes for Performance
CREATE INDEX idx_jobs_company ON jobs(company_id);
CREATE INDEX idx_jobs_location ON jobs(location_id);
CREATE INDEX idx_jobs_title ON jobs(job_title);
CREATE INDEX idx_jobs_portal ON jobs(source_portal);
CREATE INDEX idx_job_skills_job ON job_skills(job_id);
CREATE INDEX idx_job_skills_skill ON job_skills(skill_id);
CREATE INDEX idx_skills_name ON skills(skill_name);
CREATE INDEX idx_skills_category ON skills(skill_category);

-- Insert initial locations (Indian tech cities)
INSERT INTO locations (city, state) VALUES
    ('Bengaluru', 'Karnataka'),
    ('Mumbai', 'Maharashtra'),
    ('Pune', 'Maharashtra'),
    ('Delhi', 'Delhi'),
    ('Hyderabad', 'Telangana'),
    ('Chennai', 'Tamil Nadu'),
    ('Noida', 'Uttar Pradesh'),
    ('Gurugram', 'Haryana')
ON CONFLICT DO NOTHING;