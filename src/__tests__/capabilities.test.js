import { getCapabilities } from '../config/capabilities';

test('real mode refuses unfinished service capabilities', () => {
  const real = getCapabilities('real');
  expect(real.diary).toBe(true);
  expect(real.aiGeneration).toBe(false);
  expect(real.membershipPayment).toBe(false);
  expect(real.pdfExport).toBe(false);
  expect(real.cloudBackup).toBe(false);
});

test('mock mode keeps visual-demo capabilities', () => {
  expect(Object.values(getCapabilities('mock')).every(Boolean)).toBe(true);
});
