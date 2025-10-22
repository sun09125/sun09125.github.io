# sun09125.github.io

나의 홈페이지

## 📚 Aladin Book Cover Scrapers

알라딘 도서 표지 다운로더 - 두 가지 방식 제공

### 1. API 방식 (권장) ⭐

**파일**: `aladin_api_scraper.py`

알라딘 공식 TTB API를 사용하여 도서 표지를 다운로드합니다.

```bash
# API 키로 검색
python aladin_api_scraper.py --key YOUR_TTB_KEY --search "혈의 누"

# ISBN으로 조회
python aladin_api_scraper.py --key YOUR_TTB_KEY --isbn "9788936434274"

# 베스트셀러 다운로드
python aladin_api_scraper.py --key YOUR_TTB_KEY --list Bestseller --max 10
```

📖 **상세 가이드**: [API_README.md](API_README.md)

### 2. 웹 스크래핑 방식

**파일**: `aladin_scraper.py`

HTML 파싱을 통해 도서 표지를 스크래핑합니다.

```bash
# URL로 스크래핑
python aladin_scraper.py --url "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=12345"

# 검색 후 스크래핑
python aladin_scraper.py --search "파친코"
```

📖 **상세 가이드**: [SCRAPER_README.md](SCRAPER_README.md)

### 설치

```bash
pip install -r requirements.txt
```

### 비교

| 특징 | API 방식 | 스크래핑 방식 |
|------|---------|------------|
| API 키 | 필요 ✅ | 불필요 ❌ |
| 안정성 | 높음 ✅ | 보통 ⚠ |
| 속도 | 빠름 ✅ | 느림 ⚠ |
| 권장 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
