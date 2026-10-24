# 공식 119개 외 운영용 Endpoint

공식 v0.3 API 후보에 포함되지 않은 현재 운영 Endpoint는 감사 스크립트 실행 결과로 확인해 갱신합니다.

| Method | Endpoint | 용도 |
|---|---|---|
| GET | `/` | 서비스 루트 |
| GET | `/health` | 애플리케이션 상태 점검 |
| GET | `/health/db` | DB 연결 상태 점검 |
| GET | `/auth/status` | 인증 기반 상태 |
