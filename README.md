# 🧬 PubMed Non-Academic Paper Extractor

A command-line tool to fetch research papers from PubMed and identify those with authors affiliated with pharmaceutical or biotech companies.

## 🔍 Features

- Fetch papers from PubMed using full query syntax  
- Identify non-academic (pharmaceutical/biotech) author affiliations  
- Extract corresponding author emails  
- Export results to CSV or display in console  
- Robust error handling and logging  
- Type hints throughout the codebase  
- Comprehensive test suite with high coverage  

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher  
- Poetry (dependency and packaging manager)  

### Setup

```bash
git clone https://github.com/Hari-P-T/aganitha-backend-exercise.git
cd aganitha-backend-exercise/pubmed_scraper
poetry install
```

To enter the environment:

```bash
poetry shell
```

## 🛠 Usage

### Basic usage

```bash
poetry run get-papers-list "covid-19"
```

### Save to CSV

```bash
poetry run get-papers-list "covid-19" --file results.csv
```

### Enable debug mode

```bash
poetry run get-papers-list "covid-19" --debug
```

### CLI help

```bash
poetry run get-papers-list --help
```

## 🧪 Testing

### Test Dependencies

Add these dependencies to your `pyproject.toml`:

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
pytest-cov = "^4.0.0"
pytest-mock = "^3.12.0"
responses = "^0.24.0"
black = "^23.0.0"
flake8 = "^6.0.0"
mypy = "^1.8.0"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = [
    "--verbose",
    "--cov=pubmed_scraper",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-fail-under=80"
]
```

### Install Test Dependencies

```bash
poetry install
poetry add --group dev pytest pytest-cov pytest-mock responses
```

### Running Tests

```bash
poetry run pytest
poetry run pytest -v
poetry run pytest --cov=pubmed_scraper
poetry run pytest --cov=pubmed_scraper --cov-report=html
poetry run pytest tests/test_utils.py
poetry run pytest tests/test_utils.py::test_email_extraction
poetry run pytest -n auto
```

### Test Structure

```
tests/
├── __init__.py
├── conftest.py
├── test_utils.py
├── test_parser.py
├── test_fetcher.py
├── test_cli.py
└── fixtures/
    ├── sample_response.xml
    └── expected_output.csv
```

### Test Coverage

Covers:
- Affiliation Classification  
- Email Extraction  
- XML Parsing  
- API Interactions  
- CLI Commands  
- Error Handling  

### Quality Checks

```bash
poetry run mypy pubmed_scraper/
poetry run black pubmed_scraper/ tests/
poetry run flake8 pubmed_scraper/ tests/
poetry run pytest && poetry run mypy pubmed_scraper/ && poetry run black --check pubmed_scraper/ tests/
```

## 🚀 Continuous Integration

Example GitHub Actions:

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install Poetry
      uses: snok/install-poetry@v1

    - name: Install dependencies
      run: poetry install

    - name: Run tests
      run: poetry run pytest --cov=pubmed_scraper --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## 🧪 Output Format

| Column | Description |
|--------|-------------|
| PubmedID | Unique identifier for the paper |
| Title | Title of the paper |
| Publication Date | Date the paper was published |
| Non-academic Author(s) | Names of authors from non-academic institutions |
| Company Affiliation(s) | Names of biotech/pharmaceutical companies |
| Corresponding Author Email | Emails extracted from affiliation text |

## 📁 Code Structure

```
pubmed_scraper/
├── pubmed_scraper/
│   ├── cli.py
│   ├── core/
│   │   ├── fetcher.py
│   │   ├── parser.py
│   │   └── utils.py
├── tests/
│   ├── conftest.py
│   ├── test_*.py
│   └── fixtures/
├── pyproject.toml
└── README.md
```

## 🧠 How It Works

1. **Search Phase**: ESearch API for article IDs  
2. **Fetch Phase**: Fetch metadata via EFetch  
3. **Parse Phase**: Extract names, emails, affiliations  
4. **Filter Phase**: Heuristic-based classification  
5. **Output Phase**: CSV or stdout  

## 🔍 Affiliation Heuristics

- Exclusion filters: university, hospital, institute, etc.  
- Email domain analysis: .edu, .ac vs corporate domains  
- Keywords: biotech, pharma, inc, ltd, corp  

## 🧰 Dev Tools

- Poetry  
- Typer  
- Requests  
- Pandas  
- ElementTree  
- Pytest  
- Coverage.py  
- Black  
- MyPy  

## 🚨 Error Handling

- Invalid queries  
- API/network failures  
- Malformed XML  
- File write errors  

## 📦 Optional: Publish to TestPyPI

```bash
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry publish --build -r test-pypi
```

## 🧑‍💻 Contributing

- Fork and branch
- Add code and tests
- Run: `poetry run pytest`
- Quality: `black`, `mypy`, `flake8`
- Pull request

## 💼 Development Workflow

```bash
poetry install
# Make changes
poetry run pytest
poetry run black pubmed_scraper/ tests/
poetry run mypy pubmed_scraper/
poetry run flake8 pubmed_scraper/ tests/
poetry run pytest --cov=pubmed_scraper --cov-report=html
```