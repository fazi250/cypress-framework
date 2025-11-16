// ============================================
// FILE: cypress/support/commands.ts
// ============================================

declare global {
  namespace Cypress {
    interface Chainable {
      extractMainDOM(filename?: string): Chainable<void>;
    }
  }
}

// -----------------------------
// 🔹 Helper 1: Get main element
// -----------------------------
function getMainElement(win: Window): Element | null {
  const main = win.document.querySelector('#main-content');
  if (!main) cy.log('⚠️ Main element not found in DOM');
  return main;
}

// -----------------------------
// 🔹 Helper 2: Remove <style> and <script> tags
// -----------------------------
function removeUnwantedElements(element: Element): void {
  // Remove all <style> and <script> tags inside the given element
  const selectors = ['style', 'script'];
  selectors.forEach((tag) => {
    const nodes = element.querySelectorAll(tag);
    nodes.forEach((n) => n.remove());
  });
}

// -----------------------------
// 🔹 Helper 3: Get element attributes
// -----------------------------
function getElementAttributes(element: Element): string {
  return Array.from(element.attributes)
    .map((attr: Attr) => `${attr.name}="${attr.value}"`)
    .join(' ');
}

// -----------------------------
// 🔹 Helper 4: Check if void element
// -----------------------------
function isVoidElement(tagName: string): boolean {
  const voidTags = [
    'area', 'base', 'br', 'col', 'embed', 'hr',
    'img', 'input', 'link', 'meta', 'param',
    'source', 'track', 'wbr'
  ];
  return voidTags.includes(tagName);
}

// -----------------------------
// 🔹 Helper 5: Recursively extract formatted DOM
// -----------------------------
function extractFullDOM(element: Element, depth: number = 0): string {
  const indent = '  '.repeat(depth);
  const tagName = element.tagName.toLowerCase();
  const attributes = getElementAttributes(element);

  if (isVoidElement(tagName)) {
    return `${indent}<${tagName}${attributes ? ' ' + attributes : ''} />\n`;
  }

  let html = `${indent}<${tagName}${attributes ? ' ' + attributes : ''}>\n`;

  // Handle Shadow DOM
  const shadowRoot = (element as any).shadowRoot as ShadowRoot | null;
  if (shadowRoot) {
    html += `${indent}  <!-- Shadow DOM Start -->\n`;
    Array.from(shadowRoot.children).forEach((child: Element) => {
      html += extractFullDOM(child, depth + 1);
    });
    html += `${indent}  <!-- Shadow DOM End -->\n`;
  }

  // Handle children
  element.childNodes.forEach((node: ChildNode) => {
    if (node.nodeType === Node.ELEMENT_NODE) {
      html += extractFullDOM(node as Element, depth + 1);
    } else if (node.nodeType === Node.TEXT_NODE) {
      const text = node.textContent?.trim();
      if (text) html += `${indent}  ${text}\n`;
    }
  });

  html += `${indent}</${tagName}>\n`;
  return html;
}

// -----------------------------
// 🔹 Helper 6: Save HTML to browser as file
// -----------------------------
function saveHTMLToFile(win: Window, html: string, filename: string): void {
  const blob = new Blob([html], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const link = win.document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

// -----------------------------
// 🔹 Main Cypress Command
// -----------------------------
Cypress.Commands.add('extractMainDOM', (filename: string = 'main-dom.html'): void => {
  cy.window().then((win: Window) => {
    const mainElement = getMainElement(win);
    if (!mainElement) return;

    // 🧹 Remove unwanted <style> and <script> tags before extraction
    removeUnwantedElements(mainElement);

    const formattedHTML = extractFullDOM(mainElement);
    saveHTMLToFile(win, formattedHTML, filename);

    cy.log(`✅ DOM extracted (without styles/scripts) and saved as ${filename}`);
    cy.task('log', formattedHTML, { log: false });
  });
});

export {};
