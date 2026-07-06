import { Redirect } from 'expo-router';
import ComponentLab from '../../src/dev-ui-lab/pages/ComponentLab';
import { enableDevUI } from '../../src/dev-ui-lab/runtime/env';

export default function ComponentLabRoute() {
  if (!enableDevUI) {
    return <Redirect href="/" />;
  }

  return <ComponentLab />;
}
