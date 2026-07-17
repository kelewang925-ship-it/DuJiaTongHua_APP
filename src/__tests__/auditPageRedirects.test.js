import fs from 'node:fs';
import path from 'node:path';

const { isRedirectOnly } = require('../../scripts/audit-page-structure-redirects.cjs');
const root = path.resolve(__dirname, '../..');
const read = (relativePath) => fs.readFileSync(path.join(root, relativePath), 'utf8');

describe('page structure redirect-only classification', () => {
  test.each([
    'app/ai/generation-progress.js',
    'app/album/index.js',
    'app/index.js',
    'app/interaction/comments.js',
  ])('recognizes Expo Router Redirect route %s', (relativePath) => {
    expect(isRedirectOnly(read(relativePath))).toBe(true);
  });

  test('recognizes imperative router redirect routes', () => {
    expect(isRedirectOnly(`
      import { useEffect } from 'react';
      import { router } from 'expo-router';
      export default function AliasRoute() {
        useEffect(() => { router.replace('/target'); }, []);
        return null;
      }
    `)).toBe(true);
  });

  test('does not exclude a visible page merely because Redirect is imported', () => {
    expect(isRedirectOnly(`
      import { Redirect } from 'expo-router';
      import FairyPage from '../src/components/FairyPage';
      export default function VisiblePage() {
        return <FairyPage><Text>Visible</Text></FairyPage>;
      }
    `)).toBe(false);
  });

  test('does not exclude a route that renders Redirect with other visible UI', () => {
    expect(isRedirectOnly(`
      import { Redirect } from 'expo-router';
      export default function ConditionalPage({ ready }) {
        if (ready) return <Redirect href="/target" />;
        return <LoadingCard />;
      }
    `)).toBe(false);
  });

  test('supports an aliased Expo Router Redirect import', () => {
    expect(isRedirectOnly(`
      import { Redirect as ExpoRedirect } from 'expo-router';
      export default function AliasRoute() {
        return <ExpoRedirect href="/target" />;
      }
    `)).toBe(true);
  });
});
