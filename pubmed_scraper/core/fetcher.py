# ==== pubmed_scraper/core/fetcher.py ====
"""Fetcher module for retrieving data from PubMed API."""

import requests
import logging
from typing import Optional

from ..config import PUBMED_BASE_URL, DEFAULT_MAX_RESULTS

logger = logging.getLogger(__name__)

def fetch_pubmed_data(query: str, max_results: int = DEFAULT_MAX_RESULTS) -> str:
    """
    Fetch PubMed data for a given search query.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to fetch
        
    Returns:
        XML data as string
        
    Raises:
        requests.RequestException: If API request fails
    """
    logger.debug(f"Searching PubMed for: '{query}' (max_results: {max_results})")
    
    # Step 1: Search for article IDs
    esearch_url = f"{PUBMED_BASE_URL}/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,
    }
    
    try:
        response = requests.get(esearch_url, params=search_params, timeout=30)
        response.raise_for_status()
        search_result = response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to search PubMed: {e}")
        raise
    except ValueError as e:
        logger.error(f"Invalid JSON response from PubMed search: {e}")
        raise requests.RequestException(f"Invalid JSON response: {e}")

    # Extract article IDs
    esearch_result = search_result.get("esearchresult", {})
    ids = esearch_result.get("idlist", [])
    
    if not ids:
        logger.info("No articles found for the given query")
        return ""

    logger.debug(f"Found {len(ids)} article IDs")

    # Step 2: Fetch detailed article information
    efetch_url = f"{PUBMED_BASE_URL}/efetch.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml"
    }
    
    try:
        response = requests.get(efetch_url, params=fetch_params, timeout=60)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logger.error(f"Failed to fetch PubMed articles: {e}")
        raise
