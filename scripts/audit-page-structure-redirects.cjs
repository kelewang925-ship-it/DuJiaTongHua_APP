function expoRedirectLocalNames(source) {
  const names = new Set();
  const importPattern = /import\s*\{([\s\S]*?)\}\s*from\s*['"]expo-router['"]\s*;?/g;
  let match;

  while ((match = importPattern.exec(source))) {
    for (const specifier of match[1].split(',')) {
      const normalized = specifier.trim();
      const redirect = normalized.match(/^Redirect(?:\s+as\s+([A-Za-z_$][\w$]*))?$/);
      if (redirect) names.add(redirect[1] || 'Redirect');
    }
  }

  return names;
}

function isImperativeRedirectOnly(source) {
  const hasRouterRedirect = /\brouter\s*\.\s*(?:replace|push)\s*\(/.test(source);
  const returnsNull = /\breturn\s+null\s*;?/.test(source);
  const rendersPage = /<FairyPage\b/.test(source);
  const rendersJsx = /\breturn\s*\(\s*</.test(source);
  return hasRouterRedirect && returnsNull && !rendersPage && !rendersJsx;
}

function isDeclarativeRedirectOnly(source) {
  const localNames = expoRedirectLocalNames(source);
  if (!localNames.size || /<FairyPage\b/.test(source)) return false;

  const renderedComponents = [...source.matchAll(/<([A-Z][A-Za-z0-9_.$]*)\b/g)].map((match) => match[1]);
  if (renderedComponents.length !== 1) return false;

  const redirectName = renderedComponents[0];
  if (!localNames.has(redirectName)) return false;

  const escapedName = redirectName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const returnPattern = new RegExp(
    `\\breturn\\s*\\(?\\s*<${escapedName}\\b(?=[^>]*\\bhref\\s*=)[^>]*\\/\\s*>\\s*\\)?\\s*;?`
  );
  return returnPattern.test(source);
}

function isRedirectOnly(source) {
  return isImperativeRedirectOnly(source) || isDeclarativeRedirectOnly(source);
}

module.exports = {
  expoRedirectLocalNames,
  isDeclarativeRedirectOnly,
  isImperativeRedirectOnly,
  isRedirectOnly,
};
