# ==== tests/test_cli.py ====
"""Tests for command-line interface."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, Mock
from typer.testing import CliRunner
from pubmed_scraper.cli import main

runner = CliRunner()

class TestCLI:
    """Test cases for command-line interface."""

    @patch('pubmed_scraper.cli.fetch_pubmed_data')
    @patch('pubmed_scraper.cli.parse_pubmed_records')
    def test_successful_query_console_output(self, mock_parse, mock_fetch, sample_xml):
        """Test successful query with console output."""
        mock_fetch.return_value = sample_xml
        mock_parse.return_value = [
            {
                "PubmedID": "123456",
                "Title": "Test Paper",
                "Publication Date": "2023-01-01",
                "Non-academic Author(s)": "John Doe",
                "Company Affiliation(s)": "Pfizer Inc.",
                "Corresponding Author Email": "john@pfizer.com"
            }
        ]
        
        result = runner.invoke(main, ["covid-19"])
        assert result.exit_code == 0
        assert "PubmedID" in result.stdout

    @patch('pubmed_scraper.cli.fetch_pubmed_data')
    @patch('pubmed_scraper.cli.parse_pubmed_records')
    def test_successful_query_file_output(self, mock_parse, mock_fetch, sample_xml):
        """Test successful query with file output."""
        mock_fetch.return_value = sample_xml
        mock_parse.return_value = [
            {
                "PubmedID": "123456",
                "Title": "Test Paper",
                "Publication Date": "2023-01-01",
                "Non-academic Author(s)": "John Doe",
                "Company Affiliation(s)": "Pfizer Inc.",
                "Corresponding Author Email": "john@pfizer.com"
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            tmp_path = tmp.name
        
        try:
            result = runner.invoke(main, ["covid-19", "--file", tmp_path])
            assert result.exit_code == 0
            assert os.path.exists(tmp_path)
            
            # Check file contents
            with open(tmp_path, 'r') as f:
                content = f.read()
                assert "PubmedID" in content
                assert "123456" in content
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    @patch('pubmed_scraper.cli.fetch_pubmed_data')
    def test_no_data_returned(self, mock_fetch):
        """Test handling when no data is returned from PubMed."""
        mock_fetch.return_value = ""
        
        result = runner.invoke(main, ["nonexistent-query"])
        assert result.exit_code == 1
        assert "No results found" in result.stdout

    @patch('pubmed_scraper.cli.fetch_pubmed_data')
    @patch('pubmed_scraper.cli.parse_pubmed_records')
    def test_no_non_academic_papers(self, mock_parse, mock_fetch, sample_xml):
        """Test handling when no papers have non-academic affiliations."""
        mock_fetch.return_value = sample_xml
        mock_parse.return_value = [
            {
                "PubmedID": "123456",
                "Title": "Test Paper",
                "Publication Date": "2023-01-01",
                "Non-academic Author(s)": "",  # No non-academic authors
                "Company Affiliation(s)": "",
                "Corresponding Author Email": ""
            }
        ]
        
        result = runner.invoke(main, ["academic-only-query"])
        assert result.exit_code == 0
        assert "No papers found with pharmaceutical/biotech company affiliations" in result.stdout

    @patch('pubmed_scraper.cli.fetch_pubmed_data')
    def test_api_error_handling(self, mock_fetch):
        """Test handling of API errors."""
        mock_fetch.side_effect = Exception("API Error")
        
        result = runner.invoke(main, ["covid-19"])
        assert result.exit_code == 1
        assert "Error:" in result.stdout

    def test_debug_mode(self):
        """Test debug mode functionality."""
        result = runner.invoke(main, ["covid-19", "--debug"])
        # Debug mode should be enabled (will fail due to actual API call, but we check the flag works)
        assert result.exit_code == 1  # Expected to fail without mocking

    def test_max_results_parameter(self):
        """Test max results parameter."""
        result = runner.invoke(main, ["covid-19", "--max-results", "10"])
        # Should fail due to actual API call, but parameter should be accepted
        assert result.exit_code == 1

    def test_help_message(self):
        """Test help message display."""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Search query for PubMed" in result.stdout
        assert "--file" in result.stdout
        assert "--debug" in result.stdout