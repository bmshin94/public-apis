# public-apis 전수조사 · 활용 · 수익화 대화 정리 (한국어)

> 이 문서는 `public-apis` 저장소를 **파일 24개 / README 2,330줄 전수조사**한 결과와,
> 활용법 · 기술 정체성 · 로컬 에이전트 연계 · 수익화 아이디어에 대한 대화를 정리한 기록입니다.
> 작성일: 2026-09-29

---

## 📎 관련 GitHub 주소

| 구분 | 주소 |
|:---|:---|
| 이 저장소 (내 포크) | https://github.com/bmshin94/public-apis |
| 작업 브랜치 | https://github.com/bmshin94/public-apis/tree/claude/festive-gauss-pfpela |
| 원본 저장소 | https://github.com/public-apis/public-apis |
| 기여 가이드 | https://github.com/public-apis/public-apis/blob/master/CONTRIBUTING.md |
| 이슈 | https://github.com/public-apis/public-apis/issues |
| 풀 리퀘스트 | https://github.com/public-apis/public-apis/pulls |
| 이 목록의 JSON API (서드파티) | https://github.com/davemachado/public-api |
| 운영 주체 (APILayer) | https://apilayer.com |
| APILayer Postman 컬렉션 | https://www.postman.com/apilayer/apilayer/collection/2uo8qbu/apilayer-suite |

---

## 1. 이게 뭐 하는 물건인가 (전수조사 결과)

### 1-1. 정체 — 코드가 아니라 "목록(데이터)"

실행되는 프로그램도, 라이브러리도 아니다. **전 세계 무료 공개 API를 사람이 손으로 정리한
큐레이션 목록**이며 `README.md` 한 개가 프로젝트의 99%다.

```
public-apis/                     파일 24개
├── README.md              259KB / 약 2,330줄   💥 프로젝트 본체
├── CONTRIBUTING.md          6KB  기여 규칙 (매우 깐깐)
├── CLAUDE.md                1KB  프로젝트 가이드
├── LICENSE                       MIT
├── .gitattributes / .gitignore
│
├── scripts/                      ← 본체 아님. README를 지키는 "문지기"
│   ├── validate/format.py        표 형식 검사기 (278줄)
│   ├── validate/links.py         링크 생존 검사기 (274줄)
│   ├── tests/test_validate_format.py
│   ├── tests/test_validate_links.py
│   ├── github_pull_request.sh    PR diff 검증
│   ├── requirements.txt          requests 등 5개
│   └── README.md                 스크립트 사용법
│
└── .github/
    ├── workflows/                GitHub Actions 3개
    ├── ISSUE_TEMPLATE.md
    ├── PULL_REQUEST_TEMPLATE.md
    └── assets/                   APILayer 배너·로고
```

핵심: **코드는 총 552줄뿐**이고, 그 코드마저 "README가 망가지지 않게 감시하는 역할"이다.

### 1-2. 실측 통계 (직접 집계)

| 항목 | 수치 |
|:---|:---|
| **총 API 개수** | **약 1,832개** (표 행 1,843개 − APILayer 스폰서 11행) |
| **카테고리 수** | **51개** |
| 인증 불필요 (`No`) | **867개 (47.3%)** |
| API 키 필요 (`apiKey`) | 802개 (43.8%) |
| OAuth 필요 | 150개 (8.2%) |
| `X-Mashape-Key` / `User-Agent` | 7개 |
| HTTPS 미지원 | 91개 (나머지 약 1,741개 지원) |
| CORS `Unknown` | 1,002개 (미확인) |
| **무인증 + CORS 가능** | **372개** ⭐ 서버 없이 브라우저 직접 호출 가능 |

카테고리 51개: Animals, Anime, Anti-Malware, Art & Design, Authentication & Authorization,
Blockchain, Books, Business, Calendar, Cloud Storage & File Sharing, Continuous Integration,
Cryptocurrency, Currency Exchange, Data Validation, Development, Dictionaries,
Documents & Productivity, Email, Entertainment, Environment, Events, Finance, Food & Drink,
Games & Comics, Geocoding, Government, Health, Jobs, Machine Learning, Music, News, Open Data,
Open Source Projects, Patent, Personality, Phone, Photography, Programming, Science & Math,
Security, Shopping, Social, Sports & Fitness, Test Data, Text Analysis, Tracking,
Transportation, URL Shorteners, Vehicle, Video, Weather

### 1-3. 데이터 형식 (5개 컬럼이 전부)

```markdown
### Animals
| API | Description | Auth | HTTPS | CORS |
|:---|:---|:---|:---|:---|
| [Axolotl](https://theaxolotlapi.netlify.app/) | Collection of axolotl pictures and facts | No | Yes | No |
| [Cats](https://docs.thecatapi.com/) | Pictures of cats from Tumblr | `apiKey` | Yes | No |
| [Dogs](https://dog.ceo/dog-api/) | Based on the Stanford Dogs Dataset | No | Yes | Yes |
```

**[이름](문서링크) / 설명 / 인증방식 / HTTPS / CORS**

### 1-4. scripts/ 자동 품질관리 장치

**`scripts/validate/format.py` — 표 형식 검사기**
- 카테고리 내부 알파벳 순서 (`check_alphabetical_order`)
- 5개 컬럼 존재, 셀 좌우 공백 정확히 1칸
- 제목이 `[TITLE](LINK)` 문법인지, `... API`로 끝나면 탈락
- 설명: 첫 글자 대문자 / 구두점으로 끝나지 않음 / **100자 이내**
- Auth 값은 `apiKey`·`OAuth`·`X-Mashape-Key`·`User-Agent`·`No` 중 하나 + 백틱
- HTTPS는 `Yes`/`No`, CORS는 `Yes`/`No`/`Unknown`
- 새 카테고리는 최소 3개 항목 + 상단 Index 등록 필수

**`scripts/validate/links.py` — 링크 생존 검사기**
- 중복 링크 탐지 (`-odlc` 옵션은 이것만 빠르게)
- 실제 HTTP 요청으로 생존 확인 (timeout 25초)
- **User-Agent를 브라우저 4종으로 위장** (`fake_user_agent`) — 봇 차단 회피
- **Cloudflare 오탐 방지** (`has_cloudflare_protection`):
  403/503 + `Server: cloudflare` + 특징 문자열 18개 조합으로 "죽은 링크 vs 방어벽" 구분
- 에러를 SSL / 연결오류 / 타임아웃 / 리다이렉트 과다 / 미상 5종으로 분류

**`.github/workflows/` — GitHub Actions 3개**

| 워크플로 | 시점 | 하는 일 |
|:---|:---|:---|
| `test_of_push_and_pull.yml` | push / PR | 형식 검사 + PR에서 추가된 줄의 링크만 생존 확인 |
| `test_of_validate_package.yml` | push / PR | 검증 스크립트 자체의 유닛테스트 |
| `validate_links.yml` | **매일 자정 cron** | 1,800여 개 링크 전수 생존 점검 |

즉 이 프로젝트는 **"사람이 데이터를 넣고, 봇이 품질을 지키는"** 구조다.

---

## 2. 쉽게 이해하기

### 2-1. 비유 — "전국 맛집 지도"

| 현실 세계 | public-apis |
|:---|:---|
| 맛집 지도 | README.md |
| 가게 주소 | API 문서 링크 |
| "예약 필요?" | Auth 컬럼 (`No` = 그냥 사용, `apiKey` = 가입 필요) |
| "카드 되나요?" | HTTPS 컬럼 |
| "배달 되나요?" | CORS 컬럼 (브라우저 직접 호출 가능 여부) |
| 지도 편집자들 | 기여자 380명+ |
| 매일 문 열었나 확인하는 알바 | `validate_links.py` (매일 자정 cron) |

지도는 밥을 만들어주지 않지만, 지도 없이는 재료 찾다 하루가 간다.

### 2-2. API 개념

```
내 코드 ──(요청: "서울 날씨 줘")──▶ 남의 서버
       ◀──(응답: {"temp": 23, "sky": "맑음"})──
```

기상 관측소를 지을 필요 없이 주소로 요청만 보내면 데이터가 온다. 그 주소 1,832개 모음집.

### 2-3. 3개 컬럼의 실전 의미

**`Auth` = 문 앞 경비원**

| 값 | 의미 | 난이도 |
|:---|:---|:---|
| `No` | 경비원 없음 | ⭐ 즉시 사용 (867개) |
| `apiKey` | 가입 → 키 발급 → 요청에 첨부 | ⭐⭐ 10분 (802개) |
| `OAuth` | 사용자 로그인 동의 필요 | ⭐⭐⭐⭐ 서버 필수 (150개) |

**`CORS` = 브라우저가 직접 호출해도 받아주나 (매우 중요)**

```javascript
// CORS: Yes → React에서 바로 됨, 백엔드 불필요
fetch('https://dog.ceo/api/breeds/image/random')

// CORS: No  → 브라우저가 차단. 내 서버(PHP/Node)가 대신 호출해야 함
```

| 값 | 뜻 | 해야 할 일 |
|:---|:---|:---|
| `Yes` | 직접 호출 OK | React만으로 완성 |
| `No` | 차단 | PHP/Node 프록시 필요 |
| `Unknown` | 미확인 (1,002개) | 직접 테스트 필요 |

**→ "Auth: No + CORS: Yes" 372개가 보물.** 가입 X, 서버 X, 결제 X → HTML 한 장으로 앱 완성.

### 2-4. 48만 스타의 의미

| 프로젝트 | 스타 |
|:---|:---|
| **public-apis** | **~48만** |
| freeCodeCamp | ~41만 |
| React | ~23만 |
| Vue | ~20만 |
| Linux 커널 | ~18만 |

코드 552줄짜리 문서가 React의 2배, Linux의 2.7배. **"기술 난이도 ≠ 가치"**의 증거.

### 2-5. 실전 사용 흐름

```
1. "고양이 사진 앱 만들고 싶다"
2. README에서 Ctrl+F → Animals 카테고리
3. 표 확인:
   [Cats](docs.thecatapi.com) | `apiKey` | Yes | No   ← 키 필요 + CORS 막힘 ❌
   [Dogs](dog.ceo/dog-api)    | No       | Yes | Yes  ← 바로 가능 ✅
4. 문서 링크 → 엔드포인트 확인
5. fetch('https://dog.ceo/api/breeds/image/random')
6. 완성 (5분, 0원)
```

### 2-6. 단점 (솔직하게)

1. README 한 개에 2,330줄 → 무겁고, 검색은 Ctrl+F뿐 (← **수익화 포인트**)
2. CORS `Unknown` 1,002개(55%) → 절반 이상 직접 테스트 필요
3. "무료 티어"의 함정 — 월 1,000건 제한 등은 표에 없음. 문서 직접 확인 필수
4. 상단에 APILayer(상업 회사) 광고 11행 — 운영 주체가 APILayer
5. 링크가 죽어도 항목 삭제까지 시간차 존재

---

## 3. 질문 7개 정리

### Q1. 설치 및 사용법?

**"설치" 개념이 없다.** 웹사이트를 보면 끝.

```bash
# 방법 B — 클론
git clone https://github.com/bmshin94/public-apis

# 방법 C — 검증 스크립트 (기여자용, Python 3.8+)
python -m pip install -r scripts/requirements.txt
python scripts/validate/format.py README.md          # 형식 검사 (수 초)
python scripts/validate/links.py README.md           # 링크 전수 검사 (1시간+)
python scripts/validate/links.py README.md -odlc     # 중복만 빠르게 (추천)
cd scripts && python -m unittest discover tests/ --verbose
```

**기여 규칙 요약**: 알파벳 순서 / 설명 100자 이내 / 첫 글자 대문자 / 마침표 금지 /
이름이 `API`로 끝나면 안 됨 / **PR 1개당 링크 1개** / PR 제목 `Add Blockchain API` 형식 /
커밋 squash / `master` 브랜치 타겟

### Q2. 플러그인? 스킬? MCP?

**셋 다 아니다. 그냥 문서(데이터)다.**

| 구분 | public-apis |
|:---|:---|
| 플러그인 | ❌ 끼울 데가 없음 |
| Claude Skill | ❌ `SKILL.md` 없음 |
| MCP | ❌ 서버가 아님 |
| 라이브러리 | ❌ import 불가 |
| **데이터셋 / 큐레이션 문서** | ✅ **정답** |

단, 이걸 **재료로 써서** 세 개 다 만들 수 있다.

```
public-apis (README.md)
   ├─▶ 파싱 → JSON → MCP 서버 ("AI야, 날씨 API 찾아줘")
   ├─▶ SKILL.md 작성 → Claude Skill ("무료 API 추천 스킬")
   └─▶ VS Code Extension → 에디터에서 검색 → 코드 자동 삽입
```

**핵심 인사이트: 이건 "부품"이고, 제품은 내가 만든다.**

### Q3. API 토큰이 필요한가?

**이 저장소 자체는 토큰이 전혀 필요 없다** (문서일 뿐).
여기 실린 API를 쓸 때만 갈린다.

| 경우 | 개수 | 토큰 | 방법 |
|:---|:---:|:---|:---|
| `Auth: No` | 867개 | ❌ | `fetch(url)` 끝 |
| `Auth: apiKey` | 802개 | ✅ | 가입 → 키 발급 → 요청에 첨부 |
| `Auth: OAuth` | 150개 | ✅ | 사용자 동의 흐름 (서버 필수) |

무인증 API 예시:
```javascript
fetch('https://dog.ceo/api/breeds/image/random').then(r=>r.json()).then(console.log)
fetch('https://api.open-meteo.com/v1/forecast?latitude=37.56&longitude=126.97&current_weather=true')
  .then(r=>r.json()).then(console.log)
fetch('https://catfact.ninja/fact').then(r=>r.json()).then(console.log)
```

**키 보안 필수**
```javascript
// ❌ 프론트엔드에 키 노출 — 브라우저에서 다 보임
const KEY = "sk_live_abcd1234";

// ✅ 서버에 숨기고 프론트는 내 서버만 호출
fetch('/api/weather')
```
환경변수(`.env`) 사용 + `.gitignore` 등록 필수. 깃허브에 키가 올라가면 봇이 수 분 내에 수집한다.

### Q4. 왜 깃허브에서 유명한가?

1. **고통이 보편적** — 개발자 100%가 "이 데이터 어디서 구하지?"를 겪는다
2. **진입장벽 0** — 가입/설치/학습 불필요, 링크 열면 즉시 가치
3. **기여 문턱이 극히 낮음** — 한 줄 추가로 컨트리뷰터 → 기여자 380명+ → 선순환
4. **스타 = 개인 북마크** — 즐겨찾기 성격이라 폭발적으로 누적
5. **SEO 지배** — "free public api" 검색 1위, 구글 트래픽이 스타를 만든다
6. **자동화로 품질 유지** — 매일 cron 링크 검사 → 다른 awesome-list처럼 썩지 않는다
7. **기업이 운영 인수** — APILayer가 관리해서 유지보수가 끊기지 않는다 (대신 광고 부착)

**교훈: 정리·큐레이션 자체가 상품이 된다.**

### Q5. 로컬 에이전트 구축에 도움이 되나?

**매우 도움 된다. 단, "그대로"가 아니라 "가공해서" 써야 한다.**

❌ 실패하는 방법: README 2,330줄을 프롬프트에 전부 넣기 → 토큰 25만+ 폭발

✅ 성공하는 방법 4단계:

**1단계 — README → 구조화 데이터 파싱 (Python)**
```python
import re, json
row = re.compile(r'^\| \[(.+?)\]\((http.+?)\) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|?')
apis, category = [], None
for line in open('README.md', encoding='utf-8'):
    if line.startswith('### '):
        category = line[4:].strip()
    m = row.match(line.strip())
    if m and category:
        apis.append({
            'name': m.group(1), 'url': m.group(2),
            'desc': m.group(3), 'auth': m.group(4).strip('`'),
            'https': m.group(5), 'cors': m.group(6),
            'category': category,
        })
json.dump(apis, open('apis.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
```

**2단계 — 임베딩 → 벡터DB (RAG)**
```
apis.json → 항목별 임베딩 → Chroma/Qdrant
→ "환율 데이터 필요해" → 의미 검색 → 관련 API 5개만 컨텍스트 주입
→ 토큰 25만 → 500토큰
```

**3단계 — MCP 서버로 감싸기**
```
search_apis(query, auth_filter, cors_filter)   API 검색
get_api_detail(name)                            상세 정보
test_api_alive(url)                             생존 확인
suggest_stack(idea)                             아이디어 → 필요 API 조합 추천
generate_snippet(name, lang)                    복붙 코드 생성
```

**4단계 — 에이전트가 직접 호출**
```
"오늘 서울 날씨 알려줘"
 → search_apis("weather", auth="No") → Open-Meteo 발견
 → 실제 HTTP 호출 → "서울 23도 맑음"
```

**무인증 867개 = 인증 절차 없이 에이전트가 즉시 쓸 수 있는 도구 867개.**
`scripts/validate/links.py`를 재활용하면 "죽은 도구 자동 제외"도 바로 구현된다.
MIT 라이선스이므로 상업적 이용·재가공·판매 모두 자유.

### Q6. 수익화 아이디어가 있나?

있다 → **4장에서 상세히 정리.**

### Q7. React나 PHP로 만들 수 있나?

**100% 가능. 오히려 React + PHP 조합이 정답에 가깝다.**

```
┌─────────────────────────────────────────────┐
│  React (프론트엔드)                          │
│  - 검색 UI, 필터, 카드 리스트                │
│  - CORS: Yes 인 API는 여기서 직접 호출       │
└────────────────┬────────────────────────────┘
┌────────────────▼────────────────────────────┐
│  PHP (백엔드 / 프록시)                       │
│  - CORS: No 인 API 대신 호출                 │
│  - apiKey 숨기기, 캐싱, 사용량 제한, 결제    │
└────────────────┬────────────────────────────┘
        ┌────────▼────────┐
        │ apis.json / MySQL│  ← README 파싱 결과
        └─────────────────┘
```

**PHP 파서**
```php
<?php
$lines = file('README.md');
$apis = []; $category = null;
foreach ($lines as $line) {
    $line = trim($line);
    if (str_starts_with($line, '### ')) { $category = substr($line, 4); continue; }
    if (preg_match('/^\|\s*\[(.+?)\]\((http.+?)\)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|?$/', $line, $m)) {
        $apis[] = [
            'name' => $m[1], 'url' => $m[2], 'desc' => $m[3],
            'auth' => trim($m[4], '`'), 'https' => $m[5],
            'cors' => $m[6], 'category' => $category,
        ];
    }
}
file_put_contents('apis.json', json_encode($apis, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
echo count($apis) . "개 파싱 완료\n";
```

**PHP 프록시 (CORS 우회 + 키 숨김)**
```php
<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json; charset=utf-8');

$target = $_GET['url'] ?? '';
$allow = ['api.example.com', 'api.another.com'];   // 화이트리스트 필수
if (!in_array(parse_url($target, PHP_URL_HOST), $allow, true)) {
    http_response_code(400);
    exit(json_encode(['error' => 'not allowed']));
}

$key = getenv('MY_API_KEY');        // .env 에서 로드, 코드에 하드코딩 금지
$ch = curl_init($target);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HTTPHEADER => ["Authorization: Bearer $key"],
    CURLOPT_TIMEOUT => 15,
]);
echo curl_exec($ch);
```
⚠️ 화이트리스트가 없으면 **SSRF 취약점**이 된다. 임의 URL을 받으면 내부망 접근이 가능해지므로 반드시 차단.

**React 검색 컴포넌트**
```jsx
import { useState, useMemo, useEffect } from 'react';

export default function ApiExplorer() {
  const [apis, setApis] = useState([]);
  const [q, setQ] = useState('');
  const [noAuthOnly, setNoAuthOnly] = useState(false);
  const [corsOnly, setCorsOnly] = useState(false);

  useEffect(() => { fetch('/apis.json').then(r => r.json()).then(setApis); }, []);

  const filtered = useMemo(() => apis.filter(a =>
    `${a.name} ${a.desc} ${a.category}`.toLowerCase().includes(q.toLowerCase()) &&
    (!noAuthOnly || a.auth === 'No') &&
    (!corsOnly   || a.cors === 'Yes')
  ), [apis, q, noAuthOnly, corsOnly]);

  return (
    <div>
      <input value={q} onChange={e => setQ(e.target.value)} placeholder="API 검색... 예: weather" />
      <label><input type="checkbox" checked={noAuthOnly} onChange={e => setNoAuthOnly(e.target.checked)} /> 키 없이 사용 가능 (867개)</label>
      <label><input type="checkbox" checked={corsOnly} onChange={e => setCorsOnly(e.target.checked)} /> 브라우저 직접 호출 가능</label>
      <p>{filtered.length}개 발견</p>
      {filtered.map(a => (
        <a key={a.url} href={a.url} target="_blank" rel="noreferrer">
          <h4>{a.name} <small>{a.category}</small></h4>
          <p>{a.desc}</p>
          <span>{a.auth === 'No' ? '🔓 무인증' : `🔑 ${a.auth}`} · CORS {a.cors}</span>
        </a>
      ))}
    </div>
  );
}
```

**현실적 개발 일정**

| 단계 | 작업 | 기간 |
|:---|:---|:---|
| 1 | README 파서 (PHP/Python) | 0.5일 |
| 2 | React 검색 UI | 2일 |
| 3 | 배포 (Vercel / 공유호스팅) | 0.5일 |
| **MVP** | | **3일** |
| 4 | PHP 프록시 + 캐시 | 2일 |
| 5 | 생존 체크 배치 (cron) | 1일 |
| 6 | 회원 / 결제 | 3~5일 |

---

## 4. 수익화 아이디어

> 전제: public-apis는 **MIT 라이선스** → 파싱·재가공·상업적 판매 모두 합법.
> 단, "목록을 그대로 복사한 사이트"는 가치가 없다. **가공·검증·연결**에서 수익이 나온다.

### 티어 1 — 현실적이고 빠른 수익

#### 아이디어 1. 무료 API 검색 SaaS (정석)

**문제**: README 2,330줄, 검색은 Ctrl+F뿐. CORS Unknown 1,002개(55%)로 실사용 가능 여부 불명.

**해결**: 검증된 메타데이터 + 강력한 필터
- 실시간 생존 상태 (죽은 API 자동 숨김)
- **CORS 실측** — Unknown 1,002개를 직접 테스트해 Yes/No 확정 ← 최대 차별점
- **무료 티어 한도 정리** (월 몇 건? 유료 전환 조건?) ← README에 없는 정보
- 응답 속도 / 안정성 점수
- 언어별 복붙 코드 스니펫 자동 생성 (JS / PHP / Python / cURL)

| 플랜 | 가격 | 내용 |
|:---|:---|:---|
| Free | $0 | 검색 + 기본 정보 (SEO 유입용) |
| Pro | $9/월 | 생존 알림, CORS 실측, 고급 필터, 즐겨찾기 |
| API | $29/월 | 카탈로그를 JSON API로 제공 |
| 광고 | - | 유료 API 업체 스폰서 배치 |

난이도 ⭐⭐ / 기간 1~2주 / 예상 월 $300~3,000

#### 아이디어 2. 어필리에이트 리뷰 미디어 (진입 최易)

무료 API 사용자의 상당수가 유료로 전환한다. 그 전환에 수수료가 붙는다.

- "무료 날씨 API 41개 비교 — 실제 테스트 순위" 형식 콘텐츠
- 카테고리 51개 → 비교 리뷰 51편
- 유료 API 업체 어필리에이트 링크 삽입
- SEO 롱테일: "free weather api no key", "무료 환율 api"

수익: 어필리에이트 15~30% + 애드센스 + 스폰서 리뷰
난이도 ⭐ (개발 거의 없음) / 예상 월 $200~5,000
→ **초기 투자 대비 회수율 최고.**

#### 아이디어 3. MCP 서버 / Claude Skill 판매 (타이밍 최적)

AI 에이전트 붐인데 "에이전트가 쓸 도구 카탈로그"가 부족하다.

제품: `free-api-finder` MCP 서버
```
search_apis(query, auth, cors)   무료 API 검색
get_api_detail(name)             상세 + 인증 방법
test_api(url)                    실제 호출 테스트
suggest_stack(idea)              "여행앱" → 필요 API 조합 추천
generate_snippet(name, lang)     복붙 코드 생성
```

- 기본 무료 배포 (GitHub 스타 = 마케팅)
- Pro $5~15/월: 생존 검증 + CORS 실측 + 무료 한도 DB
- 기업 라이선스 $99~499/월 (사내 에이전트 탑재)
- 컨설팅: "귀사 AI 에이전트에 도구 연결"

난이도 ⭐⭐⭐ / 기간 2~3주 / 예상 월 $200~2,000 + 컨설팅 건당 $2,000~

#### 아이디어 4. 노코드 API 위젯 생성기 (비개발자 타깃)

```
"고양이 사진 위젯" 선택 → 색/크기 설정
  → <script src="widget.io/cat/abc123"></script>
  → 블로그/노션/워드프레스에 붙이면 끝
```

위젯: 날씨, 환율, 코인 시세, 명언, 뉴스 헤드라인, 주식, 랜덤 이미지, 운세 등
수익: Free(워터마크) / Pro $5~12월 / 워드프레스 플러그인 유료판
난이도 ⭐⭐ / 기간 2주 / 예상 월 $300~2,000

### 티어 2 — 크게 성장할 수 있는 것

#### 아이디어 5. 통합 프록시 API (APILayer의 무료판)

**문제**: 무료 API 10개 사용 → 키 10개 관리, CORS 각기 다름, 응답 포맷 제각각, 하나 죽으면 서비스 중단

**해결**: 하나의 키로 통합
```javascript
fetch('https://ourapi.com/v1/weather?city=seoul', {headers:{'X-Key': MY_KEY}})
fetch('https://ourapi.com/v1/currency?from=USD&to=KRW', {headers:{'X-Key': MY_KEY}})
```
- CORS 전부 해결 (우리가 프록시)
- **자동 폴백**: A가 죽으면 같은 기능의 B로 자동 전환 ← 킬러 기능
- 응답 포맷 통일 + 캐싱으로 무료 한도 절약
- 사용량 대시보드

수익: Free 1,000콜/월 → Starter $19 → Pro $49 → Business $199
난이도 ⭐⭐⭐⭐ / 기간 1~2개월 / 예상 월 $500~20,000
⚠️ 무료 API의 **재판매·캐싱 금지 조항** 반드시 확인.

#### 아이디어 6. API 모니터링 서비스

`scripts/validate/links.py` 로직을 확장해 제품화.
- 사용 중인 API 등록 → 5분마다 헬스체크 → 장애 시 슬랙/이메일 알림
- 응답 속도 추이 그래프, 대체 API 추천, 상태 페이지 위젯

수익: Free 3개 → $9(20개) → $29(100개) → 팀 $99
난이도 ⭐⭐⭐ / 예상 월 $300~5,000

#### 아이디어 7. 테마별 API 번들 + 보일러플레이트 판매

```
날씨앱 스타터킷 ($29)       React+PHP + 날씨/지오코딩/시간대 연동 완성본
핀테크 대시보드 킷 ($49)    환율+주식+코인 + 차트 완성본
게임 정보 허브 킷 ($39)
```
한 번 제작 후 반복 판매 (Gumroad / Lemon Squeezy)
난이도 ⭐⭐ / 예상 건당 $29~79, 월 $200~2,000 (패시브)

### 티어 3 — 틈새 / 부가 수익

| # | 아이디어 | 수익 | 난이도 |
|:--:|:---|:---|:--:|
| 8 | 한국 특화판 — 공공데이터포털 + 국내 API 한글 큐레이션 | 광고/스폰서 | ⭐ |
| 9 | 뉴스레터 — "주간 무료 API" 매주 3개 소개 | 스폰서 $100~500/회 | ⭐ |
| 10 | 유튜브/블로그 — "무료 API로 앱 만들기" 시리즈 | 광고 + 강의 유입 | ⭐⭐ |
| 11 | 온라인 강의 — "무료 API로 사이드프로젝트 10개" | 인프런/유데미 | ⭐⭐ |
| 12 | VS Code 익스텐션 — 에디터에서 검색 → 코드 삽입 | 스폰서/Pro | ⭐⭐⭐ |
| 13 | 목데이터 SaaS — Test Data 카테고리 확장 | $9~29/월 | ⭐⭐⭐ |
| 14 | 기업 컨설팅 — "무료 API로 비용 절감" | 건당 $1,000~ | ⭐⭐ |

### 추천 실행 순서

```
[1단계 · 1주]   아이디어 2 (어필리에이트 리뷰 블로그)
                개발 0, SEO 씨앗 뿌리기. 트래픽이 모든 것의 기반
       ↓
[2단계 · 2주]   아이디어 1 (검색 SaaS, React + PHP)
                블로그 트래픽 유입. CORS 1,002개 실측이 차별점
       ↓
[3단계 · 3주]   아이디어 3 (MCP 서버)
                로컬 에이전트 프로젝트와 시너지. 무료 배포로 인지도
       ↓
[4단계 · 1~2달] 아이디어 5 (통합 프록시 API)
                앞 3개가 검증되면 본게임. 스케일이 나오는 지점
```

### 성공의 열쇠 3가지

1. **"목록 복사"로는 안 된다** — README를 그대로 옮긴 사이트는 이미 수십 개 있고 모두 실패했다.
   **검증된 정보(CORS 실측, 무료 한도, 생존 상태)**가 진짜 상품이다.
2. **CORS Unknown 1,002개가 금광** — 아무도 하지 않은 일이고, 자동 테스트로 채울 수 있다.
3. **SEO 먼저, 제품 나중** — "free api" 검색 트래픽 = 무한 리드. 블로그부터 시작.

### 리스크 체크

- 무료 API 이용약관 (재판매 / 캐싱 금지 조항) 확인 필수
- 프록시 서버는 SSRF 방어 + Rate limit 필수
- 무료 API의 갑작스러운 유료화 → 폴백 설계로 대응
- 개인정보 취급 API는 처리 방침 주의

---

## 5. 한 장 요약

| 질문 | 답 |
|:---|:---|
| 이게 뭐야? | 무료 공개 API 약 1,832개를 정리한 **큐레이션 문서** (README.md 하나) |
| 실행되는 프로그램? | ❌ 아니다. `scripts/`는 README 품질을 지키는 검증 도구일 뿐 |
| 플러그인/스킬/MCP? | ❌ 전부 아니다. **데이터셋**. 단, 이걸로 셋 다 만들 수 있다 |
| 토큰 필요? | 저장소 자체는 ❌. 개별 API는 867개 무인증 / 802개 apiKey / 150개 OAuth |
| 왜 유명해? | 보편적 고통 해결 + 진입장벽 0 + 기여 문턱 낮음 + SEO 독점 + 자동화 품질관리 |
| 로컬 에이전트에 도움? | ✅ 매우. 파싱 → 벡터DB → MCP 서버로 감싸면 도구 카탈로그 확보 |
| React/PHP로 가능? | ✅ React(UI) + PHP(프록시·키 숨김) 조합이 정답. MVP 3일 |
| 수익화? | 검색 SaaS / 어필리에이트 미디어 / MCP 판매 / 위젯 생성기 / 통합 프록시 API |
| 가장 큰 기회 | **CORS Unknown 1,002개를 실측해 확정하는 것** (아무도 안 했고, 자동화 가능) |
| 라이선스 | MIT — 재가공·상업적 판매 자유 |
