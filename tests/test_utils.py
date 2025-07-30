"""Tests for utility functions."""

import pytest
from pubmed_scraper.core.utils import is_non_academic_affiliation, extract_emails

class TestIsNonAcademicAffiliation:
    """Test cases for non-academic affiliation detection."""

    def test_pharmaceutical_companies(self):
        """Test detection of pharmaceutical companies."""
        assert is_non_academic_affiliation("Pfizer Inc.") is True
        assert is_non_academic_affiliation("Moderna Inc., Cambridge, MA") is True
        assert is_non_academic_affiliation("Roche Pharma Research & Early Development") is True
        assert is_non_academic_affiliation("Johnson & Johnson Pharmaceutical Research") is True
        assert is_non_academic_affiliation("Novartis AG, Basel, Switzerland") is True

    def test_biotech_companies(self):
        """Test detection of biotech companies."""
        assert is_non_academic_affiliation("Genentech Inc.") is True
        assert is_non_academic_affiliation("Amgen Biotechnology") is True
        assert is_non_academic_affiliation("BioNTech SE, Germany") is True
        assert is_non_academic_affiliation("Biogen Corp.") is True

    def test_academic_institutions(self):
        """Test that academic institutions are correctly identified as academic."""
        assert is_non_academic_affiliation("Harvard University") is False
        assert is_non_academic_affiliation("Stanford Medical School") is False
        assert is_non_academic_affiliation("Massachusetts Institute of Technology") is False
        assert is_non_academic_affiliation("University of California, San Francisco") is False
        assert is_non_academic_affiliation("Johns Hopkins Hospital") is False
        assert is_non_academic_affiliation("Mayo Clinic") is False
        assert is_non_academic_affiliation("Cancer Research Institute") is False

    def test_mixed_affiliations(self):
        """Test affiliations with both academic and corporate indicators."""
        # Corporate should override academic when corporate indicators are present
        assert is_non_academic_affiliation("Pfizer Research Institute Inc.") is True
        assert is_non_academic_affiliation("Roche Institute of Molecular Biology Corp.") is True
        
        # Pure academic research institutes should remain academic
        assert is_non_academic_affiliation("Cold Spring Harbor Laboratory") is False
        assert is_non_academic_affiliation("Broad Institute of MIT and Harvard") is False

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        assert is_non_academic_affiliation("") is False
        assert is_non_academic_affiliation(None) is False
        assert is_non_academic_affiliation("   ") is False
        assert is_non_academic_affiliation("Some random text") is False

    def test_case_insensitive(self):
        """Test that detection is case insensitive."""
        assert is_non_academic_affiliation("PFIZER INC.") is True
        assert is_non_academic_affiliation("pfizer inc.") is True
        assert is_non_academic_affiliation("Pfizer INC.") is True
        assert is_non_academic_affiliation("HARVARD UNIVERSITY") is False
        assert is_non_academic_affiliation("harvard university") is False

    def test_international_companies(self):
        """Test detection of international company formats."""
        assert is_non_academic_affiliation("Novartis AG") is True
        assert is_non_academic_affiliation("Sanofi SA") is True
        assert is_non_academic_affiliation("Bayer AG") is True
        assert is_non_academic_affiliation("AstraZeneca PLC") is True

class TestExtractEmails:
    """Test cases for email extraction."""

    def test_single_email(self):
        """Test extraction of single email address."""
        text = "Contact: john.doe@pfizer.com"
        emails = extract_emails(text)
        assert "john.doe@pfizer.com" in emails
        assert len(emails) == 1

    def test_multiple_emails(self):
        """Test extraction of multiple email addresses."""
        text = "Contact: john.doe@pfizer.com; jane.smith@moderna.com"
        emails = extract_emails(text)
        assert "john.doe@pfizer.com" in emails
        assert "jane.smith@moderna.com" in emails
        assert len(emails) == 2

    def test_emails_in_mixed_text(self):
        """Test extraction from text with mixed content."""
        text = "Pfizer Inc., New York, USA. Correspondence: john.doe@pfizer.com. Additional contact: jane@pfizer.com"
        emails = extract_emails(text)
        assert "john.doe@pfizer.com" in emails
        assert "jane@pfizer.com" in emails

    def test_no_emails(self):
        """Test text with no email addresses."""
        text = "Pfizer Inc., New York, USA"
        emails = extract_emails(text)
        assert len(emails) == 0

    def test_invalid_emails(self):
        """Test that invalid email formats are not extracted."""
        text = "Invalid emails: @pfizer.com, john.doe@, incomplete@"
        emails = extract_emails(text)
        assert len(emails) == 0

    def test_duplicate_emails(self):
        """Test that duplicate emails are handled correctly."""
        text = "john.doe@pfizer.com and john.doe@pfizer.com again"
        emails = extract_emails(text)
        assert len(emails) == 1
        assert "john.doe@pfizer.com" in emails

    def test_edge_cases(self):
        """Test edge cases for email extraction."""
        assert extract_emails("") == []
        assert extract_emails(None) == []
        assert extract_emails("No emails here") == []

    def test_complex_email_formats(self):
        """Test various valid email formats."""
        text = "Contacts: first.last@company.com, user+tag@example.org, user_name@sub.domain.co.uk"
        emails = extract_emails(text)
        assert "first.last@company.com" in emails
        assert "user+tag@example.org" in emails
        assert "user_name@sub.domain.co.uk" in emails
        assert len(emails) == 3