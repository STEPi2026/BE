# Backend 단독 개발 로드맵

API ID와 상세 상태의 단일 기준은 [API_MASTER.md](API_MASTER.md)입니다.

## 현재 완료 근거

- 인증 기반: `bba2469`, PR #4 merge
- 회원가입: `48deb43`, PR #5 merge commit `e7e1bc3` — `POST /auth/signup` 검증 완료

## 1 인증·계정

- 관련 공식 API: AUTH-01~AUTH-13
- 선행 조건: JWT 인증·권한 정책, 관련 DB 모델과 Schema 확인
- 완료 기준: Router 등록, 정상·오류·권한 테스트, OpenAPI 확인
- 권장 Issue: 기능 단위로 분리

## 2 사용자·프로필

- 관련 공식 API: AUTH-05~AUTH-08
- 선행 조건: JWT 인증·권한 정책, 관련 DB 모델과 Schema 확인
- 완료 기준: Router 등록, 정상·오류·권한 테스트, OpenAPI 확인
- 권장 Issue: 기능 단위로 분리

## 3 교육과정·기준정보

- 관련 공식 API: CUR-01~CUR-08
- 선행 조건: JWT 인증·권한 정책, 관련 DB 모델과 Schema 확인
- 완료 기준: Router 등록, 정상·오류·권한 테스트, OpenAPI 확인
- 권장 Issue: 기능 단위로 분리

## 4 문제 관리

- 관련 공식 API: LEARN-05~LEARN-06
- 선행 조건: JWT 인증·권한 정책, 관련 DB 모델과 Schema 확인
- 완료 기준: Router 등록, 정상·오류·권한 테스트, OpenAPI 확인
- 권장 Issue: 기능 단위로 분리

## 5 학습 세션

- 관련 공식 API: LEARN-01~LEARN-04
- 선행 조건: JWT 인증·권한 정책, 관련 DB 모델과 Schema 확인
- 완료 기준: Router 등록, 정상·오류·권한 테스트, OpenAPI 확인
- 권장 Issue: 기능 단위로 분리

## 6 풀이 기록

- 관련 공식 API: LEARN-07~LEARN-13
- 선행 조건: JWT 인증·권한 정책, 관련 DB 모델과 Schema 확인
- 완료 기준: Router 등록, 정상·오류·권한 테스트, OpenAPI 확인
- 권장 Issue: 기능 단위로 분리

## 7 기본 학습 상태

- 관련 공식 API: MAP-03~MAP-06
- 선행 조건: JWT 인증·권한 정책, 관련 DB 모델과 Schema 확인
- 완료 기준: Router 등록, 정상·오류·권한 테스트, OpenAPI 확인
- 권장 Issue: 기능 단위로 분리

## 8 기본 게임화

- 관련 공식 API: GAME-01~GAME-07
- 선행 조건: JWT 인증·권한 정책, 관련 DB 모델과 Schema 확인
- 완료 기준: Router 등록, 정상·오류·권한 테스트, OpenAPI 확인
- 권장 Issue: 기능 단위로 분리

## 8단계 이후

- BE_ONLY로 분류된 콘텐츠 조회와 관리자 기준 데이터 API를 별도 Issue로 분리합니다.
- CONTRACT_REQUIRED와 AI_INTEGRATION 항목은 계약 확정 전 실제 통합 완료로 표시하지 않습니다.
