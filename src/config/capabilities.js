const realCapabilities = Object.freeze({
  auth: true, couple: true, diary: true, photo: true, anniversary: true,
  tags: true, timeCapsules: true, comments: true, notifications: true,
  systemShare: true,
  aiGeneration: false, membershipPayment: false, pdfExport: false,
  cloudBackup: false, shareCardPersistence: false,
  voiceAttachment: false, locationAttachment: false,
  feedbackSubmission: false, feedbackAttachment: false,
});

const mockCapabilities = Object.freeze(Object.keys(realCapabilities).reduce((result, key) => ({ ...result, [key]: true }), {}));
const disabledCapabilities = Object.freeze(Object.keys(realCapabilities).reduce((result, key) => ({ ...result, [key]: false }), {}));

export function normalizeCapabilityMode(mode = process.env.EXPO_PUBLIC_API_MODE || 'mock') {
  const value = String(mode || '').trim().toLowerCase();
  return value === 'real' || value === 'mock' ? value : 'disabled';
}

export function getCapabilities(mode) {
  const normalizedMode = normalizeCapabilityMode(mode);
  if (normalizedMode === 'real') return realCapabilities;
  if (normalizedMode === 'mock') return mockCapabilities;
  return disabledCapabilities;
}

export function hasCapability(name, mode) {
  return Boolean(getCapabilities(mode)[name]);
}
