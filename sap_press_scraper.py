"""
Web scraper for SAP Press books catalog
Scrapes all books from https://www.sap-press.com and provides them in a structured format
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
from typing import List, Dict, Optional
import time
from urllib.parse import urljoin


class SAPPressScraper:
    """Scraper for SAP Press website to extract book information"""
    
    # AI-related keywords to filter books
    AI_KEYWORDS = [
        'artificial intelligence', 'ai', 'machine learning', 'deep learning',
        'neural network', 'nlp', 'natural language', 'tensorflow', 'pytorch',
        'keras', 'data science', 'data analytics', 'predictive', 'ai model',
        'ai-powered', 'generative ai', 'llm', 'algorithm', 'automation',
        'intelligent', 'cognitive'
    ]
    
    def __init__(self, base_url: str = "https://www.sap-press.com", filter_ai: bool = False):
        self.base_url = base_url
        self.books = []
        self.filter_ai = filter_ai
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def is_ai_related(self, book_info: Dict) -> bool:
        """Check if a book is related to AI/ML"""
        text_to_search = f"{book_info['title']} {book_info['description']}".lower()
        for keyword in self.AI_KEYWORDS:
            if keyword in text_to_search:
                return True
        return False
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a page"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_books_from_page(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract book information from a page"""
        books_on_page = []
        seen_urls = set()
        
        # Find all links that look like book links (format: /title_id/)
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            try:
                href = link.get('href', '')
                # Book links contain an underscore followed by digits at the end
                # Pattern: /something-something_digits/
                if href.startswith('/') and '_' in href and href.endswith('/'):
                    # Extract the ID part
                    try:
                        book_id = href.split('_')[-1].rstrip('/')
                        if book_id.isdigit():
                            # This looks like a book link
                            title = link.get_text(strip=True)
                            if title and title != 'More about the book' and title != 'Cover':
                                book_url = urljoin(self.base_url, href)
                                
                                # Avoid duplicates
                                if book_url not in seen_urls:
                                    seen_urls.add(book_url)
                                    
                                    # Get the description (usually in a nearby p tag)
                                    description = ""
                                    parent = link.find_parent()
                                    if parent:
                                        p_tag = parent.find('p')
                                        if p_tag:
                                            description = p_tag.get_text(strip=True)
                                    
                                    book_info = {
                                        'title': title.strip(),
                                        'url': book_url,
                                        'description': description[:200] + '...' if len(description) > 200 else description
                                    }
                                    
                                    # Apply AI filter if enabled
                                    if self.filter_ai:
                                        if self.is_ai_related(book_info):
                                            books_on_page.append(book_info)
                                    else:
                                        books_on_page.append(book_info)
                    except (IndexError, ValueError):
                        continue
            except Exception as e:
                continue
        
        return books_on_page
    
    def scrape_all_books(self, max_pages: Optional[int] = None) -> List[Dict]:
        """
        Scrape all books from SAP Press website
        
        Args:
            max_pages: Maximum number of pages to scrape (None for all)
        
        Returns:
            List of book dictionaries
        """
        print("Starting to scrape SAP Press website...")
        print(f"Base URL: {self.base_url}")
        
        # Start with the homepage
        soup = self.fetch_page(self.base_url)
        if not soup:
            print("Failed to fetch the homepage")
            return []
        
        # Extract books from the first page
        self.books.extend(self.extract_books_from_page(soup))
        print(f"Found {len(self.books)} books on the homepage")
        
        # Try to find pagination links for more pages
        page_num = 2
        while max_pages is None or page_num <= max_pages:
            # Common pagination URL patterns for websites
            page_urls = [
                f"{self.base_url}/?page={page_num}",
                f"{self.base_url}/page/{page_num}/",
                f"{self.base_url}/?p={page_num}",
            ]
            
            found_books = False
            for page_url in page_urls:
                soup = self.fetch_page(page_url)
                if soup:
                    books_on_page = self.extract_books_from_page(soup)
                    if books_on_page:
                        self.books.extend(books_on_page)
                        print(f"Found {len(books_on_page)} books on page {page_num}")
                        found_books = True
                        time.sleep(1)  # Be respectful to the server
                        break
            
            if not found_books:
                print(f"No more pages found at page {page_num}")
                break
            
            page_num += 1
        
        # Remove duplicates while preserving order
        seen_urls = set()
        unique_books = []
        for book in self.books:
            if book['url'] not in seen_urls:
                seen_urls.add(book['url'])
                unique_books.append(book)
        
        self.books = unique_books
        print(f"\nTotal unique books found: {len(self.books)}")
        
        return self.books
    
    def save_to_json(self, filename: str = "sap_press_books.json"):
        """Save books to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.books, f, indent=2, ensure_ascii=False)
            print(f"Books saved to {filename}")
        except Exception as e:
            print(f"Error saving to JSON: {e}")
    
    def save_to_csv(self, filename: str = "sap_press_books.csv"):
        """Save books to CSV file"""
        try:
            if not self.books:
                print("No books to save")
                return
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['title', 'url', 'description'])
                writer.writeheader()
                writer.writerows(self.books)
            print(f"Books saved to {filename}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")
    
    def print_books(self):
        """Print all books in a formatted way"""
        if not self.books:
            print("No books found")
            return
        
        print("\n" + "="*80)
        print("SAP PRESS BOOKS CATALOG".center(80))
        print("="*80 + "\n")
        
        for idx, book in enumerate(self.books, 1):
            print(f"{idx}. {book['title']}")
            print(f"   URL: {book['url']}")
            if book['description']:
                print(f"   Description: {book['description']}")
            print()


def get_sample_books() -> List[Dict]:
    """Returns a list of sample books from SAP Press for demonstration"""
    return [
        {
            'title': 'Machines That Think–How Artificial Intelligence Works and What It Means for Us',
            'url': 'https://www.sap-press.com/machines-that-think_6171/',
            'description': 'Artificial intelligence is no longer confined to science fiction. It recommends what we watch, curates what we read, and drives critical business decisions. Learn how AI works and what it means for us.'
        },
        {
            'title': 'Applied Machine Learning',
            'url': 'https://www.sap-press.com/applied-machine-learning_6170/',
            'description': 'Put machine learning theory into practice with this hands-on guide! Learn about the real-world application of machine learning models and how to implement them in your projects.'
        },
        {
            'title': 'PyTorch–The Practical Guide',
            'url': 'https://www.sap-press.com/pytorch_6207/',
            'description': 'PyTorch is the framework for deep learning—so dive on in! Learn how to train, optimize, and deploy AI models using PyTorch, one of the most popular deep learning frameworks.'
        },
        {
            'title': 'Keras 3–The Comprehensive Guide to Deep Learning with the Keras API and Python',
            'url': 'https://www.sap-press.com/keras-3_6142/',
            'description': 'Harness the power of AI with this guide to using Keras! Start by reviewing the fundamentals of deep learning and how to build neural networks with the Keras API.'
        },
        {
            'title': 'Developing Apps with SAP Build Code and Generative AI',
            'url': 'https://www.sap-press.com/developing-apps-with-sap-build-code-and-generative-ai_6230/',
            'description': 'Are you ready to make the most of SAP\'s generative AI-powered developer tools? With this guide, learn how to develop apps using AI-powered code generation.'
        },
        {
            'title': 'Hardware Security–The Practical Guide to Penetration Testing and Prevention',
            'url': 'https://www.sap-press.com/hardware-security_6181/',
            'description': 'Defend your system against hardware-based security breaches by thinking like a hacker! Learn about AI-driven security threats and prevention methods.'
        },
        {
            'title': 'Python 3–The Comprehensive Guide',
            'url': 'https://www.sap-press.com/python-3_5566/',
            'description': 'Ready to master Python? Learn to write effective code with this award-winning comprehensive guide. Python is the go-to language for AI and machine learning development.'
        },
        {
            'title': 'Google Analytics 4–The Practical Guide',
            'url': 'https://www.sap-press.com/google-analytics-4_6180/',
            'description': 'Frustrated by the complexities of Google Analytics 4? Let us show you the way! Learn to use AI-powered insights for data analytics and decision making.'
        }
    ]


def main():
    """Main function to run the scraper"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Scrape books from SAP Press website'
    )
    parser.add_argument('--max-pages', type=int, default=None,
                        help='Maximum number of pages to scrape')
    parser.add_argument('--output-json', default='sap_press_books.json',
                        help='Output JSON filename')
    parser.add_argument('--output-csv', default='sap_press_books.csv',
                        help='Output CSV filename')
    parser.add_argument('--print', action='store_true',
                        help='Print books to console')
    parser.add_argument('--demo', action='store_true',
                        help='Use sample books for demonstration (no actual scraping)')
    parser.add_argument('--ai-only', action='store_true',
                        help='Filter books to show only AI and Machine Learning related titles')
    
    args = parser.parse_args()
    
    # Create scraper and run it
    scraper = SAPPressScraper(filter_ai=args.ai_only)
    
    if args.demo:
        print("Using sample books for demonstration...")
        scraper.books = get_sample_books()
        if args.ai_only:
            print("Filtering for AI-related books only...\n")
            scraper.books = [book for book in scraper.books if scraper.is_ai_related(book)]
    else:
        scraper.scrape_all_books(max_pages=args.max_pages)
    
    # Save results
    scraper.save_to_json(args.output_json)
    scraper.save_to_csv(args.output_csv)
    
    # Print if requested
    if args.print:
        scraper.print_books()
    
    filter_text = " (AI-related only)" if args.ai_only else ""
    print(f"\nScraping completed! Total books found{filter_text}: {len(scraper.books)}")


if __name__ == '__main__':
    main()
