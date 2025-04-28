#!/usr/bin/env python3
"""
Script to find ISBNs for books in a CSV file using the Open Library API.

This script takes a CSV containing book titles, authors, and publication years,
searches for each book's ISBN, and outputs a new CSV with the ISBNs included.

Usage:
    python find_isbn.py input.csv output.csv
"""

import argparse
import csv
import json
import requests
import time
import sys
from typing import Dict, List, Optional, Tuple

def clean_title(title: str) -> str:
    """Clean and normalize a book title for better search results."""
    return title.strip().lower()

def clean_author(author: str) -> str:
    """Clean and normalize an author name for better search results."""
    # Handle "Last, First" format
    if ',' in author:
        parts = author.split(',', 1)
        return f"{parts[1].strip()} {parts[0].strip()}".lower()
    return author.strip().lower()

def find_isbn(title: str, author: str, year: str) -> Tuple[str, str, str]:
    """
    Search for a book's ISBN using the Open Library API.
    Returns a tuple of (ISBN-13, ISBN-10, source)
    """
    # Clean the inputs for better search results
    clean_t = clean_title(title)
    clean_a = clean_author(author)
    
    # Try searching by title and author
    try:
        # Build query parameters
        params = {
            'title': clean_t,
            'author': clean_a,
            'limit': 5
        }
        
        # Add year if available
        if year and year.strip() and year.strip().isdigit():
            params['publish_year'] = year.strip()
        
        # Make the API request
        response = requests.get('https://openlibrary.org/search.json', params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if we got any results
            if data['numFound'] > 0:
                # Go through results to find one with ISBN
                for doc in data['docs']:
                    # Check for ISBN-13
                    isbn_13 = None
                    isbn_10 = None
                    
                    if 'isbn' in doc:
                        for isbn in doc['isbn']:
                            if len(isbn) == 13:
                                isbn_13 = isbn
                            elif len(isbn) == 10:
                                isbn_10 = isbn
                            
                            if isbn_13 and isbn_10:
                                break
                    
                    if isbn_13 or isbn_10:
                        return isbn_13 or "", isbn_10 or "", "OpenLibrary API"
            
            return "", "", "Not found"
        
        return "", "", f"API Error: {response.status_code}"
    
    except Exception as e:
        return "", "", f"Error: {str(e)}"

def process_csv(input_file: str, output_file: str) -> None:
    """Process the input CSV and create an output CSV with ISBNs."""
    try:
        # Open the input file
        with open(input_file, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            
            # Check for required columns
            fieldnames = reader.fieldnames
            if not fieldnames:
                print("Error: Input CSV appears to be empty")
                return
                
            # Identify the title, author, and year columns
            title_col = None
            author_col = None
            year_col = None
            
            for field in fieldnames:
                lower_field = field.lower()
                if 'title' in lower_field:
                    title_col = field
                elif 'author' in lower_field:
                    author_col = field
                elif any(year_term in lower_field for year_term in ['year', 'date', 'published']):
                    year_col = field
            
            if not title_col:
                print("Error: Could not identify title column")
                return
                
            if not author_col:
                print("Error: Could not identify author column")
                return
            
            # Create output fieldnames (all original columns plus ISBN columns)
            output_fieldnames = list(fieldnames)
            # Add ISBN columns if they don't already exist
            if not any('isbn-13' in field.lower() for field in output_fieldnames):
                output_fieldnames.append('ISBN-13')
            if not any('isbn-10' in field.lower() for field in output_fieldnames):
                output_fieldnames.append('ISBN-10')
            output_fieldnames.append('ISBN_Source')
            
            # Prepare the output file
            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=output_fieldnames)
                writer.writeheader()
                
                total_books = sum(1 for _ in csv.DictReader(open(input_file, 'r', newline='', encoding='utf-8')))
                processed = 0
                
                # Reset the input file reader
                infile.seek(0)
                next(reader)  # Skip header
                
                # Process each row
                for row in reader:
                    processed += 1
                    title = row.get(title_col, '')
                    author = row.get(author_col, '')
                    year = row.get(year_col, '') if year_col else ''
                    
                    # Skip if we don't have enough information
                    if not title or not author:
                        print(f"Skipping row {processed}: Missing title or author")
                        row['ISBN-13'] = ''
                        row['ISBN-10'] = ''
                        row['ISBN_Source'] = 'Missing data'
                        writer.writerow(row)
                        continue
                    
                    # Status update
                    print(f"Processing {processed}/{total_books}: {title} by {author}", end="\r")
                    
                    # Find ISBN
                    isbn_13, isbn_10, source = find_isbn(title, author, year)
                    
                    # Add ISBN to the row
                    row['ISBN-13'] = isbn_13
                    row['ISBN-10'] = isbn_10
                    row['ISBN_Source'] = source
                    
                    # Write the updated row
                    writer.writerow(row)
                    
                    # Respect API rate limits
                    time.sleep(1)
                
                print("\nProcessing complete!")
                print(f"Output written to: {output_file}")
                
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    """Main function to parse arguments and run the script."""
    parser = argparse.ArgumentParser(description='Find ISBNs for books in a CSV file.')
    parser.add_argument('input_file', help='Input CSV file with books')
    parser.add_argument('output_file', help='Output CSV file to write results')
    
    args = parser.parse_args()
    
    process_csv(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
