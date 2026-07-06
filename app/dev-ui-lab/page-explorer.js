import { Redirect } from 'expo-router';
import PageExplorer from '../../src/dev-ui-lab/pages/PageExplorer';
import { enableDevUI } from '../../src/dev-ui-lab/runtime/env';

export default function PageExplorerRoute() {
  if (!enableDevUI) {
    return <Redirect href="/" />;
  }

  return <PageExplorer />;
}
