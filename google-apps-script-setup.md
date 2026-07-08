# POB 성경클럽 문의 접수 연결

목표: 상세페이지 문의 내용을 Google Sheets에 기록하고, `fastkorea12@gmail.com`으로 알림 메일을 보냅니다.

## 준비된 응답 시트

https://docs.google.com/spreadsheets/d/1rpTKvItlYJyqRO48h4qC8aVG4IyyIiRQt1db3COS-7Q/edit

## Apps Script 설정

1. https://script.google.com/ 접속
2. 새 프로젝트 만들기
3. 기본 `Code.gs` 내용을 지우고 `google-apps-script.gs` 내용을 붙여넣기
4. 저장
5. `배포` → `새 배포`
6. 유형 선택: `웹 앱`
7. 실행 사용자: `나`
8. 액세스 권한: `모든 사용자`
9. 배포 후 나오는 웹 앱 URL을 복사
10. `detail.html`의 `INQUIRY_ENDPOINT` 값에 웹 앱 URL 붙여넣기

## 알림 동작

문의가 접수되면:

- Google Sheets에 한 줄로 저장됩니다.
- `fastkorea12@gmail.com`으로 알림 메일이 발송됩니다.
- 문의자는 페이지에서 접수 완료 메시지를 봅니다.
