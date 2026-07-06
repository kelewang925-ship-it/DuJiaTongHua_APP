import { Redirect } from 'expo-router';
import MockCenter from '../../src/dev-ui-lab/pages/MockCenter';
import { enableDevUI } from '../../src/dev-ui-lab/runtime/env';

export default function MockCenterRoute() {
  if (!enableDevUI) {
    return <Redirect href="/" />;
  }

  return <MockCenter />;
}
