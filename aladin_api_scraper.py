#!/usr/bin/env python3
"""
Aladin TTB API Cover Scraper
알라딘 TTB API를 사용한 도서 표지 다운로더

Official Aladin API documentation: http://blog.aladin.co.kr/ttb/
"""

import os
import requests
import xml.etree.ElementTree as ET
import json
import time
import argparse
from urllib.parse import urljoin, urlparse


class AladinAPIClient:
    """알라딘 TTB API 클라이언트"""

    def __init__(self, ttb_key, output_dir="api_covers"):
        """
        Initialize Aladin API client

        Args:
            ttb_key (str): Aladin TTB API Key
            output_dir (str): Directory to save downloaded images
        """
        self.ttb_key = ttb_key
        self.base_url = "http://www.aladin.co.kr/ttb/api"
        self.output_dir = output_dir

        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def search_items(self, query, query_type="Title", search_target="Book",
                     max_results=10, start=1, sort="Accuracy", cover="Big",
                     output_format="xml"):
        """
        상품 검색 API (ItemSearch)

        Args:
            query (str): 검색어
            query_type (str): 검색어 종류 (Keyword, Title, Author, Publisher)
            search_target (str): 검색 대상 (Book, Foreign, Music, DVD, eBook, All)
            max_results (int): 최대 결과 수 (1-50)
            start (int): 시작 페이지
            sort (str): 정렬 (Accuracy, PublishTime, Title, SalesPoint, CustomerRating)
            cover (str): 표지 크기 (Big, MidBig, Mid, Small, Mini, None)
            output_format (str): 출력 형식 (xml, js)

        Returns:
            dict: 검색 결과
        """
        url = f"{self.base_url}/ItemSearch.aspx"

        params = {
            'ttbkey': self.ttb_key,
            'Query': query,
            'QueryType': query_type,
            'MaxResults': max_results,
            'start': start,
            'SearchTarget': search_target,
            'Sort': sort,
            'Cover': cover,
            'output': output_format,
            'Version': '20131101'
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            if output_format == 'xml':
                return self._parse_xml_response(response.text)
            else:
                return json.loads(response.text)

        except Exception as e:
            print(f"Error in search_items: {e}")
            return None

    def lookup_item(self, item_id, item_id_type="ISBN13", cover="Big",
                    opt_result=None, output_format="xml"):
        """
        상품 조회 API (ItemLookUp)

        Args:
            item_id (str): 상품 ID (ISBN 또는 ItemId)
            item_id_type (str): ID 타입 (ISBN, ISBN13, ItemId)
            cover (str): 표지 크기 (Big, MidBig, Mid, Small, Mini, None)
            opt_result (list): 부가정보 (ebookList, usedList, reviewList 등)
            output_format (str): 출력 형식 (xml, js)

        Returns:
            dict: 상품 정보
        """
        url = f"{self.base_url}/ItemLookUp.aspx"

        params = {
            'ttbkey': self.ttb_key,
            'ItemId': item_id,
            'ItemIdType': item_id_type,
            'Cover': cover,
            'output': output_format,
            'Version': '20131101'
        }

        if opt_result:
            params['OptResult'] = ','.join(opt_result)

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            if output_format == 'xml':
                return self._parse_xml_response(response.text)
            else:
                return json.loads(response.text)

        except Exception as e:
            print(f"Error in lookup_item: {e}")
            return None

    def get_item_list(self, query_type="ItemNewAll", search_target="Book",
                     max_results=10, start=1, cover="Big", output_format="xml"):
        """
        상품 리스트 API (ItemList)

        Args:
            query_type (str): 리스트 종류 (ItemNewAll, ItemNewSpecial, Bestseller 등)
            search_target (str): 검색 대상
            max_results (int): 최대 결과 수
            start (int): 시작 페이지
            cover (str): 표지 크기
            output_format (str): 출력 형식

        Returns:
            dict: 상품 리스트
        """
        url = f"{self.base_url}/ItemList.aspx"

        params = {
            'ttbkey': self.ttb_key,
            'QueryType': query_type,
            'MaxResults': max_results,
            'start': start,
            'SearchTarget': search_target,
            'Cover': cover,
            'output': output_format,
            'Version': '20131101'
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            if output_format == 'xml':
                return self._parse_xml_response(response.text)
            else:
                return json.loads(response.text)

        except Exception as e:
            print(f"Error in get_item_list: {e}")
            return None

    def _parse_xml_response(self, xml_text):
        """Parse XML response to dictionary"""
        try:
            root = ET.fromstring(xml_text)

            # Check for error
            error_elem = root.find('.//errorMessage')
            if error_elem is not None:
                return {'error': error_elem.text}

            result = {
                'version': root.findtext('version'),
                'title': root.findtext('title'),
                'link': root.findtext('link'),
                'totalResults': root.findtext('totalResults'),
                'items': []
            }

            for item in root.findall('.//item'):
                item_data = {
                    'title': item.findtext('title'),
                    'link': item.findtext('link'),
                    'author': item.findtext('author'),
                    'pubDate': item.findtext('pubDate'),
                    'description': item.findtext('description'),
                    'isbn': item.findtext('isbn'),
                    'isbn13': item.findtext('isbn13'),
                    'itemId': item.findtext('itemId'),
                    'priceSales': item.findtext('priceSales'),
                    'priceStandard': item.findtext('priceStandard'),
                    'cover': item.findtext('cover'),
                    'publisher': item.findtext('publisher'),
                    'categoryName': item.findtext('categoryName'),
                    'customerReviewRank': item.findtext('customerReviewRank')
                }
                result['items'].append(item_data)

            return result

        except Exception as e:
            print(f"Error parsing XML: {e}")
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
            if not image_url or image_url == 'None':
                print(f"✗ No image URL provided")
                return False

            response = requests.get(image_url, timeout=15, stream=True)
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

    def scrape_back_cover(self, item_link):
        """
        Try to scrape back cover from item page
        (알라딘 API에는 뒷표지가 없으므로 웹 스크래핑 시도)

        Args:
            item_link (str): Item page URL

        Returns:
            str: Back cover URL if found, None otherwise
        """
        try:
            from bs4 import BeautifulSoup

            response = requests.get(item_link, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')

            # Look for back cover patterns
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
                        return urljoin(item_link, back_elem.get('href'))
                    elif back_elem.name == 'img' and back_elem.get('src'):
                        return urljoin(item_link, back_elem.get('src'))

            return None

        except ImportError:
            print("⚠ BeautifulSoup not installed. Cannot scrape back cover.")
            print("  Install with: pip install beautifulsoup4")
            return None
        except Exception as e:
            print(f"⚠ Error scraping back cover: {e}")
            return None

    def download_covers(self, item, download_back=True):
        """
        Download front and back covers for an item

        Args:
            item (dict): Item information from API
            download_back (bool): Whether to try downloading back cover

        Returns:
            dict: Download results
        """
        results = {
            'item': item,
            'downloads': []
        }

        # Determine base filename
        isbn = item.get('isbn13') or item.get('isbn')
        if isbn:
            base_name = isbn
        else:
            item_id = item.get('itemId')
            base_name = f"item_{item_id}" if item_id else f"book_{int(time.time())}"

        print(f"\n{'='*60}")
        print(f"Title: {item.get('title')}")
        print(f"Author: {item.get('author')}")
        print(f"ISBN: {isbn}")
        print(f"Publisher: {item.get('publisher')}")
        print(f"{'='*60}")

        # Download front cover
        cover_url = item.get('cover')
        if cover_url:
            ext = os.path.splitext(urlparse(cover_url).path)[1] or '.jpg'
            front_filename = f"{base_name}_front{ext}"

            print(f"\nDownloading front cover...")
            if self.download_image(cover_url, front_filename):
                results['downloads'].append({
                    'type': 'front',
                    'filename': front_filename,
                    'url': cover_url
                })
            time.sleep(0.5)
        else:
            print("\n✗ Front cover not available from API")

        # Try to download back cover
        if download_back:
            item_link = item.get('link')
            if item_link:
                print(f"\nAttempting to find back cover...")
                back_cover_url = self.scrape_back_cover(item_link)

                if back_cover_url:
                    ext = os.path.splitext(urlparse(back_cover_url).path)[1] or '.jpg'
                    back_filename = f"{base_name}_back{ext}"

                    print(f"Downloading back cover...")
                    if self.download_image(back_cover_url, back_filename):
                        results['downloads'].append({
                            'type': 'back',
                            'filename': back_filename,
                            'url': back_cover_url
                        })
                else:
                    print("⚠ Back cover not found")
            else:
                print("⚠ No item link to search for back cover")

        print(f"\n{'='*60}")
        print(f"Complete! Downloaded {len(results['downloads'])} image(s)")
        print(f"Saved to: {self.output_dir}/")
        print(f"{'='*60}\n")

        return results


def main():
    parser = argparse.ArgumentParser(
        description='Aladin TTB API Cover Scraper - 알라딘 API 표지 다운로더',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search and download covers
  python aladin_api_scraper.py --key YOUR_TTB_KEY --search "혈의 누"

  # Lookup by ISBN and download
  python aladin_api_scraper.py --key YOUR_TTB_KEY --isbn "9788936434274"

  # Get bestseller list
  python aladin_api_scraper.py --key YOUR_TTB_KEY --list Bestseller --max 5

  # Specify output directory
  python aladin_api_scraper.py --key YOUR_TTB_KEY --search "파친코" --output my_covers

Note: You need a TTB API Key from Aladin.
Get your key at: https://www.aladin.co.kr/ttb/wkey_request.aspx
        """
    )

    parser.add_argument('--key', required=True, help='Aladin TTB API Key')
    parser.add_argument('--search', type=str, help='Search query')
    parser.add_argument('--isbn', type=str, help='ISBN to lookup')
    parser.add_argument('--list', type=str,
                       choices=['ItemNewAll', 'ItemNewSpecial', 'Bestseller', 'BlogBest'],
                       help='Get item list')
    parser.add_argument('--max', type=int, default=5, help='Maximum results (default: 5)')
    parser.add_argument('--cover-size', type=str, default='Big',
                       choices=['Big', 'MidBig', 'Mid', 'Small', 'Mini'],
                       help='Cover image size (default: Big)')
    parser.add_argument('--output', type=str, default='api_covers',
                       help='Output directory (default: api_covers)')
    parser.add_argument('--no-back', action='store_true',
                       help='Do not attempt to download back cover')

    args = parser.parse_args()

    # Initialize API client
    client = AladinAPIClient(args.key, output_dir=args.output)

    items = []

    # Search
    if args.search:
        print(f"Searching for: {args.search}")
        result = client.search_items(
            query=args.search,
            max_results=args.max,
            cover=args.cover_size
        )

        if result and result.get('items'):
            items = result['items']
            print(f"Found {len(items)} item(s)\n")
        else:
            if result and result.get('error'):
                print(f"API Error: {result['error']}")
            else:
                print("No items found")
            return

    # Lookup by ISBN
    elif args.isbn:
        print(f"Looking up ISBN: {args.isbn}")
        result = client.lookup_item(
            item_id=args.isbn,
            item_id_type='ISBN13' if len(args.isbn) == 13 else 'ISBN',
            cover=args.cover_size
        )

        if result and result.get('items'):
            items = result['items']
            print(f"Found item\n")
        else:
            if result and result.get('error'):
                print(f"API Error: {result['error']}")
            else:
                print("Item not found")
            return

    # Get list
    elif args.list:
        print(f"Getting list: {args.list}")
        result = client.get_item_list(
            query_type=args.list,
            max_results=args.max,
            cover=args.cover_size
        )

        if result and result.get('items'):
            items = result['items']
            print(f"Found {len(items)} item(s)\n")
        else:
            if result and result.get('error'):
                print(f"API Error: {result['error']}")
            else:
                print("No items found")
            return

    else:
        parser.print_help()
        return

    # Download covers
    download_back = not args.no_back

    for i, item in enumerate(items, 1):
        print(f"\n[{i}/{len(items)}]")
        client.download_covers(item, download_back=download_back)

        if i < len(items):
            time.sleep(1)  # Be polite with delays


if __name__ == "__main__":
    main()
