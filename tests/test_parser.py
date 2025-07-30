# ==== tests/test_parser.py ====
"""Tests for XML parser functionality."""

import pytest
from pubmed_scraper.core.parser import (
    parse_pubmed_records, 
    parse_single_article, 
    extract_text,
    extract_publication_date,
    convert_month_name_to_number
)
import xml.etree.ElementTree as ET

class TestParsePubmedRecords:
    """Test cases for parsing PubMed XML records."""

    def test_parse_valid_xml(self, sample_xml):
        """Test parsing of valid XML data."""
        result = parse_pubmed_records(sample_xml)
        assert len(result) == 2
        
        # Check first article (with non-academic affiliations)
        first_article = result[0]
        assert first_article["PubmedID"] == "123456"
        assert first_article["Title"] == "Test COVID-19 Treatment Study"
        assert "John Doe" in first_article["Non-academic Author(s)"]
        assert "Bob Johnson" in first_article["Non-academic Author(s)"]
        assert "jane.smith" not in first_article["Non-academic Author(s)"]  # Academic author
        
        # Check second article (academic only)
        second_article = result[1]
        assert second_article["PubmedID"] == "789012"
        assert second_article["Non-academic Author(s)"] == ""  # No non-academic authors

    def test_parse_empty_xml(self, empty_xml):
        """Test parsing of empty XML data."""
        result = parse_pubmed_records(empty_xml)
        assert len(result) == 0

    def test_parse_malformed_xml(self, malformed_xml):
        """Test handling of malformed XML."""
        result = parse_pubmed_records(malformed_xml)
        assert len(result) == 0

    def test_parse_empty_string(self):
        """Test parsing of empty string."""
        result = parse_pubmed_records("")
        assert len(result) == 0

    def test_parse_none_input(self):
        """Test parsing of None input."""
        result = parse_pubmed_records(None)
        assert len(result) == 0

class TestParseSingleArticle:
    """Test cases for parsing individual articles."""

    def test_parse_article_with_affiliations(self, sample_xml):
        """Test parsing article with mixed affiliations."""
        root = ET.fromstring(sample_xml)
        article = root.find(".//PubmedArticle")
        
        result = parse_single_article(article)
        assert result is not None
        assert result["PubmedID"] == "123456"
        assert "Pfizer Inc." in result["Company Affiliation(s)"]
        assert "Moderna Inc." in result["Company Affiliation(s)"]
        assert "Harvard Medical School" not in result["Company Affiliation(s)"]

    def test_parse_article_academic_only(self, sample_xml):
        """Test parsing article with only academic affiliations."""
        root = ET.fromstring(sample_xml)
        articles = root.findall(".//PubmedArticle")
        academic_article = articles[1]  # Second article is academic only
        
        result = parse_single_article(academic_article)
        assert result is not None
        assert result["Non-academic Author(s)"] == ""
        assert result["Company Affiliation(s)"] == ""

class TestExtractText:
    """Test cases for text extraction from XML elements."""

    def test_extract_existing_text(self, sample_xml):
        """Test extraction of existing text elements."""
        root = ET.fromstring(sample_xml)
        article = root.find(".//PubmedArticle")
        
        pmid = extract_text(article, ".//PMID")
        assert pmid == "123456"
        
        title = extract_text(article, ".//ArticleTitle")
        assert title == "Test COVID-19 Treatment Study"

    def test_extract_nonexistent_text(self, sample_xml):
        """Test extraction of non-existent elements."""
        root = ET.fromstring(sample_xml)
        article = root.find(".//PubmedArticle")
        
        result = extract_text(article, ".//NonExistentElement")
        assert result is None

class TestExtractPublicationDate:
    """Test cases for publication date extraction."""

    def test_extract_complete_date(self, sample_xml):
        """Test extraction of complete publication date."""
        root = ET.fromstring(sample_xml)
        article = root.find(".//PubmedArticle")
        
        date = extract_publication_date(article)
        assert date == "2023-07-01"

    def test_extract_year_month_only(self):
        """Test extraction when only year and month are available."""
        xml = '''<Article>
            <DateRevised>
                <Year>2023</Year>
                <Month>07</Month>
            </DateRevised>
        </Article>'''
        article = ET.fromstring(xml)
        
        date = extract_publication_date(article)
        assert date == "2023-07"

    def test_extract_year_only(self):
        """Test extraction when only year is available."""
        xml = '''<Article>
            <DateRevised>
                <Year>2023</Year>
            </DateRevised>
        </Article>'''
        article = ET.fromstring(xml)
        
        date = extract_publication_date(article)
        assert date == "2023"

    def test_no_date_available(self):
        """Test when no publication date is available."""
        xml = '''<Article></Article>'''
        article = ET.fromstring(xml)
        
        date = extract_publication_date(article)
        assert date == ""

class TestConvertMonthNameToNumber:
    """Test cases for month name conversion."""

    def test_convert_standard_months(self):
        """Test conversion of standard month abbreviations."""
        assert convert_month_name_to_number("Jan") == "1"
        assert convert_month_name_to_number("Feb") == "2"
        assert convert_month_name_to_number("Mar") == "3"
        assert convert_month_name_to_number("Dec") == "12"

    def test_convert_full_month_names(self):
        """Test conversion of full month names."""
        assert convert_month_name_to_number("January") == "1"
        assert convert_month_name_to_number("February") == "2"
        assert convert_month_name_to_number("December") == "12"

    def test_convert_numeric_months(self):
        """Test that numeric months are returned as-is."""
        assert convert_month_name_to_number("01") == "01"
        assert convert_month_name_to_number("12") == "12"

    def test_convert_unknown_month(self):
        """Test handling of unknown month formats."""
        assert convert_month_name_to_number("Unknown") == "Unknown"
        assert convert_month_name_to_number("") == ""