const SPREADSHEET_ID = '1rpTKvItlYJyqRO48h4qC8aVG4IyyIiRQt1db3COS-7Q';
const SHEET_NAME = 'Sheet1';
const NOTIFY_EMAIL = 'fastkorea12@gmail.com';

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents || '{}');
    const submittedAt = new Date();

    const row = [
      submittedAt,
      data.name || '',
      data.phone || '',
      data.group || '',
      data.interest || '',
      data.message || '',
      data.page || '',
    ];

    SpreadsheetApp.openById(SPREADSHEET_ID)
      .getSheetByName(SHEET_NAME)
      .appendRow(row);

    const subject = '[POB 성경클럽] 새 문의가 접수되었습니다';
    const body = [
      'POB 성경클럽 상세페이지에서 새 문의가 접수되었습니다.',
      '',
      `이름: ${data.name || '-'}`,
      `연락처: ${data.phone || '-'}`,
      `교회명 또는 가정: ${data.group || '-'}`,
      `관심 프로그램: ${data.interest || '-'}`,
      '',
      '문의 내용:',
      data.message || '-',
      '',
      `유입 페이지: ${data.page || '-'}`,
      `접수 시간: ${submittedAt}`,
    ].join('\n');

    MailApp.sendEmail(NOTIFY_EMAIL, subject, body);

    return jsonResponse({ ok: true });
  } catch (error) {
    return jsonResponse({ ok: false, error: String(error) });
  }
}

function jsonResponse(payload) {
  return ContentService
    .createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON);
}
