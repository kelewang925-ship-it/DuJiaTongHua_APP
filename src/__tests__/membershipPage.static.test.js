import fs from 'node:fs';
import path from 'node:path';

const source = fs.readFileSync(path.resolve(process.cwd(), 'app/membership.js'), 'utf8');

describe('membership page payment guards', () => {
  test('does not fabricate a locally activated membership plan', () => {
    expect(source).not.toContain('activatedPlan');
    expect(source).not.toContain('体验权益已在本地开启');
    expect(source).not.toContain('已开启`');
  });

  test('keeps membership state dependent on payment capability', () => {
    expect(source).toContain("hasCapability('membershipPayment')");
    expect(source).toContain("disabled={!paymentAvailable}");
    expect(source).toContain('会员支付暂未开放');
  });

  test('requires explicit agreement instead of preselecting consent', () => {
    expect(source).toContain('const [agreed, setAgreed] = useState(false)');
  });

  test('does not claim that confirmation creates an order', () => {
    expect(source).toContain('尚未接入支付与会员状态同步');
    expect(source).toContain('不会创建订单或变更会员状态');
  });
});
