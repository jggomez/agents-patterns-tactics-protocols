import { LitElement, html, css } from 'lit';
import { customElement } from 'lit/decorators.js';

@customElement('a2ui-card')
export class A2UICard extends LitElement {
  static styles = css`
    :host {
      display: block;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(148, 163, 184, 0.2);
      border-radius: 12px;
      padding: 16px;
      margin: 8px 0;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -2px rgba(0, 0, 0, 0.2);
      transition: border-color 0.2s ease;
    }
    :host(:hover) {
      border-color: rgba(96, 165, 250, 0.4);
    }
  `;

  render() {
    return html`<slot></slot>`;
  }
}
