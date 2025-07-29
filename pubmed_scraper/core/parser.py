# ==== pubmed_scraper/core/parser.py ====
"""Parser module for processing PubMed XML data."""

from typing import List, Dict, Optional
import xml.etree.ElementTree as ET
import logging

from .utils import is_non_academic_affiliation, extract_emails

logger = logging.getLogger(__name__)

def parse_pubmed_records(xml_data: str) -> List[Dict[str, str]]:
    """
    Parse PubMed XML data and extract relevant information.
    
    Args:
        xml_data: XML data string from PubMed API
        
    Returns:
        List of dictionaries containing parsed article information
    """
    if not xml_data.strip():
        logger.warning("Empty XML data provided")
        return []
    
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        logger.error(f"Failed to parse XML: {e}")
        return []
    
    results = []
    articles = root.findall(".//PubmedArticle")
    logger.info(f"Found {len(articles)} articles to process")

    for article in articles:
        try:
            record = parse_single_article(article)
            if record:
                results.append(record)
        except Exception as e:
            logger.debug(f"Error processing article: {e}")
            continue

    logger.info(f"Successfully processed {len(results)} records")
    return results

def parse_single_article(article: ET.Element) -> Optional[Dict[str, str]]:
    """
    Parse a single PubMed article element.
    
    Args:
        article: XML element representing a single article
        
    Returns:
        Dictionary with article information or None if parsing fails
    """
    # Extract basic article information
    pmid = extract_text(article, ".//PMID") or ""
    title = extract_text(article, ".//ArticleTitle") or ""
    
    # Extract publication date
    pubdate = extract_publication_date(article)
    
    # Process authors and affiliations
    non_academic_authors = []
    company_affiliations = []
    emails = []
    corresponding_emails = []
    
    # Check for corresponding author emails in different locations
    corresponding_emails.extend(extract_emails_from_elements(article, ".//AuthorList//Author//Email"))
    corresponding_emails.extend(extract_emails_from_elements(article, ".//DataBankList//DataBank//Name"))
    
    # Process each author
    for author in article.findall(".//Author"):
        last_name = extract_text(author, "LastName") or ""
        fore_name = extract_text(author, "ForeName") or ""
        initials = extract_text(author, "Initials") or ""
        
        # Build full name
        name_parts = [fore_name or initials, last_name]
        full_name = " ".join(part for part in name_parts if part).strip()
        
        # Process affiliations for this author
        author_affiliations = []
        for aff_info in author.findall(".//AffiliationInfo"):
            aff_text = extract_text(aff_info, "Affiliation")
            if aff_text:
                author_affiliations.append(aff_text)
                # Extract emails from affiliation text
                emails.extend(extract_emails(aff_text))
        
        # Check if any affiliation is non-academic
        has_non_academic = any(is_non_academic_affiliation(aff) for aff in author_affiliations)
        
        if has_non_academic and full_name:
            if full_name not in non_academic_authors:
                non_academic_authors.append(full_name)
            # Add non-academic affiliations to company list
            for aff in author_affiliations:
                if is_non_academic_affiliation(aff) and aff not in company_affiliations:
                    company_affiliations.append(aff)
    
    # Combine corresponding author emails
    all_emails = list(set(emails + corresponding_emails))
    
    # Create result record
    record = {
        "PubmedID": pmid,
        "Title": title,
        "Publication Date": pubdate,
        "Non-academic Author(s)": "; ".join(non_academic_authors),
        "Company Affiliation(s)": "; ".join(company_affiliations),
        "Corresponding Author Email": "; ".join(all_emails),
    }
    
    return record

def extract_text(element: ET.Element, xpath: str) -> Optional[str]:
    """Extract text from XML element using xpath."""
    try:
        found = element.find(xpath)
        return found.text.strip() if found is not None and found.text else None
    except Exception:
        return None

def extract_publication_date(article: ET.Element) -> str:
    """Extract publication date from article element."""
    pubdate_elem = article.find(".//PubDate")
    if pubdate_elem is None:
        return ""
    
    year = pubdate_elem.findtext("Year") or ""
    month = pubdate_elem.findtext("Month") or ""
    day = pubdate_elem.findtext("Day") or ""
    
    # Handle different date formats
    date_parts = []
    if year:
        date_parts.append(year)
    if month:
        # Convert month name to number if needed
        month_num = convert_month_name_to_number(month)
        date_parts.append(month_num.zfill(2) if month_num.isdigit() else month)
    if day:
        date_parts.append(day.zfill(2) if day.isdigit() else day)
    
    return "-".join(date_parts)

def convert_month_name_to_number(month_name: str) -> str:
    """Convert month name to number."""
    month_map = {
        "Jan": "1", "Feb": "2", "Mar": "3", "Apr": "4",
        "May": "5", "Jun": "6", "Jul": "7", "Aug": "8", 
        "Sep": "9", "Oct": "10", "Nov": "11", "Dec": "12"
    }
    return month_map.get(month_name[:3], month_name)

def extract_emails_from_elements(article: ET.Element, xpath: str) -> List[str]:
    """Extract emails from specific XML elements."""
    emails = []
    for element in article.findall(xpath):
        if element.text:
            emails.extend(extract_emails(element.text))
    return emails
