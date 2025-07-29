# ==== pubmed_scraper/core/utils.py ====
"""Utility functions for PubMed scraper."""

import re
from typing import List

from ..config import ACADEMIC_KEYWORDS, PHARMA_BIOTECH_KEYWORDS

def is_non_academic_affiliation(affiliation: str) -> bool:
    """
    Check if an affiliation string represents a non-academic organization.
    
    This function uses heuristics to identify pharmaceutical/biotech companies
    and other non-academic institutions.
    
    Args:
        affiliation: The affiliation string to check
        
    Returns:
        True if the affiliation appears to be non-academic, False otherwise
    """
    if not affiliation or not affiliation.strip():
        return False
        
    affiliation_lower = affiliation.lower()
    
    # First check if it contains academic keywords
    has_academic_keywords = any(keyword in affiliation_lower for keyword in ACADEMIC_KEYWORDS)
    
    # If it has academic keywords, it's likely academic
    if has_academic_keywords:
        # However, some companies have "research" or "institute" in their name
        # Check if it also has strong pharma/biotech indicators
        has_pharma_keywords = any(keyword in affiliation_lower for keyword in PHARMA_BIOTECH_KEYWORDS)
        
        # If it has both academic and pharma keywords, do additional checks
        if has_pharma_keywords:
            # Look for corporate indicators that override academic keywords
            corporate_indicators = ["inc", "ltd", "llc", "corp", "corporation", "company", "ag", "gmbh", "sa", "plc"]
            has_corporate = any(indicator in affiliation_lower for indicator in corporate_indicators)
            return has_corporate
        
        return False
    
    # If no academic keywords, check for pharma/biotech indicators
    has_pharma_keywords = any(keyword in affiliation_lower for keyword in PHARMA_BIOTECH_KEYWORDS)
    
    # Additional heuristics for non-academic organizations
    corporate_patterns = [
        r'\b(inc|ltd|llc|corp|corporation|company)\b',
        r'\b(ag|gmbh|sa|plc)\b',
        r'\b(pharmaceutical|pharma|biotech|biotechnology)\b',
        r'\b(drug|therapeutics|medicines)\b'
    ]
    
    has_corporate_pattern = any(re.search(pattern, affiliation_lower) for pattern in corporate_patterns)
    
    return has_pharma_keywords or has_corporate_pattern

def extract_emails(text: str) -> List[str]:
    """
    Extract email addresses from a text string.
    
    Args:
        text: The text to search for email addresses
        
    Returns:
        List of unique email addresses found in the text
    """
    if not text:
        return []
    
    # Comprehensive email regex pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    
    # Return unique emails, preserving order
    unique_emails = []
    for email in emails:
        if email not in unique_emails:
            unique_emails.append(email)
    
    return unique_emails
