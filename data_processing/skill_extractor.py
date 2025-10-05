"""
Skill extraction from job descriptions
Uses keyword matching and NLP techniques
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import json
import re
import logging
from typing import List, Dict, Set
import pandas as pd
from collections import Counter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SkillExtractor:
    """Extract skills from job descriptions"""
    
    def __init__(self, skill_keywords_path: str = None):
        """
        Initialize skill extractor with keyword dictionary
        
        Args:
            skill_keywords_path: Path to skill_keywords.json
        """
        if skill_keywords_path is None:
            skill_keywords_path = Path(__file__).parent / 'skill_keywords.json'
        
        self.skill_keywords = self._load_skill_keywords(skill_keywords_path)
        self.all_skills = self._flatten_skills()
        self.skill_patterns = self._compile_patterns()
        
        logger.info(f"Loaded {len(self.all_skills)} unique skills")
    
    def _load_skill_keywords(self, path: str) -> Dict[str, List[str]]:
        """Load skill keywords from JSON file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading skill keywords: {e}")
            return {}
    
    def _flatten_skills(self) -> Set[str]:
        """Flatten skill dictionary into a single set of all skills"""
        all_skills = set()
        for category, skills in self.skill_keywords.items():
            all_skills.update([skill.lower() for skill in skills])
        return all_skills
    
    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """
        Compile regex patterns for each skill
        Creates word boundary patterns to avoid partial matches
        """
        patterns = {}
        for skill in self.all_skills:
            # Escape special regex characters
            escaped_skill = re.escape(skill)
            # Create word boundary pattern (case-insensitive)
            pattern = re.compile(r'\b' + escaped_skill + r'\b', re.IGNORECASE)
            patterns[skill] = pattern
        
        return patterns
    
    def extract_skills_from_text(self, text: str) -> List[str]:
        """
        Extract skills from a text using keyword matching
        
        Args:
            text: Job description or any text to extract skills from
            
        Returns:
            List of found skills (deduplicated)
        """
        if not text or not isinstance(text, str):
            return []
        
        # Clean text
        text = self._clean_text(text)
        
        found_skills = []
        
        # Match each skill pattern
        for skill, pattern in self.skill_patterns.items():
            if pattern.search(text):
                # Find the original case from skill_keywords
                original_skill = self._get_original_case(skill)
                found_skills.append(original_skill)
        
        return list(set(found_skills))  # Remove duplicates
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for better matching"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Remove special characters but keep alphanumeric, spaces, and common punctuation
        text = re.sub(r'[^\w\s.#+\-]', ' ', text)
        return text
    
    def _get_original_case(self, skill_lower: str) -> str:
        """Get original case of skill from skill_keywords"""
        for category, skills in self.skill_keywords.items():
            for skill in skills:
                if skill.lower() == skill_lower:
                    return skill
        return skill_lower.title()  # Fallback to title case
    
    def extract_skills_from_dataframe(self, df: pd.DataFrame, 
                                     description_column: str = 'description') -> Dict[int, List[str]]:
        """
        Extract skills from all job descriptions in a DataFrame
        
        Args:
            df: DataFrame containing job data
            description_column: Name of column containing job descriptions
            
        Returns:
            Dictionary mapping DataFrame index to list of extracted skills
        """
        logger.info(f"Extracting skills from {len(df)} job descriptions...")
        
        skills_by_job = {}
        skill_counts = Counter()
        
        for idx, row in df.iterrows():
            description = row.get(description_column, '')
            
            # Also check job title for skills
            title = row.get('title', '')
            combined_text = f"{title} {description}"
            
            skills = self.extract_skills_from_text(combined_text)
            skills_by_job[idx] = skills
            
            # Update skill counts
            skill_counts.update(skills)
            
            # Progress logging
            if (idx + 1) % 100 == 0:
                logger.info(f"Processed {idx + 1}/{len(df)} jobs")
        
        # Log statistics
        logger.info(f"\n{'='*50}")
        logger.info(f"Skill Extraction Complete!")
        logger.info(f"Total jobs processed: {len(df)}")
        logger.info(f"Jobs with skills found: {sum(1 for s in skills_by_job.values() if s)}")
        logger.info(f"Unique skills found: {len(skill_counts)}")
        logger.info(f"\nTop 10 most common skills:")
        for skill, count in skill_counts.most_common(10):
            logger.info(f"  {skill}: {count}")
        logger.info(f"{'='*50}\n")
        
        return skills_by_job
    
    def get_skill_category(self, skill_name: str) -> str:
        """Get the category of a skill"""
        skill_lower = skill_name.lower()
        for category, skills in self.skill_keywords.items():
            if any(s.lower() == skill_lower for s in skills):
                return category.replace('_', ' ').title()
        return "Other"
    
    def get_skills_by_category(self, extracted_skills: List[str]) -> Dict[str, List[str]]:
        """Group extracted skills by their categories"""
        categorized = {}
        for skill in extracted_skills:
            category = self.get_skill_category(skill)
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(skill)
        return categorized
    
    def analyze_skill_combinations(self, skills_by_job: Dict[int, List[str]], 
                                  min_count: int = 5) -> List[tuple]:
        """
        Analyze which skills frequently appear together
        
        Args:
            skills_by_job: Dictionary mapping job ID to list of skills
            min_count: Minimum co-occurrence count to include
            
        Returns:
            List of tuples (skill1, skill2, count) sorted by count
        """
        from itertools import combinations
        
        co_occurrences = Counter()
        
        for skills in skills_by_job.values():
            if len(skills) < 2:
                continue
            
            # Generate all pairs of skills in this job
            for skill1, skill2 in combinations(sorted(skills), 2):
                co_occurrences[(skill1, skill2)] += 1
        
        # Filter by minimum count and sort
        filtered = [(s1, s2, count) for (s1, s2), count in co_occurrences.items() 
                   if count >= min_count]
        filtered.sort(key=lambda x: x[2], reverse=True)
        
        return filtered


class AdvancedSkillExtractor(SkillExtractor):
    """
    Advanced skill extraction using NLP (for Phase 2)
    Currently a placeholder - can be enhanced with spaCy
    """
    
    def __init__(self, skill_keywords_path: str = None, use_nlp: bool = False):
        super().__init__(skill_keywords_path)
        self.use_nlp = use_nlp
        self.nlp = None
        
        if use_nlp:
            try:
                import spacy
                # Try to load spaCy model
                try:
                    self.nlp = spacy.load('en_core_web_sm')
                    logger.info("✓ Loaded spaCy model for advanced NLP")
                except OSError:
                    logger.warning("spaCy model not found. Run: python -m spacy download en_core_web_sm")
                    self.use_nlp = False
            except ImportError:
                logger.warning("spaCy not installed. Using basic keyword matching only.")
                self.use_nlp = False
    
    def extract_skills_with_nlp(self, text: str) -> List[str]:
        """
        Enhanced skill extraction using NLP
        (Placeholder for future enhancement)
        """
        # Start with keyword-based extraction
        skills = self.extract_skills_from_text(text)
        
        if not self.use_nlp or not self.nlp:
            return skills
        
        # TODO: Add NLP-based extraction
        # - Named entity recognition for tech terms
        # - Skill inference from context
        # - Synonym matching
        
        return skills


def main():
    """Test skill extraction"""
    
    # Sample job descriptions for testing
    test_jobs = pd.DataFrame([
        {
            'title': 'Senior Python Developer',
            'description': '''
            We are looking for a Senior Python Developer with 5+ years of experience.
            Required skills: Python, Django, Flask, REST API, PostgreSQL, Docker, AWS.
            Experience with React and JavaScript is a plus.
            Should have strong problem-solving skills and team collaboration experience.
            '''
        },
        {
            'title': 'Data Analyst',
            'description': '''
            Seeking a Data Analyst proficient in SQL, Python, and Excel.
            Experience with Tableau, Power BI for data visualization.
            Knowledge of statistics, A/B testing, and Pandas is required.
            Machine Learning experience is beneficial.
            '''
        },
        {
            'title': 'Full Stack Engineer',
            'description': '''
            Full Stack Engineer role requiring Node.js, React, MongoDB experience.
            Must know JavaScript, TypeScript, HTML, CSS.
            Docker, Kubernetes, and CI/CD pipeline experience preferred.
            Agile/Scrum methodology knowledge essential.
            '''
        }
    ])
    
    # Initialize extractor
    extractor = SkillExtractor()
    
    # Extract skills
    skills_by_job = extractor.extract_skills_from_dataframe(test_jobs)
    
    # Display results
    print("\n" + "="*50)
    print("SKILL EXTRACTION RESULTS")
    print("="*50)
    
    for idx, row in test_jobs.iterrows():
        print(f"\nJob: {row['title']}")
        print(f"Skills found: {', '.join(skills_by_job[idx])}")
        
        # Show categorized skills
        categorized = extractor.get_skills_by_category(skills_by_job[idx])
        print("\nBy Category:")
        for category, skills in categorized.items():
            print(f"  {category}: {', '.join(skills)}")
    
    # Analyze skill combinations
    print("\n" + "="*50)
    print("SKILL CO-OCCURRENCES")
    print("="*50)
    
    combinations = extractor.analyze_skill_combinations(skills_by_job, min_count=1)
    for skill1, skill2, count in combinations[:10]:
        print(f"{skill1} + {skill2}: {count} times")


if __name__ == "__main__":
    main()