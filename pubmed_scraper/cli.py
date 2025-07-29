# cli.py
"""Command-line interface for the PubMed scraper."""

import typer
import logging
import sys
from pathlib import Path
from typing import Optional

import pandas as pd

from pubmed_scraper.core.fetcher import fetch_pubmed_data
from pubmed_scraper.core.parser import parse_pubmed_records

def setup_logging(debug: bool = False) -> logging.Logger:
    """Setup logging configuration."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(levelname)s:%(name)s:%(message)s'
    )
    return logging.getLogger(__name__)

def main(
    query: str = typer.Argument(..., help="Search query for PubMed"),
    file: Optional[str] = typer.Option(None, "-f", "--file", help="Output CSV file name"),
    debug: bool = typer.Option(False, "-d", "--debug", help="Enable debug mode"),
    max_results: int = typer.Option(50, "--max-results", help="Maximum number of results to fetch")
) -> None:
    """
    Fetch research papers from PubMed and identify those with pharmaceutical/biotech company affiliations.
    
    Args:
        query: Search query for PubMed
        file: Optional output CSV file name
        debug: Enable debug logging
        max_results: Maximum number of results to fetch
    """
    logger = setup_logging(debug)
    
    try:
        logger.info(f"Fetching data from PubMed for query: '{query}'")
        xml_data = fetch_pubmed_data(query, max_results=max_results)
        
        if not xml_data:
            logger.warning("No data returned from PubMed API")
            typer.echo("No results found for the given query.", err=True)
            raise typer.Exit(1)

        logger.info("Parsing records...")
        parsed_data = parse_pubmed_records(xml_data)
        
        if not parsed_data:
            logger.warning("No valid records found after parsing")
            typer.echo("No valid records found after parsing.", err=True)
            raise typer.Exit(1)
            
        # Filter records with non-academic affiliations
        filtered_data = [record for record in parsed_data if record.get("Non-academic Author(s)")]
        
        if not filtered_data:
            logger.info("No papers found with pharmaceutical/biotech company affiliations")
            typer.echo("No papers found with pharmaceutical/biotech company affiliations.")
            return
            
        df = pd.DataFrame(filtered_data)
        logger.info(f"Found {len(df)} papers with pharmaceutical/biotech affiliations")

        if file:
            try:
                output_path = Path(file)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                df.to_csv(output_path, index=False, encoding='utf-8')
                logger.info(f"Results saved to {output_path}")
                typer.echo(f"Results saved to {output_path}")
            except Exception as e:
                logger.error(f"Failed to save to file {file}: {e}")
                typer.echo(f"Error saving file: {e}", err=True)
                raise typer.Exit(1)
        else:
            typer.echo(df.to_csv(index=False))
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        typer.echo("Operation cancelled.", err=True)
        raise typer.Exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        if debug:
            logger.exception("Full traceback:")
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

def cli_entry_point():
    """Entry point for the CLI script."""
    typer.run(main)

if __name__ == "__main__":
    cli_entry_point()