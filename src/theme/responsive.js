export const BREAKPOINTS = {
  compact: 390,
  standard: 768,
};

export const responsiveModes = {
  compact: {
    pagePadding: 16,
    maxContentWidth: 640,
    columns: 1,
  },
  standard: {
    pagePadding: 20,
    maxContentWidth: 760,
    columns: 1,
  },
  wide: {
    pagePadding: 24,
    maxContentWidth: 960,
    columns: 2,
  },
};

export function getResponsiveMode(width) {
  if (width <= BREAKPOINTS.compact) return 'compact';
  if (width <= BREAKPOINTS.standard) return 'standard';
  return 'wide';
}

export function getResponsiveMetrics(width) {
  return responsiveModes[getResponsiveMode(width)];
}

export default {
  BREAKPOINTS,
  responsiveModes,
  getResponsiveMode,
  getResponsiveMetrics,
};
