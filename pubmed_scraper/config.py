"""Configuration settings for the PubMed scraper."""

from typing import List

# PubMed API configuration
PUBMED_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
DEFAULT_MAX_RESULTS = 50

# Keywords to identify academic institutions (case-insensitive)
ACADEMIC_KEYWORDS: List[str] = [
    "university", "college", "school", "institute", "faculty", 
    "department", "hospital", "clinic", "medical center", 
    "research center", "academic", "campus", "laboratory",
    "lab", "centre", "institut", "universidad", "université"
]

# Keywords that suggest pharmaceutical/biotech companies
PHARMA_BIOTECH_KEYWORDS: List[str] = [
    "pharmaceutical", "pharma", "biotech", "biotechnology",
    "drug", "therapeutics", "medicines", "biopharmaceutical",
    "inc", "ltd", "llc", "corp", "corporation", "company",
    "ag", "gmbh", "sa", "plc"
]
