import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import './a2ui-text';
import './a2ui-button';
import './a2ui-layout';

@customElement('a2ui-surface')
export class A2UISurface extends LitElement {
  @property({ type: Array }) components: any[] = [];
  @property({ type: String }) rootId = 'root';

  static styles = css`
    :host {
      display: block;
      background: rgba(30, 41, 59, 0.5);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 16px;
      padding: 20px;
      margin-top: 16px;
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
  `;

  render() {
    const compMap = new Map(this.components.map(c => [c.id, c]));
    const root = compMap.get(this.rootId);
    
    if (!root) {
      return html`<div style="color: #ef4444">⚠️ Root component '${this.rootId}' not found</div>`;
    }

    return this._renderComponent(root, compMap);
  }

  private _renderComponent(comp: any, compMap: Map<string, any>): any {
    const type = comp.component;
    const props = comp.props || {};
    const childrenIds = comp.children || [];
    
    const children = childrenIds.map((id: string) => {
      const child = compMap.get(id);
      return child ? this._renderComponent(child, compMap) : html`<span style="color:red">Missing ${id}</span>`;
    });

    switch (type) {
      case 'Column':
        return html`<a2ui-column>${children}</a2ui-column>`;
      case 'Row':
        return html`<a2ui-row>${children}</a2ui-row>`;
      case 'Text':
        return html`<a2ui-text .text=${props.text} .usageHint=${props.usageHint}></a2ui-text>`;
      case 'Button':
        return html`<a2ui-button .label=${props.label} .action=${props.action}></a2ui-button>`;
      default:
        return html`<div>Unknown component type: ${type}</div>`;
    }
  }
}
