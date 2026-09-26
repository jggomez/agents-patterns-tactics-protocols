import { LitElement, html, css } from 'lit';
import { customElement, property } from 'lit/decorators.js';

@customElement('a2ui-text')
export class A2UIText extends LitElement {
  @property({ type: String }) text = '';
  @property({ type: String }) variant = 'body';
  @property({ type: String }) usageHint = '';

  static styles = css`
    :host { display: block; margin-bottom: 8px; }
    .h1 { font-family: 'Outfit', sans-serif; font-size: 24px; font-weight: 700; color: #60a5fa; margin: 0 0 8px 0; }
    .h2 { font-family: 'Outfit', sans-serif; font-size: 20px; font-weight: 600; color: #93c5fd; margin: 0 0 6px 0; }
    .h3 { font-family: 'Outfit', sans-serif; font-size: 18px; font-weight: 600; color: #bfdbfe; margin: 0 0 4px 0; }
    .body { font-size: 15px; line-height: 1.5; color: #e2e8f0; }
    .caption { font-size: 13px; color: #94a3b8; font-style: italic; }
  `;

  render() {
    const styleClass = this.variant || this.usageHint || 'body';
    return html`<div class="${styleClass}">${this.text}</div>`;
  }
}
