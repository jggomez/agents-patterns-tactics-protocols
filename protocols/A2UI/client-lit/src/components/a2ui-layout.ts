import { LitElement, html, css } from 'lit';
import { customElement } from 'lit/decorators.js';

@customElement('a2ui-column')
export class A2UIColumn extends LitElement {
  static styles = css`
    :host {
      display: flex;
      flex-direction: column;
      gap: 12px;
      width: 100%;
    }
  `;
  render() { return html`<slot></slot>`; }
}

@customElement('a2ui-row')
export class A2UIRow extends LitElement {
  static styles = css`
    :host {
      display: flex;
      flex-direction: row;
      gap: 12px;
      align-items: center;
      width: 100%;
    }
  `;
  render() { return html`<slot></slot>`; }
}
