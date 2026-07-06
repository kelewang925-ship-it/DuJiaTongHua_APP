import { useCallback, useEffect, useState } from 'react';
import { StyleSheet, View } from 'react-native';
import FairyToast from './FairyToast';

let messageHandler = null;
const pendingMessages = [];

function showMessage(tone, content, options = {}) {
  const payload = {
    id: Date.now() + Math.random(),
    tone,
    content,
    duration: options.duration,
  };

  if (messageHandler) {
    messageHandler(payload);
    return;
  }

  pendingMessages.push(payload);
}

export const message = {
  success: (content, options) => showMessage('success', content, options),
  info: (content, options) => showMessage('info', content, options),
  error: (content, options) => showMessage('error', content, options),
};

export function FairyMessageProvider({ children }) {
  const [current, setCurrent] = useState(null);

  const open = useCallback((payload) => {
    setCurrent(payload);
  }, []);

  useEffect(() => {
    messageHandler = open;

    if (pendingMessages.length) {
      setCurrent(pendingMessages[pendingMessages.length - 1]);
      pendingMessages.length = 0;
    }

    return () => {
      if (messageHandler === open) {
        messageHandler = null;
      }
    };
  }, [open]);

  return (
    <View style={styles.host}>
      {children}
      <FairyToast
        key={current?.id}
        visible={Boolean(current)}
        tone={current?.tone}
        message={current?.content}
        duration={current?.duration}
        onHide={() => setCurrent(null)}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  host: {
    flex: 1,
  },
});
