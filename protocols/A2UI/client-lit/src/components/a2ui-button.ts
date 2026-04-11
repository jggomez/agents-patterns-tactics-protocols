import { LitElement, html, css } from 'lit';
import { customElement, property } from 'lit/decorators.js';

@customElement('a2ui-button')
export class A2UIButton extends LitElement {
  @property({ type: String }) label = '';
  @property({ type: String }) action = '';

  static styles = css`
    button {
      background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 8px;
      font-family: inherit;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    button:hover {
      transform: translateY(-1px);
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
      filter: brightness(1.1);
    }
    button:active {
      transform: translateY(0);
    }
  `;

  private _handleClick() {
    this.dispatchEvent(new CustomEvent('a2ui-action', {
      detail: { action: this.action },
      bubbles: true,
      composed: true
    }));
  }

  render() {
    return html`<button @click=${this._handleClick}>${this.label}</button>`;
  }
}
