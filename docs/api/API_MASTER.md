# STEPi Backend API Master

## 기준과 검증 범위

- 기준 명세서: `STEPi_Backend_API_전체기능_명세서_v0.3_119개_통합본.docx`
- 기준 브랜치: `origin/main`
- 기준 커밋: `e4b1ab2`
- 점검일: 2026-10-24
- 공식 API: 119개(클라이언트 110개, INTERNAL 9개)
- 실제 OpenAPI: 4개(`GET /`, `GET /health`, `GET /health/db`, `GET /auth/status`) — 기준 `origin/main` 감사 결과
- 의존성 분류는 공식 명세의 확정 분류가 아닌 초기 Backend 분석 결과입니다.
- AUTH-01은 PR #5에서 테스트가 통과했지만 기준 main에 아직 merge되지 않아 `IN_PROGRESS`로 기록합니다.

## 집계

- BE_ONLY: 55
- CONTRACT_REQUIRED: 27
- AI_INTEGRATION: 37
- VERIFIED: 0
- IN_PROGRESS: 1
- NOT_STARTED: 118

## 상태 갱신 규칙

구현 상태는 Router 등록, 테스트, 현재 기준 브랜치 반영 여부를 함께 확인해 갱신합니다. AI Mock 또는 Schema만으로 `INTEGRATED`나 `VERIFIED`로 표시하지 않습니다.

## 공식 API 원장

### AUTH — 인증·사용자

| API ID | Method | 명세 Endpoint | 실제 Endpoint | 기능 | 의존성 | 구현 상태 | 테스트 | 연동 상태 | Issue/PR |
|---|---|---|---|---|---|---|---|---|---|
| AUTH-01 | POST | `/auth/signup` | /auth/signup (PR #5) | 회원가입 | BE_ONLY | IN_PROGRESS | PASSED | NOT_REQUIRED | PR #5 · 48deb43 |
| AUTH-02 | POST | `/auth/login` | — | 로그인 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| AUTH-03 | POST | `/auth/refresh` | — | 토큰 재발급 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| AUTH-04 | POST | `/auth/logout` | — | 로그아웃 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| AUTH-05 | GET | `/users/me` | — | 내 정보 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| AUTH-06 | PATCH | `/users/me` | — | 내 정보 수정 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| AUTH-07 | GET | `/me/student-profile` | — | 학생 프로필 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| AUTH-08 | PATCH | `/me/student-profile` | — | 학생 프로필 수정 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| AUTH-09 | PATCH | `/auth/password` | — | 현재 비밀번호 변경 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| AUTH-10 | DELETE | `/users/me` | — | 회원 탈퇴 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| AUTH-11 | GET | `/auth/check-email` | — | 이메일 중복 확인 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| AUTH-12 | POST | `/auth/password-reset/request` | — | 비밀번호 재설정 요청 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| AUTH-13 | POST | `/auth/password-reset/confirm` | — | 비밀번호 재설정 완료 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |

### CUR — 교육과정·Concept·Skill

| API ID | Method | 명세 Endpoint | 실제 Endpoint | 기능 | 의존성 | 구현 상태 | 테스트 | 연동 상태 | Issue/PR |
|---|---|---|---|---|---|---|---|---|---|
| CUR-01 | GET | `/curriculum/grades` | — | 학년 목록 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| CUR-02 | GET | `/curriculum/units` | — | 학년별 단원 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| CUR-03 | GET | `/concepts` | — | Concept 목록 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| CUR-04 | GET | `/concepts/{code}` | — | Concept 상세 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| CUR-05 | GET | `/skills` | — | Skill 목록 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| CUR-06 | GET | `/skills/{code}` | — | Skill 상세 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| CUR-07 | GET | `/skills/{code}/prerequisites` | — | 선수 Skill | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| CUR-08 | GET | `/curriculum/graph` | — | 교육과정 그래프 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |

### DIAG — Adaptive Level Test

| API ID | Method | 명세 Endpoint | 실제 Endpoint | 기능 | 의존성 | 구현 상태 | 테스트 | 연동 상태 | Issue/PR |
|---|---|---|---|---|---|---|---|---|---|
| DIAG-01 | POST | `/diagnostics` | — | 진단 시작 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| DIAG-02 | GET | `/diagnostics/{id}` | — | 진단 진행상태 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| DIAG-03 | GET | `/diagnostics/{id}/current-question` | — | 현재 진단문제 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| DIAG-04 | POST | `/diagnostics/{id}/answers` | — | 답안 제출 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| DIAG-05 | GET | `/diagnostics/{id}/results` | — | 진단 결과 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| DIAG-06 | GET | `/me/diagnostics` | — | 진단 이력 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |

### MAP — Knowledge Map

| API ID | Method | 명세 Endpoint | 실제 Endpoint | 기능 | 의존성 | 구현 상태 | 테스트 | 연동 상태 | Issue/PR |
|---|---|---|---|---|---|---|---|---|---|
| MAP-01 | GET | `/me/knowledge-map` | — | 전체 Knowledge Map | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| MAP-02 | GET | `/me/knowledge-map/summary` | — | 학년별 숙련도 요약 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| MAP-03 | GET | `/me/concept-states` | — | Concept 숙련도 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| MAP-04 | GET | `/me/skill-states` | — | Skill 숙련도 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| MAP-05 | GET | `/me/skill-states/{code}/history` | — | Skill 숙련도 이력 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| MAP-06 | GET | `/me/weak-skills` | — | 취약 Skill | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| MAP-07 | GET | `/me/knowledge-map/history` | — | Knowledge Map 이력 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |

### ROAD — Learning Roadmap

| API ID | Method | 명세 Endpoint | 실제 Endpoint | 기능 | 의존성 | 구현 상태 | 테스트 | 연동 상태 | Issue/PR |
|---|---|---|---|---|---|---|---|---|---|
| ROAD-01 | GET | `/me/roadmap` | — | 현재 Roadmap | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| ROAD-02 | POST | `/me/roadmap/generate` | — | Roadmap 생성 요청 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| ROAD-03 | POST | `/me/roadmap/replan` | — | Roadmap 재계획 요청 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| ROAD-04 | GET | `/me/roadmap/steps/{id}` | — | 학습 단계 상세 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| ROAD-05 | GET | `/me/roadmap/progress` | — | 진행률 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| ROAD-06 | GET | `/me/roadmap/history` | — | 이전 Roadmap | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |

### LEARN — 문제·학습 세션·풀이 기록

| API ID | Method | 명세 Endpoint | 실제 Endpoint | 기능 | 의존성 | 구현 상태 | 테스트 | 연동 상태 | Issue/PR |
|---|---|---|---|---|---|---|---|---|---|
| LEARN-01 | POST | `/learning-sessions` | — | 세션 시작 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| LEARN-02 | GET | `/learning-sessions` | — | 세션 목록 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| LEARN-03 | GET | `/learning-sessions/{id}` | — | 세션 상세 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| LEARN-04 | PATCH | `/learning-sessions/{id}/finish` | — | 세션 종료 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| LEARN-05 | GET | `/problems` | — | 문제 목록 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| LEARN-06 | GET | `/problems/{id}` | — | 문제 상세 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| LEARN-07 | POST | `/problem-attempts` | — | 풀이 제출 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| LEARN-08 | GET | `/problem-attempts` | — | 풀이 목록 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| LEARN-09 | GET | `/problem-attempts/{id}` | — | 풀이 결과 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| LEARN-10 | GET | `/me/learning-history` | — | 학습 이력 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| LEARN-11 | GET | `/me/learning-summary` | — | 학습 요약 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| LEARN-12 | GET | `/me/wrong-answers` | — | 내 오답노트 목록 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| LEARN-13 | GET | `/me/review-queue` | — | 복습 대상 목록 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |

### OCR — AI① OCR·풀이 분석

| API ID | Method | 명세 Endpoint | 실제 Endpoint | 기능 | 의존성 | 구현 상태 | 테스트 | 연동 상태 | Issue/PR |
|---|---|---|---|---|---|---|---|---|---|
| OCR-01 | POST | `/captured-problems` | — | 이미지 업로드 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| OCR-02 | GET | `/captured-problems/{id}` | — | 촬영 정보 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| OCR-03 | POST | `/captured-problems/{id}/analyze` | — | AI① 분석 요청 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| OCR-04 | GET | `/ai-analyses/{id}` | — | 분석 결과 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| OCR-05 | GET | `/ai-analyses/{id}/steps` | — | 단계별 분석 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| OCR-06 | GET | `/ai-analyses/{id}/errors` | — | 최초 오류·오개념 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| OCR-07 | POST | `/ai-analyses/{id}/retry` | — | AI① 분석 재시도 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| OCR-08 | PATCH | `/ai-analyses/{id}/ocr` | — | OCR 인식 결과 보정 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| OCR-09 | GET | `/captured-problems` | — | 내 촬영 문제 목록 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |

### TUTOR — AI② Adaptive Tutor

| API ID | Method | 명세 Endpoint | 실제 Endpoint | 기능 | 의존성 | 구현 상태 | 테스트 | 연동 상태 | Issue/PR |
|---|---|---|---|---|---|---|---|---|---|
| TUTOR-01 | POST | `/tutor/feedback` | — | 학습 개입 요청 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| TUTOR-02 | GET | `/tutor/actions/{id}` | — | Tutor Action 조회 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| TUTOR-03 | POST | `/tutor/actions/{id}/responses` | — | 학습 개입 반응 제출 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| TUTOR-04 | GET | `/me/tutor-history` | — | 튜터 이력 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| TUTOR-05 | POST | `/tutor/variant-problems` | — | 변형문제 요청 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| TUTOR-06 | POST | `/tutor/variant-problems/{id}/attempts` | — | 변형문제 재도전 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |

### CONTENT — 개념학습·영상 추천

| API ID | Method | 명세 Endpoint | 실제 Endpoint | 기능 | 의존성 | 구현 상태 | 테스트 | 연동 상태 | Issue/PR |
|---|---|---|---|---|---|---|---|---|---|
| CONTENT-01 | GET | `/learning-contents` | — | 콘텐츠 목록 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| CONTENT-02 | GET | `/learning-contents/{id}` | — | 콘텐츠 상세 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| CONTENT-03 | GET | `/skills/{code}/contents` | — | Skill 콘텐츠 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| CONTENT-04 | GET | `/me/content-recommendations` | — | 맞춤 추천 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| CONTENT-05 | POST | `/content-learning-sessions` | — | 콘텐츠 학습 시작 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| CONTENT-06 | PATCH | `/content-learning-sessions/{id}` | — | 진행·완료 기록 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |

### GAME — 게이미피케이션

| API ID | Method | 명세 Endpoint | 실제 Endpoint | 기능 | 의존성 | 구현 상태 | 테스트 | 연동 상태 | Issue/PR |
|---|---|---|---|---|---|---|---|---|---|
| GAME-01 | GET | `/me/gamification` | — | XP·레벨·Streak | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| GAME-02 | GET | `/me/xp-history` | — | XP 이력 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| GAME-03 | GET | `/quests/daily` | — | Daily Quest | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| GAME-04 | GET | `/me/quests` | — | Quest 진행 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| GAME-05 | GET | `/badges` | — | 전체 배지 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| GAME-06 | GET | `/me/badges` | — | 획득 배지 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| GAME-07 | GET | `/me/achievements` | — | 누적 성취 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |

### FRIEND — 친구·경쟁

| API ID | Method | 명세 Endpoint | 실제 Endpoint | 기능 | 의존성 | 구현 상태 | 테스트 | 연동 상태 | Issue/PR |
|---|---|---|---|---|---|---|---|---|---|
| FRIEND-01 | GET | `/friends` | — | 친구 목록 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| FRIEND-02 | POST | `/friend-requests` | — | 친구 요청 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| FRIEND-03 | GET | `/friend-requests` | — | 요청 목록 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| FRIEND-04 | PATCH | `/friend-requests/{id}` | — | 수락·거절 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| FRIEND-05 | DELETE | `/friends/{id}` | — | 친구 삭제 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| FRIEND-06 | GET | `/friends/leaderboard` | — | 친구 성장 순위 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| FRIEND-07 | GET | `/me/competition-summary` | — | 친구 비교 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |

### WEB — 학부모·교사 WEB

| API ID | Method | 명세 Endpoint | 실제 Endpoint | 기능 | 의존성 | 구현 상태 | 테스트 | 연동 상태 | Issue/PR |
|---|---|---|---|---|---|---|---|---|---|
| WEB-01 | GET | `/dashboard/summary` | — | 대시보드 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| WEB-02 | GET | `/students` | — | 권한 학생 목록 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| WEB-03 | GET | `/students/{id}` | — | 학생 상세 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| WEB-04 | GET | `/students/{id}/knowledge-map` | — | 학생 Knowledge Map | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| WEB-05 | GET | `/students/{id}/weak-skills` | — | 취약 Skill | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| WEB-06 | GET | `/students/{id}/roadmap` | — | 학생 Roadmap | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| WEB-07 | GET | `/students/{id}/learning-history` | — | 학습 이력 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| WEB-08 | GET | `/students/{id}/ai-analyses` | — | AI① 이력 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| WEB-09 | GET | `/students/{id}/tutor-history` | — | AI② 이력 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| WEB-10 | GET | `/students/{id}/gamification` | — | 학습 지속 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| WEB-11 | GET | `/students/{id}/relative-standing` | — | 서비스 내 상대 위치 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| WEB-12 | GET | `/students/{id}/reports` | — | 리포트 목록 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| WEB-13 | GET | `/students/{id}/reports/{reportId}` | — | 리포트 상세 | CONTRACT_REQUIRED | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |

### ADMIN — 관리자·기준 데이터

| API ID | Method | 명세 Endpoint | 실제 Endpoint | 기능 | 의존성 | 구현 상태 | 테스트 | 연동 상태 | Issue/PR |
|---|---|---|---|---|---|---|---|---|---|
| ADMIN-01 | POST | `/admin/concepts` | — | Concept 등록 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| ADMIN-02 | PATCH | `/admin/concepts/{code}` | — | Concept 수정 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| ADMIN-03 | POST | `/admin/skills` | — | Skill 등록 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| ADMIN-04 | PATCH | `/admin/skills/{code}` | — | Skill 수정 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| ADMIN-05 | POST | `/admin/skill-prerequisites` | — | 선수관계 등록 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| ADMIN-06 | POST | `/admin/problems` | — | 문제 등록 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| ADMIN-07 | PATCH | `/admin/problems/{id}` | — | 문제 수정 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| ADMIN-08 | POST | `/admin/learning-contents` | — | 콘텐츠 등록 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |
| ADMIN-09 | PATCH | `/admin/learning-contents/{id}` | — | 콘텐츠 수정 | BE_ONLY | NOT_STARTED | NOT_RUN | NOT_REQUIRED | — |

### INTERNAL — AI①·AI② 내부 서비스 API

| API ID | Method | 명세 Endpoint | 실제 Endpoint | 기능 | 의존성 | 구현 상태 | 테스트 | 연동 상태 | Issue/PR |
|---|---|---|---|---|---|---|---|---|---|
| INTERNAL-01 | POST | `/api/analysis` | — | BE→AI① 풀이 분석 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| INTERNAL-02 | POST | `/api/tutor/decision` | — | BE→AI② Tutor Action | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| INTERNAL-03 | POST | `/api/diagnostic/next` | — | BE→AI② 다음 진단 Skill | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| INTERNAL-04 | POST | `/api/diagnostic/evaluate` | — | BE→AI② 숙련도 추정 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| INTERNAL-05 | POST | `/api/roadmap/generate` | — | BE→AI② Roadmap 생성 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| INTERNAL-06 | POST | `/api/roadmap/replan` | — | BE→AI② 재계획 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| INTERNAL-07 | POST | `/api/tutor/content` | — | BE→AI② 설명·힌트 생성 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| INTERNAL-08 | POST | `/api/tutor/variant` | — | BE→AI② 변형문제 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
| INTERNAL-09 | POST | `/api/content/recommend` | — | BE→AI② 콘텐츠 추천 | AI_INTEGRATION | NOT_STARTED | NOT_RUN | CONTRACT_PENDING | — |
