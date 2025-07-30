# ==== tests/conftest.py ====
"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path

@pytest.fixture
def sample_xml():
    """Sample PubMed XML data for testing."""
    return '''<?xml version="1.0" ?>
    <PubmedArticleSet>
        <PubmedArticle>
            <MedlineCitation Status="MEDLINE" Owner="NLM">
                <PMID Version="1">123456</PMID>
                <Article PubModel="Print">
                    <ArticleTitle>Test COVID-19 Treatment Study</ArticleTitle>
                    <AuthorList CompleteYN="Y">
                        <Author ValidYN="Y">
                            <LastName>Doe</LastName>
                            <ForeName>John</ForeName>
                            <Initials>J</Initials>
                            <AffiliationInfo>
                                <Affiliation>Pfizer Inc., New York, USA. john.doe@pfizer.com</Affiliation>
                            </AffiliationInfo>
                        </Author>
                        <Author ValidYN="Y">
                            <LastName>Smith</LastName>
                            <ForeName>Jane</ForeName>
                            <Initials>J</Initials>
                            <AffiliationInfo>
                                <Affiliation>Harvard Medical School, Boston, MA, USA.</Affiliation>
                            </AffiliationInfo>
                        </Author>
                        <Author ValidYN="Y">
                            <LastName>Johnson</LastName>
                            <ForeName>Bob</ForeName>
                            <Initials>B</Initials>
                            <AffiliationInfo>
                                <Affiliation>Moderna Inc., Cambridge, MA. bob.johnson@modernatx.com</Affiliation>
                            </AffiliationInfo>
                        </Author>
                    </AuthorList>
                </Article>
                <DateRevised>
                    <Year>2023</Year>
                    <Month>07</Month>
                    <Day>01</Day>
                </DateRevised>
            </MedlineCitation>
            <PubmedData>
                <PublicationStatus>ppublish</PublicationStatus>
                <ArticleIdList>
                    <ArticleId IdType="pubmed">123456</ArticleId>
                </ArticleIdList>
            </PubmedData>
        </PubmedArticle>
        <PubmedArticle>
            <MedlineCitation Status="MEDLINE" Owner="NLM">
                <PMID Version="1">789012</PMID>
                <Article PubModel="Print-Electronic">
                    <ArticleTitle>Academic Research on Biomarkers</ArticleTitle>
                    <AuthorList CompleteYN="Y">
                        <Author ValidYN="Y">
                            <LastName>Wilson</LastName>
                            <ForeName>Alice</ForeName>
                            <Initials>A</Initials>
                            <AffiliationInfo>
                                <Affiliation>Department of Biology, Stanford University, CA, USA.</Affiliation>
                            </AffiliationInfo>
                        </Author>
                        <Author ValidYN="Y">
                            <LastName>Brown</LastName>
                            <ForeName>Charlie</ForeName>
                            <Initials>C</Initials>
                            <AffiliationInfo>
                                <Affiliation>Institute of Medical Research, University of California, USA.</Affiliation>
                            </AffiliationInfo>
                        </Author>
                    </AuthorList>
                </Article>
                <DateRevised>
                    <Year>2023</Year>
                    <Month>08</Month>
                    <Day>15</Day>
                </DateRevised>
            </MedlineCitation>
        </PubmedArticle>
    </PubmedArticleSet>'''

@pytest.fixture
def empty_xml():
    """Empty XML for testing edge cases."""
    return '''<?xml version="1.0" ?>
    <PubmedArticleSet>
    </PubmedArticleSet>'''

@pytest.fixture
def malformed_xml():
    """Malformed XML for testing error handling."""
    return '''<?xml version="1.0" ?>
    <PubmedArticleSet>
        <PubmedArticle>
            <MedlineCitation>
                <PMID>123456
            </MedlineCitation>
        <!-- Missing closing tags -->
    </PubmedArticleSet>'''
