import { LitElement, html, css } from 'lit';
import { customElement, property } from 'lit/decorators.js';

@customElement('a2ui-text')
export class A2UIText extends LitElement {
  @property({ type: String }) text = '';
  @property({ type: String }) usageHint = 'body';

  static styles = css`
    :host { display: block; margin-bottom: 8px; }
    .h1 { font-family: 'Outfit', sans-serif; font-size: 24px; font-weight: 700; color: #60a5fa; }
    .h2 { font-family: 'Outfit', sans-serif; font-size: 20px; font-weight: 600; color: #93c5fd; }
    .body { font-size: 16px; line-height: 1.5; color: #e2e8f0; }
    .caption { font-size: 14px; color: #94a3b8; font-style: italic; }
  `;

  render() {
    return html`<div class="${this.usageHint}">${this.text}</div>`;
  }
}
