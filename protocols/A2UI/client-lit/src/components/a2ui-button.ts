import { LitElement, html, css } from 'lit';
import { customElement, property } from 'lit/decorators.js';

@customElement('a2ui-button')
export class A2UIButton extends LitElement {
  @property({ type: String }) label = '';
  @property({ type: Object }) action: any = '';
  @property({ type: String }) variant = 'default';

  static styles = css`
    :host { display: inline-block; }
    button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 10px 20px;
      border-radius: 8px;
      font-family: inherit;
      font-weight: 600;
      font-size: 14px;
      cursor: pointer;
      transition: all 0.2s ease;
      border: 1px solid transparent;
    }
    button.primary {
      background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
      color: white;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    button.primary:hover {
      transform: translateY(-1px);
      box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
      filter: brightness(1.1);
    }
    button.default {
      background: #334155;
      color: #f1f5f9;
      border: 1px solid #475569;
    }
    button.default:hover {
      background: #475569;
      color: white;
    }
    button.borderless {
      background: transparent;
      color: #60a5fa;
      padding: 6px 12px;
    }
    button.borderless:hover {
      background: rgba(96, 165, 250, 0.1);
    }
    button:active {
      transform: translateY(0);
    }
  `;

  private _handleClick() {
    const actionPayload = typeof this.action === 'object' && this.action !== null
      ? this.action.name || this.action.action || JSON.stringify(this.action)
      : this.action;

    this.dispatchEvent(new CustomEvent('a2ui-action', {
      detail: { action: actionPayload },
      bubbles: true,
      composed: true
    }));
  }

  render() {
    const variantClass = this.variant || 'default';
    return html`
      <button class="${variantClass}" @click=${this._handleClick}>
        <slot>${this.label}</slot>
      </button>
    `;
  }
}
