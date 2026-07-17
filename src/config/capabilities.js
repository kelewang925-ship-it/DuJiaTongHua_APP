const realCapabilities = {
  auth: true, couple: true, diary: true, photo: true, anniversary: true,
  tags: true, timeCapsules: true, comments: true, notifications: true,
  systemShare: true,
  aiGeneration: false, membershipPayment: false, pdfExport: false,
  cloudBackup: false, shareCardPersistence: false,
  voiceAttachment: false, locationAttachment: false,
  feedbackSubmission: false, feedbackAttachment: false,
};

const mockCapabilities = Object.keys(realCapabilities).reduce((result, key) => ({ ...result, [key]: true }), {});

export function getCapabilities(mode = process.env.EXPO_PUBLIC_API_MODE || 'mock') {
  return mode === 'real' ? realCapabilities : mockCapabilities;
}

export function hasCapability(name, mode) {
  return Boolean(getCapabilities(mode)[name]);
}
