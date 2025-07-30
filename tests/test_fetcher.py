# ==== tests/test_fetcher.py ====
"""Tests for PubMed API fetcher functionality."""

import pytest
import requests
from unittest.mock import Mock, patch
from pubmed_scraper.core.fetcher import fetch_pubmed_data

class TestFetchPubmedData:
    """Test cases for PubMed data fetching."""

    @patch('pubmed_scraper.core.fetcher.requests.get')
    def test_successful_fetch(self, mock_get):
        """Test successful data fetching from PubMed."""
        # Mock search response
        search_response = Mock()
        search_response.json.return_value = {
            "esearchresult": {
                "idlist": ["123456", "789012"]
            }
        }
        search_response.raise_for_status.return_value = None
        
        # Mock fetch response
        fetch_response = Mock()
        fetch_response.text = "<PubmedArticleSet>Mock XML</PubmedArticleSet>"
        fetch_response.raise_for_status.return_value = None
        
        mock_get.side_effect = [search_response, fetch_response]
        
        result = fetch_pubmed_data("covid-19", max_results=50)
        assert result == "<PubmedArticleSet>Mock XML</PubmedArticleSet>"
        assert mock_get.call_count == 2

    @patch('pubmed_scraper.core.fetcher.requests.get')
    def test_no_results_found(self, mock_get):
        """Test handling when no results are found."""
        search_response = Mock()
        search_response.json.return_value = {
            "esearchresult": {
                "idlist": []
            }
        }
        search_response.raise_for_status.return_value = None
        
        mock_get.return_value = search_response
        
        result = fetch_pubmed_data("nonexistent-query")
        assert result == ""
        assert mock_get.call_count == 1

    @patch('pubmed_scraper.core.fetcher.requests.get')
    def test_search_api_failure(self, mock_get):
        """Test handling of search API failures."""
        mock_get.side_effect = requests.RequestException("API Error")
        
        with pytest.raises(requests.RequestException):
            fetch_pubmed_data("covid-19")

    @patch('pubmed_scraper.core.fetcher.requests.get')
    def test_invalid_json_response(self, mock_get):
        """Test handling of invalid JSON response."""
        search_response = Mock()
        search_response.json.side_effect = ValueError("Invalid JSON")
        search_response.raise_for_status.return_value = None
        
        mock_get.return_value = search_response
        
        with pytest.raises(requests.RequestException):
            fetch_pubmed_data("covid-19")

    @patch('pubmed_scraper.core.fetcher.requests.get')
    def test_fetch_api_failure(self, mock_get):
        """Test handling of fetch API failures."""
        # Successful search
        search_response = Mock()
        search_response.json.return_value = {
            "esearchresult": {
                "idlist": ["123456"]
            }
        }
        search_response.raise_for_status.return_value = None
        
        # Failed fetch
        fetch_response = Mock()
        fetch_response.raise_for_status.side_effect = requests.RequestException("Fetch failed")
        
        mock_get.side_effect = [search_response, fetch_response]
        
        with pytest.raises(requests.RequestException):
            fetch_pubmed_data("covid-19")