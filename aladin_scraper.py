#!/usr/bin/env python3
"""
Aladin Book Cover Scraper
알라딘(www.aladin.co.kr) 도서 표지 웹스크래퍼

This script scrapes book covers (front and back) from Aladin online bookstore.
"""

import os
import re
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse, parse_qs
import argparse


class AladinScraper:
    def __init__(self, output_dir="covers"):
        """
        Initialize Aladin scraper

        Args:
            output_dir (str): Directory to save downloaded images
        """
        self.base_url = "https://www.aladin.co.kr"
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        })

        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def get_book_id_from_url(self, url):
        """
        Extract book ID from Aladin URL

        Args:
            url (str): Aladin book page URL

        Returns:
            str: Book ID (ItemId)
        """
        try:
            parsed = urlparse(url)
            query_params = parse_qs(parsed.query)

            if 'ItemId' in query_params:
                return query_params['ItemId'][0]

            # Try to extract from path
            match = re.search(r'ItemId=(\d+)', url)
            if match:
                return match.group(1)

        except Exception as e:
            print(f"Error extracting book ID: {e}")

        return None

    def get_book_details(self, book_url):
        """
        Get book details from Aladin page

        Args:
            book_url (str): URL of the book page

        Returns:
            dict: Book information including title, author, and cover URLs
        """
        try:
            response = self.session.get(book_url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')

            book_info = {
                'url': book_url,
                'title': None,
                'author': None,
                'cover_front': None,
                'cover_back': None,
                'isbn': None
            }

            # Extract title
            title_elem = soup.select_one('div.book_info h1, a.Ere_prod_title')
            if title_elem:
                book_info['title'] = title_elem.get_text(strip=True)

            # Extract author
            author_elem = soup.select_one('li.Ere_sub_gray li a, div.author a')
            if author_elem:
                book_info['author'] = author_elem.get_text(strip=True)

            # Extract ISBN
            isbn_pattern = re.compile(r'ISBN[:\s]*([0-9\-]+)')
            isbn_match = isbn_pattern.search(response.text)
            if isbn_match:
                book_info['isbn'] = isbn_match.group(1).replace('-', '')

            # Extract front cover
            # Aladin uses various image containers
            cover_selectors = [
                'div.product_image img',
                'div#cover img',
                'img.i_cover',
                'div.thumb_img img',
                'img[src*="cover"]'
            ]

            for selector in cover_selectors:
                cover_img = soup.select_one(selector)
                if cover_img and cover_img.get('src'):
                    img_src = cover_img.get('src')
                    # Get larger version if available
                    img_src = img_src.replace('_sum_', '_large_').replace('_small_', '_large_')
                    book_info['cover_front'] = urljoin(self.base_url, img_src)
                    break

            # Look for back cover
            # Aladin sometimes has a back cover link or image
            back_cover_patterns = [
                'a[href*="back"]',
                'a[title*="뒷표지"]',
                'img[alt*="뒷표지"]',
                'div.back_cover img'
            ]

            for pattern in back_cover_patterns:
                back_elem = soup.select_one(pattern)
                if back_elem:
                    if back_elem.name == 'a' and back_elem.get('href'):
                        book_info['cover_back'] = urljoin(self.base_url, back_elem.get('href'))
                    elif back_elem.name == 'img' and back_elem.get('src'):
                        book_info['cover_back'] = urljoin(self.base_url, back_elem.get('src'))
                    break

            # Alternative: Try to find back cover by modifying front cover URL
            if book_info['cover_front'] and not book_info['cover_back']:
                # Some sites use patterns like cover_f.jpg and cover_b.jpg
                potential_back = book_info['cover_front'].replace('_f.', '_b.').replace('front', 'back')
                if potential_back != book_info['cover_front']:
                    # Check if back cover exists
                    try:
                        check_response = self.session.head(potential_back, timeout=5)
                        if check_response.status_code == 200:
                            book_info['cover_back'] = potential_back
                    except:
                        pass

            return book_info

        except requests.RequestException as e:
            print(f"Error fetching book details: {e}")
            return None

    def download_image(self, image_url, filename):
        """
        Download an image from URL

        Args:
            image_url (str): URL of the image
            filename (str): Filename to save the image

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            response = self.session.get(image_url, timeout=15, stream=True)
            response.raise_for_status()

            filepath = os.path.join(self.output_dir, filename)

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"✓ Downloaded: {filename}")
            return True

        except Exception as e:
            print(f"✗ Error downloading {filename}: {e}")
            return False

    def scrape_book(self, book_url, custom_name=None):
        """
        Scrape book covers from Aladin

        Args:
            book_url (str): URL of the book page
            custom_name (str): Custom name for saved files (optional)

        Returns:
            dict: Information about downloaded files
        """
        print(f"\n{'='*60}")
        print(f"Scraping: {book_url}")
        print(f"{'='*60}")

        # Get book details
        book_info = self.get_book_details(book_url)

        if not book_info:
            print("Failed to get book information")
            return None

        print(f"\nBook Title: {book_info['title']}")
        print(f"Author: {book_info['author']}")
        print(f"ISBN: {book_info['isbn']}")

        # Determine base filename
        if custom_name:
            base_name = custom_name
        elif book_info['isbn']:
            base_name = book_info['isbn']
        elif book_info['title']:
            # Sanitize title for filename
            base_name = re.sub(r'[^\w\s-]', '', book_info['title'])
            base_name = re.sub(r'[-\s]+', '_', base_name)
        else:
            base_name = f"book_{int(time.time())}"

        results = {
            'book_info': book_info,
            'downloads': []
        }

        # Download front cover
        if book_info['cover_front']:
            ext = os.path.splitext(urlparse(book_info['cover_front']).path)[1] or '.jpg'
            front_filename = f"{base_name}_front{ext}"

            print(f"\nDownloading front cover...")
            if self.download_image(book_info['cover_front'], front_filename):
                results['downloads'].append({
                    'type': 'front',
                    'filename': front_filename,
                    'url': book_info['cover_front']
                })

            # Add delay to be polite
            time.sleep(1)
        else:
            print("\n✗ Front cover not found")

        # Download back cover
        if book_info['cover_back']:
            ext = os.path.splitext(urlparse(book_info['cover_back']).path)[1] or '.jpg'
            back_filename = f"{base_name}_back{ext}"

            print(f"\nDownloading back cover...")
            if self.download_image(book_info['cover_back'], back_filename):
                results['downloads'].append({
                    'type': 'back',
                    'filename': back_filename,
                    'url': book_info['cover_back']
                })
        else:
            print("\n⚠ Back cover not found (not all books have back covers)")

        print(f"\n{'='*60}")
        print(f"Complete! Downloaded {len(results['downloads'])} image(s)")
        print(f"Saved to: {self.output_dir}/")
        print(f"{'='*60}\n")

        return results

    def search_books(self, query, max_results=5):
        """
        Search for books on Aladin

        Args:
            query (str): Search query
            max_results (int): Maximum number of results to return

        Returns:
            list: List of book URLs
        """
        try:
            search_url = f"{self.base_url}/search/wsearchresult.aspx"
            params = {
                'SearchTarget': 'All',
                'SearchWord': query,
                'x': '0',
                'y': '0'
            }

            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find book links
            book_links = []

            # Aladin search results contain links to book detail pages
            selectors = [
                'div.ss_book_box a.bo3',
                'a[href*="ItemId"]',
                'div.ss_book_list a'
            ]

            for selector in selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href and 'ItemId' in href:
                        full_url = urljoin(self.base_url, href)
                        if full_url not in book_links:
                            book_links.append(full_url)
                            if len(book_links) >= max_results:
                                break
                if book_links:
                    break

            return book_links[:max_results]

        except Exception as e:
            print(f"Error searching books: {e}")
            return []


def main():
    parser = argparse.ArgumentParser(
        description='Aladin Book Cover Scraper - 알라딘 도서 표지 스크래퍼',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape a specific book by URL
  python aladin_scraper.py --url "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=12345"

  # Search and scrape
  python aladin_scraper.py --search "혈의 누" --max-results 3

  # Specify output directory
  python aladin_scraper.py --url "URL" --output covers/my_books
        """
    )

    parser.add_argument('--url', type=str, help='Aladin book page URL')
    parser.add_argument('--search', type=str, help='Search for books by title/author')
    parser.add_argument('--max-results', type=int, default=5, help='Maximum search results (default: 5)')
    parser.add_argument('--output', type=str, default='covers', help='Output directory (default: covers)')
    parser.add_argument('--name', type=str, help='Custom name for saved files')

    args = parser.parse_args()

    if not args.url and not args.search:
        parser.print_help()
        return

    # Initialize scraper
    scraper = AladinScraper(output_dir=args.output)

    if args.url:
        # Scrape specific book
        scraper.scrape_book(args.url, custom_name=args.name)

    elif args.search:
        # Search and scrape
        print(f"Searching for: {args.search}")
        book_urls = scraper.search_books(args.search, max_results=args.max_results)

        if not book_urls:
            print("No books found")
            return

        print(f"\nFound {len(book_urls)} book(s)")
        print("\nDo you want to scrape all found books? (y/n): ", end='')

        try:
            choice = input().strip().lower()
            if choice == 'y':
                for i, url in enumerate(book_urls, 1):
                    print(f"\n[{i}/{len(book_urls)}]")
                    scraper.scrape_book(url)
                    if i < len(book_urls):
                        time.sleep(2)  # Be polite with delays
            else:
                print("Cancelled")
        except KeyboardInterrupt:
            print("\n\nCancelled by user")


if __name__ == "__main__":
    main()
