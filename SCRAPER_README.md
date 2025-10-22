# Aladin Book Cover Scraper

알라딘(www.aladin.co.kr) 도서 표지 웹스크래퍼

## 기능 (Features)

- 알라딘 도서 페이지에서 앞표지와 뒷표지를 자동으로 다운로드
- 도서 검색 기능 지원
- ISBN, 제목, 저자 정보 추출
- 고해상도 이미지 다운로드
- 사용자 친화적인 명령줄 인터페이스

## 설치 (Installation)

### 1. Python 설치 확인

Python 3.7 이상이 필요합니다.

```bash
python --version
```

### 2. 필요한 라이브러리 설치

```bash
pip install -r requirements.txt
```

또는 개별 설치:

```bash
pip install beautifulsoup4 requests lxml
```

## 사용법 (Usage)

### 기본 사용법

#### 1. URL로 특정 도서 스크래핑

```bash
python aladin_scraper.py --url "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=12345"
```

#### 2. 도서 검색 후 스크래핑

```bash
python aladin_scraper.py --search "혈의 누"
```

#### 3. 여러 검색 결과 가져오기

```bash
python aladin_scraper.py --search "이인직" --max-results 10
```

#### 4. 커스텀 출력 디렉토리 지정

```bash
python aladin_scraper.py --url "URL" --output my_covers
```

#### 5. 파일 이름 커스터마이징

```bash
python aladin_scraper.py --url "URL" --name "book_name"
```

### 상세 옵션

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--url` | 알라딘 도서 페이지 URL | `--url "https://..."` |
| `--search` | 도서 검색 키워드 | `--search "혈의 누"` |
| `--max-results` | 최대 검색 결과 수 (기본값: 5) | `--max-results 10` |
| `--output` | 출력 디렉토리 (기본값: covers) | `--output my_books` |
| `--name` | 저장할 파일의 커스텀 이름 | `--name "my_book"` |

## 사용 예시 (Examples)

### 예시 1: 단일 도서 다운로드

```bash
python aladin_scraper.py --url "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=335485716"
```

출력 예시:
```
============================================================
Scraping: https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=335485716
============================================================

Book Title: 혈의 누
Author: 이인직
ISBN: 9788936434274

Downloading front cover...
✓ Downloaded: 9788936434274_front.jpg

Downloading back cover...
✓ Downloaded: 9788936434274_back.jpg

============================================================
Complete! Downloaded 2 image(s)
Saved to: covers/
============================================================
```

### 예시 2: 검색 후 다운로드

```bash
python aladin_scraper.py --search "파친코" --max-results 3
```

### 예시 3: 여러 URL을 배치로 처리 (Batch Processing)

배치 스크립트 작성:

```bash
#!/bin/bash
urls=(
    "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=12345"
    "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=67890"
)

for url in "${urls[@]}"; do
    python aladin_scraper.py --url "$url"
    sleep 2
done
```

## Python 스크립트에서 사용 (Using as a Module)

```python
from aladin_scraper import AladinScraper

# 스크래퍼 초기화
scraper = AladinScraper(output_dir="my_covers")

# 도서 스크래핑
book_url = "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=12345"
results = scraper.scrape_book(book_url)

# 결과 확인
if results:
    print(f"Title: {results['book_info']['title']}")
    print(f"Author: {results['book_info']['author']}")
    for download in results['downloads']:
        print(f"{download['type']}: {download['filename']}")

# 도서 검색
search_results = scraper.search_books("혈의 누", max_results=5)
for url in search_results:
    print(url)
```

## 출력 파일 형식

다운로드된 이미지는 다음 형식으로 저장됩니다:

- **ISBN이 있는 경우**: `{ISBN}_front.jpg`, `{ISBN}_back.jpg`
- **ISBN이 없는 경우**: `{제목}_front.jpg`, `{제목}_back.jpg`
- **커스텀 이름 지정**: `{custom_name}_front.jpg`, `{custom_name}_back.jpg`

## 폴더 구조

```
.
├── aladin_scraper.py      # 메인 스크래퍼 스크립트
├── requirements.txt        # Python 의존성
├── SCRAPER_README.md      # 사용 설명서 (이 파일)
└── covers/                 # 다운로드된 이미지 (자동 생성)
    ├── 9788936434274_front.jpg
    ├── 9788936434274_back.jpg
    └── ...
```

## 주의사항 (Important Notes)

1. **로봇 배제 표준 준수**: 알라딘의 robots.txt를 확인하고 준수하세요
2. **요청 간격**: 서버에 부담을 주지 않도록 요청 사이에 적절한 지연을 두세요
3. **저작권**: 다운로드한 이미지의 저작권은 알라딘 및 출판사에 있습니다
4. **개인적 용도**: 이 스크래퍼는 개인적인 학습 및 연구 목적으로만 사용하세요
5. **뒷표지**: 모든 도서에 뒷표지가 있는 것은 아닙니다

## 문제 해결 (Troubleshooting)

### 문제: ImportError: No module named 'bs4'

**해결책**:
```bash
pip install beautifulsoup4
```

### 문제: 이미지를 찾을 수 없음

**원인**: 알라딘 웹사이트 구조가 변경되었을 수 있습니다.

**해결책**:
- URL이 정확한지 확인
- 도서 페이지가 존재하는지 확인
- 스크립트 업데이트가 필요할 수 있음

### 문제: 403 Forbidden 오류

**원인**: 너무 많은 요청으로 인한 차단

**해결책**:
- 요청 간격을 늘리기
- User-Agent 헤더 확인
- 잠시 후 다시 시도

## 기술 스택 (Tech Stack)

- **Python 3.7+**
- **BeautifulSoup4**: HTML 파싱
- **Requests**: HTTP 요청
- **lxml**: XML/HTML 처리

## 라이선스 (License)

이 스크립트는 교육 및 개인 사용 목적으로 제공됩니다.

## 면책 조항 (Disclaimer)

이 도구는 교육 목적으로 제공됩니다. 웹 스크래핑을 수행할 때는 항상:
- 웹사이트의 이용약관을 확인하세요
- robots.txt 파일을 존중하세요
- 서버에 과부하를 주지 마세요
- 저작권법을 준수하세요

## 업데이트 로그 (Changelog)

### v1.0.0 (2025-10-22)
- 초기 릴리스
- 앞표지 및 뒷표지 다운로드 기능
- 도서 검색 기능
- 명령줄 인터페이스

## 기여 (Contributing)

버그 리포트나 기능 제안은 이슈로 등록해주세요.

## 연락처 (Contact)

질문이나 제안사항이 있으시면 이슈를 통해 연락주세요.

---

**Happy Scraping!** 📚✨
