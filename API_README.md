# Aladin TTB API Cover Scraper

알라딘 TTB API를 사용한 도서 표지 다운로더

## 📚 개요

이 스크립트는 알라딘의 **공식 TTB API**를 사용하여 도서 표지 이미지를 다운로드합니다.

- **앞표지**: API에서 직접 제공 (고해상도)
- **뒷표지**: 웹 스크래핑으로 시도 (옵션)

## 🔑 API 키 발급

먼저 알라딘 TTB API 키를 발급받아야 합니다.

1. 알라딘 회원가입/로그인
2. API 키 신청 페이지 방문: https://www.aladin.co.kr/ttb/wkey_request.aspx
3. TTBKey 발급 받기

## 📦 설치

### 필수 라이브러리 설치

```bash
pip install -r requirements.txt
```

또는:

```bash
pip install requests beautifulsoup4 lxml
```

## 🚀 사용법

### 기본 사용법

#### 1. 도서 검색 후 표지 다운로드

```bash
python aladin_api_scraper.py --key YOUR_TTB_KEY --search "혈의 누"
```

#### 2. ISBN으로 조회

```bash
python aladin_api_scraper.py --key YOUR_TTB_KEY --isbn "9788936434274"
```

#### 3. 베스트셀러 리스트 가져오기

```bash
python aladin_api_scraper.py --key YOUR_TTB_KEY --list Bestseller --max 10
```

#### 4. 신간 리스트 가져오기

```bash
python aladin_api_scraper.py --key YOUR_TTB_KEY --list ItemNewAll --max 20
```

### 상세 옵션

| 옵션 | 필수 | 설명 | 예시 |
|------|------|------|------|
| `--key` | ✓ | 알라딘 TTB API 키 | `--key TTB...` |
| `--search` |  | 검색어 (도서명, 저자명 등) | `--search "파친코"` |
| `--isbn` |  | ISBN (10자리 또는 13자리) | `--isbn "9788936434274"` |
| `--list` |  | 리스트 종류 | `--list Bestseller` |
| `--max` |  | 최대 결과 수 (기본값: 5) | `--max 10` |
| `--cover-size` |  | 표지 크기 (기본값: Big) | `--cover-size Big` |
| `--output` |  | 출력 디렉토리 (기본값: api_covers) | `--output my_books` |
| `--no-back` |  | 뒷표지 다운로드 시도 안함 | `--no-back` |

### 리스트 종류 (`--list`)

- `ItemNewAll`: 신간 전체 리스트
- `ItemNewSpecial`: 주목할 만한 신간 리스트
- `Bestseller`: 베스트셀러
- `BlogBest`: 블로거 베스트셀러 (국내도서만)

### 표지 크기 (`--cover-size`)

- `Big`: 큰 크기 (너비 200px) ⭐ 권장
- `MidBig`: 중간 큰 크기 (너비 150px)
- `Mid`: 중간 크기 (너비 85px)
- `Small`: 작은 크기 (너비 75px)
- `Mini`: 매우 작은 크기 (너비 65px)

## 📋 사용 예시

### 예시 1: 특정 도서 검색

```bash
python aladin_api_scraper.py --key TTB1234567890 --search "혈의 누" --max 3
```

출력:
```
Searching for: 혈의 누
Found 3 item(s)

[1/3]
============================================================
Title: 혈의 누
Author: 이인직
ISBN: 9788936434274
Publisher: 창비
============================================================

Downloading front cover...
✓ Downloaded: 9788936434274_front.jpg

Attempting to find back cover...
Downloading back cover...
✓ Downloaded: 9788936434274_back.jpg

============================================================
Complete! Downloaded 2 image(s)
Saved to: api_covers/
============================================================
```

### 예시 2: ISBN으로 정확한 도서 조회

```bash
python aladin_api_scraper.py --key TTB1234567890 --isbn "9788936434274"
```

### 예시 3: 베스트셀러 Top 10

```bash
python aladin_api_scraper.py --key TTB1234567890 --list Bestseller --max 10 --cover-size Big
```

### 예시 4: 뒷표지 없이 앞표지만 다운로드

```bash
python aladin_api_scraper.py --key TTB1234567890 --search "파친코" --no-back
```

### 예시 5: 커스텀 출력 폴더

```bash
python aladin_api_scraper.py --key TTB1234567890 --list ItemNewAll --max 5 --output bestsellers
```

## 💻 Python 스크립트에서 사용

```python
from aladin_api_scraper import AladinAPIClient

# API 클라이언트 초기화
client = AladinAPIClient(
    ttb_key="YOUR_TTB_KEY",
    output_dir="my_covers"
)

# 도서 검색
result = client.search_items(query="혈의 누", max_results=5)

if result and result.get('items'):
    for item in result['items']:
        print(f"Title: {item['title']}")
        print(f"Author: {item['author']}")
        print(f"ISBN: {item['isbn13']}")

        # 표지 다운로드
        client.download_covers(item, download_back=True)

# ISBN으로 조회
item_info = client.lookup_item(
    item_id="9788936434274",
    item_id_type="ISBN13",
    cover="Big"
)

# 베스트셀러 리스트
bestsellers = client.get_item_list(
    query_type="Bestseller",
    max_results=10
)
```

## 📊 API 정보

### 사용 가능한 API

1. **상품 검색 API** (`ItemSearch`)
   - 키워드로 도서 검색
   - 제목, 저자, 출판사 등으로 검색 가능

2. **상품 리스트 API** (`ItemList`)
   - 신간, 베스트셀러 등 리스트 조회
   - 카테고리별 조회 가능

3. **상품 조회 API** (`ItemLookUp`)
   - ISBN 또는 ItemId로 특정 도서 조회
   - 상세 정보 포함

4. **중고상품 보유 매장 검색 API** (`ItemOffStoreList`)
   - 중고 매장 정보 조회

### API 제공 정보

- ✅ 도서 제목, 저자, 출판사
- ✅ ISBN (10자리, 13자리)
- ✅ **앞표지 이미지 URL** (다양한 크기)
- ✅ 가격 정보 (정가, 판매가)
- ✅ 출간일
- ✅ 도서 설명
- ✅ 리뷰 정보
- ❌ 뒷표지 (API에서 직접 제공 안함)

## 🔍 뒷표지 다운로드

알라딘 TTB API는 **뒷표지를 직접 제공하지 않습니다**.

이 스크립트는 뒷표지를 얻기 위해:
1. API로 도서 페이지 URL 가져오기
2. 해당 페이지를 웹 스크래핑
3. 뒷표지 이미지 찾기 시도

⚠ **주의**:
- 모든 도서에 뒷표지가 있는 것은 아닙니다
- 웹 스크래핑은 100% 성공을 보장하지 않습니다
- 뒷표지가 필요 없다면 `--no-back` 옵션 사용

## 📁 출력 파일 형식

다운로드된 이미지는 다음 형식으로 저장됩니다:

```
api_covers/
├── 9788936434274_front.jpg    # 앞표지
├── 9788936434274_back.jpg     # 뒷표지 (있는 경우)
├── 9788954698450_front.jpg
└── ...
```

파일명 규칙:
- **ISBN이 있는 경우**: `{ISBN13}_front.jpg`, `{ISBN13}_back.jpg`
- **ISBN이 없는 경우**: `item_{ItemId}_front.jpg`, `item_{ItemId}_back.jpg`

## 🔧 API 제한사항

- 한 페이지당 최대 **50개** 결과
- 총 결과는 **200개**까지만 조회 가능
- API 호출 시 적절한 지연(delay) 권장

## 📖 API 문서

공식 알라딘 TTB API 문서:
- API 소개: http://blog.aladin.co.kr/ttb/
- 카테고리 정보: https://www.aladin.co.kr/ttb/category.aspx

## 🆚 비교: API vs 웹 스크래핑

### API 방식 (`aladin_api_scraper.py`) ⭐ 권장

**장점:**
- ✅ 공식 지원, 안정적
- ✅ 고해상도 표지 이미지
- ✅ 구조화된 데이터 (JSON/XML)
- ✅ 다양한 검색/필터 옵션
- ✅ 빠른 속도
- ✅ API 키만 있으면 사용 가능

**단점:**
- ❌ API 키 발급 필요
- ❌ 뒷표지 직접 제공 안함

### 웹 스크래핑 방식 (`aladin_scraper.py`)

**장점:**
- ✅ API 키 불필요
- ✅ 뒷표지도 시도 가능

**단점:**
- ❌ 웹사이트 구조 변경 시 동작 안할 수 있음
- ❌ 느린 속도
- ❌ 로봇 배제 표준 확인 필요
- ❌ 불안정함

## ⚠ 주의사항

1. **API 키 보안**: API 키를 코드에 하드코딩하지 마세요
2. **요청 제한**: 서버에 부담을 주지 않도록 적절한 지연 사용
3. **저작권**: 다운로드한 이미지의 저작권은 알라딘 및 출판사에 있습니다
4. **개인 용도**: 개인적 학습 및 연구 목적으로만 사용하세요
5. **이용약관**: 알라딘 TTB API 이용약관을 준수하세요

## 🐛 문제 해결

### 문제: "API Error: ..." 메시지

**원인**: 잘못된 API 키 또는 API 요청 오류

**해결책**:
- API 키가 올바른지 확인
- API 키 발급 여부 확인: https://www.aladin.co.kr/ttb/wkey_request.aspx

### 문제: 뒷표지를 찾을 수 없음

**원인**:
- 해당 도서에 뒷표지가 없음
- 웹 스크래핑 실패

**해결책**:
- 모든 도서가 뒷표지를 제공하는 것은 아닙니다
- `--no-back` 옵션으로 앞표지만 다운로드

### 문제: ImportError: No module named 'requests'

**해결책**:
```bash
pip install requests beautifulsoup4
```

## 📊 두 스크립트 비교표

| 기능 | aladin_api_scraper.py (API) | aladin_scraper.py (스크래핑) |
|------|----------------------------|---------------------------|
| API 키 필요 | ✅ 필요 | ❌ 불필요 |
| 앞표지 | ✅ 고해상도 | ✅ |
| 뒷표지 | ⚠ 스크래핑 시도 | ⚠ 스크래핑 시도 |
| 안정성 | ✅ 높음 | ⚠ 보통 |
| 속도 | ✅ 빠름 | ⚠ 느림 |
| 데이터 품질 | ✅ 우수 | ⚠ 보통 |
| 검색 기능 | ✅ 다양함 | ⚠ 제한적 |
| 권장도 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

## 📝 라이선스

교육 및 개인 사용 목적으로 제공됩니다.

## 🙋 FAQ

**Q: API 키는 무료인가요?**
A: 네, 알라딘 TTB API는 무료로 사용할 수 있습니다.

**Q: 상업적 이용이 가능한가요?**
A: 알라딘 TTB API 이용약관을 확인하세요. 일반적으로 제휴 프로그램을 통한 상업적 이용은 가능합니다.

**Q: 뒷표지도 API로 제공되나요?**
A: 아니요, API에서는 앞표지만 제공합니다. 뒷표지는 웹 스크래핑으로 시도합니다.

**Q: ISBN이 없는 도서는 어떻게 검색하나요?**
A: 제목이나 저자로 검색할 수 있습니다.

**Q: 한 번에 몇 개까지 다운로드 할 수 있나요?**
A: API 제한으로 한 번에 최대 50개, 총 200개까지 조회 가능합니다.

---

**Happy Downloading!** 📚✨

알라딘 TTB API: http://blog.aladin.co.kr/ttb/
