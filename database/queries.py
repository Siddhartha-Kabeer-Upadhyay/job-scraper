"""
Predefined SQL queries for analytics and reporting
"""

# ==================== SKILL ANALYSIS QUERIES ====================

TOP_SKILLS_OVERALL = """
    SELECT 
        s.skill_name,
        s.skill_category,
        COUNT(DISTINCT js.job_id) as job_count,
        ROUND(COUNT(DISTINCT js.job_id) * 100.0 / (SELECT COUNT(*) FROM jobs), 2) as percentage
    FROM skills s
    JOIN job_skills js ON s.skill_id = js.skill_id
    GROUP BY s.skill_id, s.skill_name, s.skill_category
    ORDER BY job_count DESC
    LIMIT %s
"""

TOP_SKILLS_BY_LOCATION = """
    SELECT 
        l.city,
        s.skill_name,
        COUNT(DISTINCT j.job_id) as job_count
    FROM skills s
    JOIN job_skills js ON s.skill_id = js.skill_id
    JOIN jobs j ON js.job_id = j.job_id
    JOIN locations l ON j.location_id = l.location_id
    WHERE l.city = %s
    GROUP BY l.city, s.skill_name
    ORDER BY job_count DESC
    LIMIT %s
"""

TOP_SKILLS_BY_ROLE = """
    SELECT 
        j.job_title,
        s.skill_name,
        COUNT(*) as frequency
    FROM jobs j
    JOIN job_skills js ON j.job_id = js.job_id
    JOIN skills s ON js.skill_id = s.skill_id
    WHERE LOWER(j.job_title) LIKE LOWER(%s)
    GROUP BY j.job_title, s.skill_name
    ORDER BY frequency DESC
    LIMIT %s
"""

SKILL_COOCCURRENCE = """
    WITH skill_pairs AS (
        SELECT 
            js1.skill_id as skill1_id,
            js2.skill_id as skill2_id,
            COUNT(DISTINCT js1.job_id) as co_occurrence_count
        FROM job_skills js1
        JOIN job_skills js2 ON js1.job_id = js2.job_id AND js1.skill_id < js2.skill_id
        GROUP BY js1.skill_id, js2.skill_id
        HAVING COUNT(DISTINCT js1.job_id) >= %s
    )
    SELECT 
        s1.skill_name as skill_1,
        s2.skill_name as skill_2,
        sp.co_occurrence_count
    FROM skill_pairs sp
    JOIN skills s1 ON sp.skill1_id = s1.skill_id
    JOIN skills s2 ON sp.skill2_id = s2.skill_id
    ORDER BY sp.co_occurrence_count DESC
    LIMIT %s
"""

# ==================== COMPANY ANALYSIS QUERIES ====================

TOP_HIRING_COMPANIES = """
    SELECT 
        c.company_name,
        COUNT(j.job_id) as job_count,
        COUNT(DISTINCT l.city) as cities_hiring_in
    FROM companies c
    JOIN jobs j ON c.company_id = j.company_id
    LEFT JOIN locations l ON j.location_id = l.location_id
    GROUP BY c.company_id, c.company_name
    ORDER BY job_count DESC
    LIMIT %s
"""

COMPANIES_BY_CITY = """
    SELECT 
        l.city,
        c.company_name,
        COUNT(j.job_id) as job_count
    FROM companies c
    JOIN jobs j ON c.company_id = j.company_id
    JOIN locations l ON j.location_id = l.location_id
    WHERE l.city = %s
    GROUP BY l.city, c.company_name
    ORDER BY job_count DESC
    LIMIT %s
"""

# ==================== LOCATION ANALYSIS QUERIES ====================

JOBS_BY_CITY = """
    SELECT 
        l.city,
        l.state,
        COUNT(j.job_id) as job_count,
        COUNT(DISTINCT c.company_id) as company_count
    FROM locations l
    LEFT JOIN jobs j ON l.location_id = j.location_id
    LEFT JOIN companies c ON j.company_id = c.company_id
    GROUP BY l.location_id, l.city, l.state
    ORDER BY job_count DESC
"""

# ==================== EXPERIENCE LEVEL ANALYSIS ====================

EXPERIENCE_DEMAND_BY_SKILL = """
    SELECT 
        s.skill_name,
        j.experience_level,
        COUNT(*) as job_count
    FROM skills s
    JOIN job_skills js ON s.skill_id = js.skill_id
    JOIN jobs j ON js.job_id = j.job_id
    WHERE s.skill_name = %s AND j.experience_level IS NOT NULL
    GROUP BY s.skill_name, j.experience_level
    ORDER BY job_count DESC
"""

EXPERIENCE_DISTRIBUTION = """
    SELECT 
        experience_level,
        COUNT(*) as job_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM jobs WHERE experience_level IS NOT NULL), 2) as percentage
    FROM jobs
    WHERE experience_level IS NOT NULL
    GROUP BY experience_level
    ORDER BY job_count DESC
"""

# ==================== SALARY ANALYSIS QUERIES ====================

SALARY_BY_SKILL = """
    SELECT 
        s.skill_name,
        AVG(j.salary_min) as avg_min_salary,
        AVG(j.salary_max) as avg_max_salary,
        COUNT(*) as job_count
    FROM skills s
    JOIN job_skills js ON s.skill_id = js.skill_id
    JOIN jobs j ON js.job_id = j.job_id
    WHERE j.salary_min IS NOT NULL 
      AND j.salary_max IS NOT NULL
      AND j.salary_min > 0
      AND j.salary_max > j.salary_min
    GROUP BY s.skill_name
    HAVING COUNT(*) >= %s
    ORDER BY avg_max_salary DESC
    LIMIT %s
"""

SALARY_BY_CITY = """
    SELECT 
        l.city,
        AVG(j.salary_min) as avg_min_salary,
        AVG(j.salary_max) as avg_max_salary,
        COUNT(*) as job_count
    FROM locations l
    JOIN jobs j ON l.location_id = j.location_id
    WHERE j.salary_min IS NOT NULL 
      AND j.salary_max IS NOT NULL
      AND j.salary_min > 0
      AND j.salary_max > j.salary_min
    GROUP BY l.city
    ORDER BY avg_max_salary DESC
"""


# ==================== PORTAL ANALYSIS ====================

JOBS_BY_PORTAL = """
    SELECT 
        source_portal,
        COUNT(*) as job_count,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM jobs), 2) as percentage
    FROM jobs
    WHERE source_portal IS NOT NULL
    GROUP BY source_portal
    ORDER BY job_count DESC
"""

# ==================== SEARCH QUERIES ====================

SEARCH_JOBS = """
    SELECT 
        j.job_id,
        j.job_title,
        c.company_name,
        l.city,
        j.experience_level,
        j.job_type,
        j.job_url,
        j.posted_date
    FROM jobs j
    LEFT JOIN companies c ON j.company_id = c.company_id
    LEFT JOIN locations l ON j.location_id = l.location_id
    WHERE 
        (LOWER(j.job_title) LIKE LOWER(%s) OR %s IS NULL)
        AND (l.city = %s OR %s IS NULL)
        AND (c.company_name = %s OR %s IS NULL)
    ORDER BY j.created_at DESC
    LIMIT %s
"""

JOBS_WITH_SKILL = """
    SELECT 
        j.job_id,
        j.job_title,
        c.company_name,
        l.city,
        j.job_url
    FROM jobs j
    JOIN job_skills js ON j.job_id = js.job_id
    JOIN skills s ON js.skill_id = s.skill_id
    LEFT JOIN companies c ON j.company_id = c.company_id
    LEFT JOIN locations l ON j.location_id = l.location_id
    WHERE LOWER(s.skill_name) = LOWER(%s)
    ORDER BY j.created_at DESC
    LIMIT %s
"""