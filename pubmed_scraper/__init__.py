# ==== pubmed_scraper/__init__.py ====
"""PubMed Scraper - A tool to fetch and parse PubMed data for pharmaceutical/biotech affiliations."""

__version__ = "0.1.0"

from .core.fetcher import fetch_pubmed_data
from .core.parser import parse_pubmed_records
from .core.utils import is_non_academic_affiliation, extract_emails

__all__ = [
    "fetch_pubmed_data",
    "parse_pubmed_records", 
    "is_non_academic_affiliation",
    "extract_emails"
]
