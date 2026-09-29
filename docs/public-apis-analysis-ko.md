# public-apis 전수조사 분석 및 활용·수익화 정리 (한국어)

> 이 문서는 `public-apis` 레포지토리를 파일 단위로 전수조사한 결과와,
> 활용법 · 기술 구조 · 수익화 아이디어에 대한 논의를 정리한 기록입니다.

## 📎 관련 GitHub 주소

| 구분 | 주소 |
|:---|:---|
| 이 저장소 (포크) | https://github.com/bmshin94/public-apis |
| 원본 저장소 | https://github.com/public-apis/public-apis |
| 기여 가이드 | https://github.com/public-apis/public-apis/blob/master/CONTRIBUTING.md |
| 이슈 | https://github.com/public-apis/public-apis/issues |
| 풀 리퀘스트 | https://github.com/public-apis/public-apis/pulls |
| 이 목록의 JSON API (서드파티) | https://github.com/davemachado/public-api |
| 운영 주체 (APILayer) | https://apilayer.com |

---

## 1. 이게 뭐 하는 물건인가

### 1-1. 정체: 코드가 아니라 "목록(데이터)"

실행되는 프로그램이나 라이브러리가 아닙니다. **전 세계 무료 공개 API를 정리한 큐레이션 목록**이며,
`README.md` 한 개(2,330줄 / 259KB)가 프로젝트의 사실상 전부입니다.

```
public-apis/                     # 전체 3.6MB, 파일 24개
├── README.md          259 KB    # 💥 프로젝트의 99%
├── CONTRIBUTING.md      6 KB    # 기여 규칙
├── CLAUDE.md            1 KB    # 프로젝트 가이드
├── LICENSE              1 KB    # MIT
├── scripts/                     # 검증 도구 (본체 아님)
│   ├── validate/format.py       # 마크다운 표 형식 검사기
│   ├── validate/links.py        # 링크 생존 검사기
│   ├── tests/                   # 위 두 개의 유닛테스트
│   └── github_pull_request.sh   # PR diff 검증 스크립트
└── .github/workflows/           # GitHub Actions 3개
```

`scripts/`와 `.github/`는 README가 망가지지 않게 지키는 **문지기 장치**입니다.

### 1-2. 실측 통계 (직접 집계)

| 항목 | 수치 |
|:---|:---|
| 총 API 개수 | **약 1,833개** (표 행 1,844개 중 스폰서 광고 11행 제외) |
| 카테고리 수 | **51개** |
| 인증 불필요 (`No`) | **871개** (47.5%) |
| API 키 필요 (`apiKey`) | **805개** (43.9%) |
| OAuth 필요 | **150개** (8.2%) |
| `X-Mashape-Key` / `User-Agent` | 6개 / 1개 |
| HTTPS 지원 | 1,741개 (미지원 91개) |
| CORS `Yes` / `Unknown` / `No` | 651 / 1,003 / 178 |
| **무인증 + CORS 가능** | **372개** ⭐ 서버 없이 브라우저에서 직접 호출 가능 |
| 커밋 수 / 기여자 수 | 889 커밋 / 380명 (이 포크 기준) |

카테고리 상위: `Development(172)` `Government(109)` `Games & Comics(103)` `Geocoding(99)`
`Cryptocurrency(84)` `Transportation(82)` `Finance(76)` `Open Data(60)` `Sports & Fitness(54)`
`Social(54)` `Security(50)` `Video(49)` `Science & Math(44)` `Weather(41)` `Health(41)` ...

### 1-3. 데이터 형식

```markdown
### Weather
| API | Description | Auth | HTTPS | CORS |
|:---|:---|:---|:---|:---|
| [Open-Meteo](https://open-meteo.com/) | Global weather forecast API for non-commercial use | No | Yes | Yes |
| [OpenWeatherMap](https://openweathermap.org/api) | Weather | `apiKey` | Yes | Unknown |
```

**[이름](문서링크) / 설명 / 인증방식 / HTTPS / CORS** 5개 컬럼이 전부입니다.

### 1-4. scripts/ 자동 품질관리 장치

**`scripts/validate/format.py` — 표 형식 검사기**
- 카테고리 내부 알파벳 순서
- 5개 컬럼 존재 여부
- 제목이 `[TITLE](LINK)` 문법인가, `... API`로 끝나지 않는가
- 설명: 첫 글자 대문자 / 마침표 등 구두점으로 끝나지 않음 / **100자 이내**
- Auth 값이 `apiKey`·`OAuth`·`X-Mashape-Key`·`User-Agent`·`No` 중 하나이고 백틱으로 감쌌는가
- HTTPS는 `Yes`/`No`, CORS는 `Yes`/`No`/`Unknown`
- 각 셀 좌우 정확히 공백 1칸
- 새 카테고리는 최소 3개 항목 + 상단 Index 등록

**`scripts/validate/links.py` — 링크 생존 검사기**
- 중복 링크 탐지
- 실제 HTTP 요청으로 생존 확인 (timeout 25초)
- **User-Agent를 4종 브라우저로 위장** (봇 차단 회피)
- **Cloudflare 보호 페이지 오탐 방지**: 403/503 + `Server: cloudflare` + 18개 특징 문자열 조합 판별
- 에러를 SSL / 연결오류 / 타임아웃 / 리다이렉트 과다 / 미상 5종으로 분류

**`.github/workflows/` — GitHub Actions 3개**

| 워크플로 | 시점 | 하는 일 |
|:---|:---|:---|
| `test_of_push_and_pull.yml` | push / PR | 형식 검사 + PR에서 추가된 줄의 링크만 생존 확인 |
| `test_of_validate_package.yml` | push / PR | 검증 스크립트 자체의 유닛테스트 |
| `validate_links.yml` | **매일 자정 cron** | 1,800여 개 링크 전수 생존 점검 |

`github_pull_request.sh`는 PR의 `.diff`를 받아 `+`로 시작하는 추가 줄만 뽑아
거기 포함된 링크만 검사합니다. (전체 검사는 수십 분이 걸리므로)

### 1-5. 언제 쓰는가

1. 아이디어는 있는데 데이터가 없을 때
2. 사이드 프로젝트 / 해커톤 / 포트폴리오
3. 학습·교육용 (API 호출, JSON 파싱 연습)
4. 상용 서비스 프로토타입 검증
5. 더미 데이터가 필요할 때 (`Test Data` 카테고리)
6. LLM/AI 에이전트의 외부 도구 카탈로그

### 1-6. 무슨 도움이 되는가

- **탐색 시간 제로화**: 구글링 30분 → 30초
- **의사결정 정보 선제공**: 인증 / HTTPS / CORS는 API 선택 시 최우선 확인 항목
- **무인증+CORS 372개** = 서버·가입·비용 없이 프론트엔드만으로 앱 완성 가능
- **살아있는 링크**: 매일 자동 검증 + 380명이 지속 갱신
- **MIT 라이선스**: 가공·상업적 이용 가능 (수익화의 법적 근거)

### 1-7. 전수조사에서 발견한 실제 문제

1. **상업적 성격**: APILayer(유료 API 기업)가 운영. README 상단 약 80줄이 자사 광고이고
   모든 링크에 `utm_source=Github&utm_medium=Referral` 추적 파라미터가 붙어 있음.
   CONTRIBUTING.md는 "마케팅 PR 거절"이라 하면서 상단은 전부 자사 광고라는 모순.
2. **데이터 오염**: 형식 검사기를 우회한 항목 존재 — 백틱 없는 `apiKey` 3건,
   백틱 있는 `No` 3건, HTTPS 컬럼이 빈 11건 등.
3. **의존성 노후**: `requirements.txt`가 `requests==2.27.1`, `certifi==2021.10.8` 등
   2021~2022년 버전 고정. 최신 인증서 체인 검증에서 문제 가능.
4. **기계 판독성 부족**: JSON/YAML이 아니라 마크다운 표 → 직접 파싱 필요 (동시에 기회).
5. **"무료"의 정의가 제각각**: 완전 무료 / 무료 티어 / 가입 필요가 혼재, **레이트리밋 정보 없음**.

---

## 2. 쉬운 비유로 다시 이해하기

### 비유 1: 배달앱이 아니라 "맛집 리스트"

- 배달앱 = 켜면 음식이 옴 → 실행되는 소프트웨어
- 맛집 리스트 = 가게 이름·전화번호·주차가능 여부가 적힌 문서 → **전화는 내가 건다**

이 레포는 후자입니다. 설치해도 날씨 데이터가 오지 않습니다.
**데이터를 주는 곳의 주소를 알려줄 뿐**이고, 실제 요청은 내 코드가 보냅니다.

리스트에 미리 적힌 정보:
- 🍽 가게 이름 + 홈페이지 → API 이름 + 문서 링크
- 📝 뭘 파는 집인지 → 한 줄 설명
- 🔑 예약 필요 여부 → **Auth** (가입해서 키 받아야 하나?)
- 🔒 위생등급 → **HTTPS** (암호화 통신 되나?)
- 🚗 주차 가능 여부 → **CORS** (브라우저에서 바로 불러도 되나?)

### 비유 2: CORS = 주차장 유무

- **CORS = Yes (주차 가능)** → 브라우저에서 직접 호출 가능. 서버 불필요 → **서버비 0원**
- **CORS = No/Unknown (주차 불가)** → 브라우저가 차단. 내 서버가 대신 호출해야 함 → **서버비 발생**

그래서 **무인증 + CORS 가능 = 372개**가 황금 목록입니다.
가입도, 서버도, 돈도 없이 HTML 파일 하나로 앱이 됩니다.

### 비유 3: scripts/ = 리스트를 지키는 사서

| 로봇 | 역할 | 쉬운 말 |
|:---|:---|:---|
| `format.py` | 형식 검사 | "설명 100자 초과, 반려" "ㄱㄴㄷ 순서 틀림, 반려" |
| `links.py` | 링크 검사 | 실제로 전화를 걸어봄. 안 받으면 폐업 처리 |
| Actions (매일 자정) | 순찰 | 매일 밤 1,833곳에 전부 전화 |

1,833개를 380명이 같이 편집하면 반드시 무너지므로,
**사람이 아니라 로봇이 검사**하도록 만든 것이 이 프로젝트의 핵심 설계입니다.

---

## 3. 자주 묻는 질문

### 3-1. 설치 및 사용법

**A. 웹에서 보기 (99%의 사용법)** — 접속 후 `Ctrl+F` 검색, 상단 Index에서 카테고리 클릭.

**B. 로컬에 받기**
```bash
git clone https://github.com/bmshin94/public-apis.git
cd public-apis
grep -i "weather" README.md
grep -E '^\| \[.*\| No \| Yes \| Yes \|' README.md   # 무인증+HTTPS+CORS만 추출
```

**C. 검증 스크립트 실행 (기여 시에만 필요)**
```bash
python -m pip install -r scripts/requirements.txt

python scripts/validate/format.py README.md        # 형식 검사
python scripts/validate/links.py README.md         # 전체 링크 검사 (수십 분)
python scripts/validate/links.py README.md -odlc   # 중복만 빠르게

cd scripts && python -m unittest discover tests/ --verbose
```
> ⚠️ 의존성이 2021년 버전 고정이므로 반드시 가상환경(venv)에서 실행할 것.

**D. API 추가 기여 (PR)**
1. Fork → 브랜치 생성
2. 해당 카테고리에 알파벳 순서 맞춰 한 줄 추가
3. 규칙: 설명 100자 이내 / 첫 글자 대문자 / 마침표 금지 / 이름 끝 "API" 금지 /
   TLD(.com) 금지 / 셀 좌우 공백 1칸 / **PR 1개당 API 1개** / 커밋 squash
4. PR 제목은 `Add Blockchain API` 형식
5. CI 통과 확인

**E. 프로그램에서 데이터로 쓰기 (가장 실용적)**
```python
import re, json
rows = re.findall(r'^\| \[(.+?)\]\((http.+?)\) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|',
                  open('README.md', encoding='utf-8').read(), re.M)
apis = [{"name":n, "url":u, "desc":d, "auth":a.strip('`'), "https":h, "cors":c}
        for n,u,d,a,h,c in rows]
json.dump(apis, open('apis.json','w'), ensure_ascii=False, indent=2)
print(len(apis))   # ≈1833
```

### 3-2. 플러그인? 스킬? MCP? → 셋 다 아님

| 구분 | 정의 | public-apis |
|:---|:---|:---|
| **플러그인** | 호스트 앱 기능을 확장하는 설치형 확장 (manifest + 코드) | ❌ |
| **스킬** | AI 에이전트용 지침서 (`SKILL.md` + 리소스) | ❌ (가장 가깝게 개조 가능) |
| **MCP 서버** | AI가 호출할 도구/리소스를 노출하는 실행 서버 | ❌ |
| **public-apis** | 사람이 읽는 큐레이션 목록 + CI 검증기 | ✅ |

**다만 셋 다로 개조 가능하며, 그게 실제 가치 있는 작업입니다:**
1. **MCP 서버로 개조** (난이도 中, 가치 高) — `search_public_apis()`, `get_api_detail()` 노출
2. **스킬로 개조** (난이도 下, 가치 中) — `SKILL.md` + `apis.json`
3. **VS Code 확장** (난이도 中, 가치 中) — 검색 후 fetch 스니펫 자동 삽입

→ **①MCP 서버가 압도적으로 실용적**입니다.

### 3-3. API 토큰이 필요한가?

**레포 자체**: 불필요 ✅ (공개 레포, 로그인 없이 열람·clone 가능)

**개별 API**: API마다 다릅니다.

| Auth | 개수 | 필요한 작업 |
|:---|---:|:---|
| `No` | 871 | 없음. 바로 호출 |
| `apiKey` | 805 | 가입 → 키 발급 → 헤더/쿼리에 첨부 |
| `OAuth` | 150 | 앱 등록 → 리다이렉트 URI → 토큰 교환 (가장 복잡) |
| `X-Mashape-Key` | 6 | RapidAPI 가입 |
| `User-Agent` | 1 | 헤더 한 줄 |

**실전 팁**
- 시작은 `No` 871개부터. 특히 `No` + `CORS: Yes` = **372개**는 `fetch()` 한 줄로 끝:
```javascript
fetch('https://api.open-meteo.com/v1/forecast?latitude=37.56&longitude=126.97&current=temperature_2m')
  .then(r => r.json()).then(console.log);
```
- **`apiKey`를 프론트엔드에 절대 넣지 말 것** — React 번들에 넣으면 개발자도구에서 노출 → 요금 폭탄.
  백엔드나 서버리스 함수에 숨기고 프록시할 것.
- `.env` + `.gitignore` 는 기본.
- 무료 티어 레이트리밋 정보는 **이 목록에 없음** → 각 API 문서 직접 확인 필요.

### 3-4. 왜 GitHub에서 유명한가

1. **문제가 보편적이고 영원함** — "데이터 어디서 구하지?"는 유행을 타지 않음
2. **진입장벽 0** — 설치·설정·학습 없음. 클릭 → 읽기 → 끝
3. **북마크 대용으로 스타를 누름** — 즐겨찾기 대신 별. 스타 수를 구조적으로 부풀림
4. **기여 난이도 극단적으로 낮음** — README 한 줄 추가로 오픈소스 기여자가 됨 (380명 / 889 커밋)
5. **자동화로 품질 유지** — 보통 awesome-list는 1~2년이면 링크 절반이 죽는데,
   매일 전수 검사 + PR 자동 검증으로 붕괴를 막음. **"살아있는 리스트"라는 신뢰가 핵심 자산**
6. **네트워크 효과 + 검색 상위 노출** — "free API list" 1위 → 유입 → 스타 → 랭킹 상승 (자기강화 루프)
7. **기업이 트래픽 가치를 인정해 인수** — APILayer가 README 상단을 자사 광고로 사용.
   이 사실 자체가 **"목록의 수익성"을 기업이 증명한 것**

### 3-5. 로컬 에이전트 구축에 도움이 되는가 → 상당히. 단 가공 필요

**✅ 도움이 되는 지점**
1. **에이전트의 도구 카탈로그 시드** — 1,833개 외부 능력의 인덱스
2. **RAG 코퍼스로 최적** — 수 MB 규모라 로컬 벡터DB(Chroma/FAISS/sqlite-vec)에 즉시 적재
3. **인증/CORS 메타데이터가 선택 규칙이 됨** — "auth==No인 것만 제안", "cors==Yes인 것만 사용".
   LLM이 환각으로 만들 수 없는 **검증된 사실 데이터**
4. **환각 방지** — 존재하지 않는 엔드포인트 생성 문제를 그라운딩으로 완화
5. **비용 0의 실습 환경** — 무인증 871개로 무한 실험

**⚠️ 한계**

| 한계 | 설명 | 해결 방향 |
|:---|:---|:---|
| 엔드포인트 없음 | 링크는 **문서 페이지**지 호출 URL이 아님 | 문서 크롤링·요약 단계 추가 |
| OpenAPI 스펙 없음 | 파라미터/응답 스키마 전무 | 상위 200개만 수동/LLM 스펙화 |
| 레이트리밋 정보 없음 | 무한루프 호출 시 즉시 차단 | 자체 쿼터 테이블 구축 |
| 설명 100자 제한 | 임베딩 품질 저하 | LLM으로 설명 보강 |
| 마크다운 파싱 필요 | 구조화 데이터 아님 | 1회 파싱 → JSON 캐시 |

**추천 아키텍처**
```
README.md
   ↓ 파싱 (정규식, 1회)
apis.json (1,833건)
   ↓ LLM 보강: 카테고리 세분화 / 태그 / 예상 엔드포인트 / 무료 한도
enriched.json
   ↓ 임베딩
로컬 벡터DB (Chroma / sqlite-vec)
   ↓
MCP 서버
   ├── search_apis(query, auth_free?, cors_ok?)
   ├── get_api_doc(name)       # 문서 fetch + 요약
   └── try_call(name, params)  # 샌드박스 호출
   ↓
Claude Code / 로컬 LLM 에이전트
```

### 3-6. React나 PHP로 만들 수 있는가 → 매우 적합

핵심은 **"README.md를 파싱해 JSON으로 만든 뒤 UI를 올린다"**.
데이터가 2MB 미만, 스키마가 6개 필드뿐이라 난이도가 낮습니다.

**🔵 React 버전 (프론트 단독 · 서버비 0원)**
```
[빌드 타임]  README.md → parse.js → apis.json (약 700KB)
[런타임]     React + Fuse.js(퍼지검색) + 필터 UI
[배포]       Vercel / Netlify / GitHub Pages  (전액 무료)
[갱신]       GitHub Actions로 매일 원본 pull → 재빌드 → 자동 배포
```
```jsx
const rows = [...md.matchAll(
  /^\| \[(.+?)\]\((http.+?)\) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|/gm
)].map(([,name,url,desc,auth,https,cors]) => ({
  name, url, desc, auth: auth.replace(/`/g,''), https, cors
}));
```
1,833건은 클라이언트 메모리에 통째로 올려도 부담이 없어 **DB도 API 서버도 불필요**합니다.

**🟢 PHP 버전 (백엔드 포함 · 수익화 유리)**
```
public-apis-hub/
├── cron/sync.php        # 매일 README 받아 파싱 → MySQL 적재
├── api/v1/search.php    # JSON API 제공 (API 키/과금 부착 지점)
├── api/v1/proxy.php     # ⭐ 핵심: 외부 API 대리 호출 (CORS 우회 + 키 은닉)
├── public/index.php     # 서버사이드 렌더링 (SEO 최강)
└── admin/               # 큐레이션, 통계, 결제
```
```php
$md = file_get_contents('https://raw.githubusercontent.com/public-apis/public-apis/master/README.md');
preg_match_all('/^\| \[(.+?)\]\((http.+?)\) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|/m', $md, $m, PREG_SET_ORDER);
```
PHP의 강점: **SEO**(API별 개별 상세 페이지 서버렌더링 → 롱테일 유입),
**프록시 서버**(CORS 불가 1,181개를 사용 가능하게 → 유료화 포인트), 저렴한 호스팅,
Laravel의 인증·결제(Cashier/Stripe)·큐 기본 제공.

**🏆 추천: 하이브리드**
```
React SPA (검색/필터 UX)  ←→  Laravel API (검색, 프록시, 과금, 통계)
                                    ↑ 매일 cron 동기화
                              public-apis README.md
```

**법적 확인**: 원본은 **MIT** → 재배포·가공·상업적 이용 허용.
**LICENSE 고지와 출처 표기만 유지**하면 됩니다. (APILayer 상표/로고는 제외)

---

## 4. 수익화 아이디어 (상세)

### 전제

1. 목록 자체는 MIT로 공짜이고 누구나 복제 가능 → **그대로 재배포로는 돈이 안 됨**
2. 돈은 **원본에 없는 것**에서 나옴 — 구조화 / 실시간성 / 레이트리밋·가격 정보 / 실행(프록시) / 에이전트 연동
3. APILayer가 이미 광고 모델로 수익화 중 → **다른 링에서 싸울 것**

### 💎 아이디어 1 — MCP 서버 "API Finder for AI Agents" ⭐최우선

Claude Code / Cursor / 로컬 에이전트가 붙여 쓰는 MCP 서버.
코딩 에이전트 시장은 폭발했는데 **"어떤 외부 API를 쓸지" 판단을 돕는 MCP는 거의 비어 있음**.
에이전트의 최대 약점인 엔드포인트 환각을 정확히 메웁니다.

```
search_apis(query, auth_free?, cors_ok?, category?)  → 검증된 후보 N개
get_api_spec(name)          → 엔드포인트/파라미터/인증법/무료한도 (★독자 데이터)
generate_client(name, lang) → JS/TS/Python/PHP 호출 코드 생성
health_check(name)          → 실시간 가동 상태 + 응답속도
```

| 티어 | 가격 | 내용 |
|:---|:---|:---|
| Free | $0 | 검색 무제한, 스펙 조회 월 50회 |
| Pro | **$9/월** | 무제한 + 코드생성 + 헬스체크 + 레이트리밋 DB |
| Team | **$49/월** | 팀 공유, 사내 API 등록, SSO |

**해자**: 원본에 없는 ①OpenAPI 스펙 ②무료 한도/가격 ③실시간 가동률
**난이도** 중 · **초기 투자** 낮음 · **MVP** 3~4주

### 💎 아이디어 2 — 통합 프록시 게이트웨이 "One Key, All APIs"

사용자는 **내 키 하나**로 수백 개 무료 API 호출. 서버가 라우팅·캐싱·CORS 해결·쿼터 관리.

해결하는 통증:
- `CORS: No/Unknown` **1,181개**를 프론트엔드에서 사용 가능하게 만듦 ✅
- 키 10개 관리 → 1개로 통합 ✅
- 무료 티어 초과 걱정 → 캐싱으로 호출 수 급감 ✅
- 프론트 키 노출 위험 → 서버에 은닉 ✅

```
사용자 앱 ──(내 키 1개)──> [게이트웨이] ──> 실제 API들
                              ├ 캐싱(Redis)
                              ├ CORS 헤더 부착
                              ├ 쿼터/과금 측정
                              └ 장애 시 대체 API 폴백
```
**수익**: 종량제 (월 1만 콜 무료 → 10만 콜 $19 → 100만 콜 $99)
**⚠️ 리스크**: 각 API의 ToS에서 **재판매/중계 금지** 조항 확인 필수.
명시적 허용 API만 선별 편입 → 이 검증 자체가 진입장벽이 됨.
**난이도** 중상 · **수익 잠재력** 최상 (APILayer가 이 모델로 회사를 만듦)

### 💎 아이디어 3 — 프리미엄 데이터셋 판매 (가장 빠른 현금화)

원본에 없는 필드를 붙인 구조화 데이터셋 판매.

| 필드 | 원본 | 내 데이터셋 |
|:---|:---:|:---:|
| 이름/URL/설명/Auth/HTTPS/CORS | ✅ | ✅ |
| 실제 base endpoint | ❌ | ✅ |
| OpenAPI 스펙 | ❌ | ✅ |
| 무료 한도 (요청/일·월) | ❌ | ✅ |
| 유료 전환 가격 | ❌ | ✅ |
| 30일 가동률·평균 응답속도 | ❌ | ✅ |
| 상업적 이용 가능 여부 | ❌ | ✅ |
| 한국어 설명 | ❌ | ✅ |

**판매처**: Gumroad / Lemon Squeezy / RapidAPI / Kaggle
**가격**: 1회 $49~$99, 월간 업데이트 구독 $15/월
**장점**: 2~3주 내 현금화, 인프라 부담 0, **아이디어 1·2의 기반 자산**이 됨
**난이도** 하 · **추천도** ⭐⭐⭐

### 💎 아이디어 4 — 한국어 특화 포털

원본은 100% 영어이고 **한국 공공데이터(data.go.kr) 커버리지가 거의 0** → 큰 빈틈.

- 1,833개 전부 한국어 번역 + 한국어 검색
- **공공데이터포털/서울열린데이터/네이버·카카오 API 수백 개 추가** (순수 증분)
- API별 한국어 실전 예제 (React / PHP / Spring / Flutter)
- 국내 관심사 태그: "토스처럼 만들기", "배민 클론에 쓸 API"

**수익**: 애드센스/제휴 → 멤버십 월 5,900원 → **전자책/인프런 강의** → 기업 스폰서
**난이도** 하~중 · **강점** 경쟁자 사실상 없음, SEO 선점 가능

### 💎 아이디어 5 — API 상태 모니터링 SaaS

이 레포는 매일 1회 생존 여부만 확인 → 이를 상품급으로 격상.
- 5분 간격 헬스체크 + 응답속도/가동률 기록
- 공개 상태 페이지 (무료, SEO 유입 엔진)
- 내가 쓰는 API 장애 시 Slack/이메일 알림 (유료)
- 히스토리 그래프, SLA 리포트

**수익**: 무료 → Pro $12/월(알림 10개) → Team $59/월
**보너스**: 가동률 데이터가 아이디어 3의 프리미엄 필드로 재활용 → 인프라 하나가 상품 둘을 먹임
**난이도** 중 · 인프라 비용 관리 주의

### 💎 아이디어 6 — 노코드 "API → 앱" 생성기

무인증+CORS 372개를 골라 클릭 몇 번으로 동작하는 앱 생성.
```
[API 선택] → [템플릿: 대시보드/카드/지도/차트] → [배포]
```
**수익**: 앱 3개 무료 → Pro $15/월 (무제한 + 커스텀 도메인 + 브랜딩 제거)
**타깃**: 비개발자, 기획자, 학생, 해커톤 참가자
**난이도** 상 · 차별성 최고

### 💎 아이디어 7 — 교육 콘텐츠 (최저위험)

- 유데미/인프런 강의: "공짜 API 1833개로 배우는 실전 웹개발" (51개 카테고리 = 커리큘럼)
- 뉴스레터: 주간 "이번 주의 무료 API 5선" → 구독자 → 스폰서 광고
- 유튜브: "이 API로 30분 만에 앱 만들기"
- 템플릿 마켓: API별 스타터 킷 ($9~29)

**난이도** 하 · **초기 투자** 거의 0 · **장점** 다른 아이디어의 마케팅 채널

### 📊 종합 비교

| # | 아이디어 | 난이도 | 수익잠재력 | 회수속도 | 차별성 | 총평 |
|:--|:---|:---|:---|:---|:---|:---|
| 1 | MCP 서버 | 중 | ★★★★★ | 중 | ★★★★★ | 🥇 시장 타이밍 최적 |
| 2 | 프록시 게이트웨이 | 중상 | ★★★★★ | 중 | ★★★★ | 🥈 검증된 모델(ToS 주의) |
| 3 | 프리미엄 데이터셋 | 하 | ★★★ | **빠름** | ★★★ | 🥉 첫 삽으로 최적 |
| 4 | 한국어 포털 | 하~중 | ★★★ | 중 | ★★★★★ | 경쟁자 없음 |
| 5 | 모니터링 SaaS | 중 | ★★★ | 느림 | ★★★ | 데이터 자산화 |
| 6 | 노코드 생성기 | 상 | ★★★★ | 느림 | ★★★★★ | 하이리스크 하이리턴 |
| 7 | 교육 콘텐츠 | 하 | ★★ | 빠름 | ★★ | 병행 필수 |

### 🎯 추천 실행 로드맵

**1단계 (0~1개월) 자산 만들기 — #3 + #7**
README 파싱 → 상위 300개 API에 엔드포인트/무료한도/가격 보강 → 데이터셋 판매 시작.
동시에 뉴스레터로 잠재고객 확보. 여기서 만든 `enriched.json`이 **모든 후속 제품의 원료**.

**2단계 (1~3개월) 제품화 — #1**
데이터셋을 MCP 서버로 감쌈. 무료 배포로 확산 → Pro 전환. 1단계 구독자가 초기 사용자.

**3단계 (3~6개월) 스케일 — #2 또는 #4**
ToS가 명확히 허용하는 API부터 프록시 게이트웨이(글로벌) 또는 한국어 포털(국내 선점).

### ⚠️ 공통 법적 체크리스트

1. public-apis는 **MIT** → 재배포/상업이용 OK, **LICENSE와 출처 표기 유지**
2. **APILayer 상표·로고·UTM 링크는 제거**할 것
3. **개별 API의 ToS는 각각 다름** — 특히 프록시/캐싱/재판매의 명시적 허용 여부 확인 필수
4. 데이터셋 판매 시 "원본 목록은 무료 공개이며 본 상품은 부가 가공 데이터임" 명시

---

## 5. 한 줄 요약

> **public-apis는 "실행되는 소프트웨어"가 아니라 "매일 자동 검증되는 무료 API 1,833개의 주소록"이며,
> 진짜 가치는 목록 자체가 아니라 그 위에 무엇을 얹느냐(구조화 · 실행 · 에이전트 연동)에 있습니다.**

---

*작성일: 2026-09-29 · 저장소: https://github.com/bmshin94/public-apis*
