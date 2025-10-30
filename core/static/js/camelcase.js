(function () {
  'use strict';

  function toWords(s) {
    return s
      .toString()
      .trim()
      .split(/[^\p{L}\p{N}]+/u) // split on any non-letter/number (unicode-aware)
      .filter(Boolean);
  }

  function capitalize(word) {
    if (!word) return '';
    return word[0].toLocaleUpperCase('pt-BR') + word.slice(1).toLocaleLowerCase('pt-BR');
  }

  function toPascalCase(s) {
    return toWords(s).map(capitalize).join('');
  }

  function toLowerCamelCase(s) {
    const words = toWords(s);
    if (!words.length) return '';
    const first = words[0].toLocaleLowerCase('pt-BR');
    const rest = words.slice(1).map(capitalize).join('');
    return first + rest;
  }

  // Title case (preserve spaces): "joão da silva" -> "João Da Silva"
  function toTitleCase(s) {
    return toWords(s).map(capitalize).join(' ');
  }

  function applyToElement(el) {
    const mode = el.getAttribute('data-camel') || 'upper'; // 'upper' = Title Case (preserve spaces), 'pascal' = PascalCase (no spaces), 'lower' = lowerCamel
    const text = (el.textContent || '').trim();
    if (!text) return;
    let converted;
    if (mode === 'lower') converted = toLowerCamelCase(text);
    else if (mode === 'pascal') converted = toPascalCase(text);
    else converted = toTitleCase(text);
    el.textContent = converted;
  }

  function run() {
    document.querySelectorAll('.camel-case').forEach(applyToElement);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }

  // expose for dynamic use
  window.applyCamelCase = run;
})();
