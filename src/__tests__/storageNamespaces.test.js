import { getStorageKey } from '../config/storageNamespaces';

test('mock and real users never share persistence namespaces', () => {
  expect(getStorageKey('mock')).not.toBe(getStorageKey('real', 'user-a'));
  expect(getStorageKey('real', 'user-a')).not.toBe(getStorageKey('real', 'user-b'));
});
