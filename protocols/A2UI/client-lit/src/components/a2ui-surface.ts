import { LitElement, html, css } from 'lit';
import { customElement, property } from 'lit/decorators.js';
import './a2ui-text';
import './a2ui-button';
import './a2ui-card';
import './a2ui-layout';

@customElement('a2ui-surface')
export class A2UISurface extends LitElement {
  @property({ type: Array }) components: any[] = [];
  @property({ type: Object }) surface: any = null;
  @property({ type: Object }) dataModel: Record<string, any> = {};
  @property({ type: String }) rootId = 'root';

  static styles = css`
    :host {
      display: block;
      background: rgba(30, 41, 59, 0.5);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 16px;
      padding: 20px;
      margin-top: 16px;
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
    }
  `;

  render() {
    let compList = this.components;
    
    // If official v0.9 surface model is provided, extract its components
    if (this.surface && this.surface.componentsModel) {
      const surfaceComponents: any[] = [];
      for (const [id, node] of this.surface.componentsModel.entries()) {
        surfaceComponents.push({ id, ...node.component });
      }
      if (surfaceComponents.length > 0) {
        compList = surfaceComponents;
      }
    }

    if (!compList || compList.length === 0) {
      return html`<div style="color: #94a3b8; font-style: italic;">Loading A2UI surface...</div>`;
    }

    const compMap = new Map(compList.map(c => [c.id, c]));
    const root = compMap.get(this.rootId);
    
    if (!root) {
      return html`<div style="color: #ef4444">⚠️ Root component '${this.rootId}' not found in A2UI surface</div>`;
    }

    return this._renderComponent(root, compMap);
  }

  private _renderComponent(comp: any, compMap: Map<string, any>): any {
    const type = comp.component;
    const props = comp.properties || comp.props || comp;

    switch (type) {
      case 'Column': {
        const childIds = props.children || comp.children || [];
        const children = childIds.map((id: string) => {
          const child = compMap.get(id);
          return child ? this._renderComponent(child, compMap) : html`<span style="color:red">Missing ${id}</span>`;
        });
        return html`<a2ui-column>${children}</a2ui-column>`;
      }

      case 'Row': {
        const childIds = props.children || comp.children || [];
        const children = childIds.map((id: string) => {
          const child = compMap.get(id);
          return child ? this._renderComponent(child, compMap) : html`<span style="color:red">Missing ${id}</span>`;
        });
        return html`<a2ui-row>${children}</a2ui-row>`;
      }

      case 'Card': {
        const childId = props.child || comp.child;
        const child = childId ? compMap.get(childId) : null;
        return html`
          <a2ui-card>
            ${child ? this._renderComponent(child, compMap) : html`<slot></slot>`}
          </a2ui-card>
        `;
      }

      case 'Text': {
        const textVal = props.text !== undefined ? props.text : (comp.text || '');
        const variantVal = props.variant || comp.variant || props.usageHint || 'body';
        return html`<a2ui-text .text=${String(textVal)} .variant=${variantVal}></a2ui-text>`;
      }

      case 'Button': {
        const childId = props.child || comp.child;
        const child = childId ? compMap.get(childId) : null;
        const labelVal = props.label || comp.label || '';
        const variantVal = props.variant || comp.variant || 'default';
        const actionVal = props.action || comp.action || '';
        return html`
          <a2ui-button .label=${labelVal} .variant=${variantVal} .action=${actionVal}>
            ${child ? this._renderComponent(child, compMap) : labelVal}
          </a2ui-button>
        `;
      }

      case 'Divider':
        return html`<hr style="border: none; border-top: 1px solid rgba(148, 163, 184, 0.2); margin: 12px 0;" />`;

      default:
        return html`<div>Unknown A2UI component: ${type}</div>`;
    }
  }
}
