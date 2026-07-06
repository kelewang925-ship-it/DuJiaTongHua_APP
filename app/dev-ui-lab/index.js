import { Redirect } from 'expo-router';
import DevHome from '../../src/dev-ui-lab/pages/DevHome';
import { enableDevUI } from '../../src/dev-ui-lab/runtime/env';

export default function DevUILabRoute() {
  if (!enableDevUI) {
    return <Redirect href="/" />;
  }

  return <DevHome />;
}
