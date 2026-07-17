import fs from 'node:fs';
import path from 'node:path';

const pagePath = path.join(process.cwd(), 'app/help-feedback.js');
const source = fs.readFileSync(pagePath, 'utf8');

describe('help feedback real-data guards', () => {
  test('does not fabricate ticket ids or submitted receipts', () => {
    expect(source).not.toContain('Date.now()');
    expect(source).not.toContain('TH-${');
    expect(source).not.toContain('setSubmitted');
    expect(source).not.toContain('已收件');
    expect(source).not.toContain('受理编号');
  });

  test('does not clear draft fields after local validation', () => {
    expect(source).not.toContain("setContent('');");
    expect(source).not.toContain("setContact('');");
    expect(source).toContain('输入将继续保留');
  });

  test('states that feedback and attachments are not sent', () => {
    expect(source).toContain('当前内容不会发送，也不会生成模拟工单');
    expect(source).toContain('当前不会选择或上传文件');
    expect(source).toContain('正式反馈 API 接入前不会生成工单或受理编号');
  });

  test('uses capability-aware controls', () => {
    expect(source).toContain("hasCapability('feedbackSubmission', mode)");
    expect(source).toContain("hasCapability('feedbackAttachment', mode)");
    expect(source).toContain("canSubmitFeedback ? '检查反馈草稿' : '反馈提交未开放'");
  });
});
