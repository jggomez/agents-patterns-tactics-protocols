import { LitElement, html, css } from 'lit';
import { customElement, state } from 'lit/decorators.js';
import { MessageProcessor } from '@a2ui/web_core/v0_9';
import { basicCatalog } from '@a2ui/lit/v0_9';
import './components/a2ui-surface';

interface UiPayload {
  surfaceId: string;
  surfaceModel?: any;
  components: any[];
  dataModel?: Record<string, any>;
  rootId: string;
}

@customElement('a2ui-app')
export class A2UIApp extends LitElement {
  @state() private _messages: { role: string; text: string; ui?: UiPayload | null }[] = [];
  @state() private _input = '';
  @state() private _loading = false;

  private _processor = new MessageProcessor([basicCatalog]);

  static styles = css`
    :host { display: block; }
    .chat-window {
      height: 540px;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      scrollbar-width: thin;
    }
    .message { max-width: 85%; padding: 14px 18px; border-radius: 14px; font-family: 'Inter', sans-serif; }
    .user { align-self: flex-end; background: #2563eb; color: white; }
    .agent { align-self: flex-start; background: #1e293b; border: 1px solid #334155; }
    
    .badge-v09 {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 2px 8px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 600;
      background: rgba(16, 185, 129, 0.2);
      color: #34d399;
      border: 1px solid rgba(52, 211, 153, 0.3);
      margin-left: 8px;
    }

    .input-area {
      display: flex;
      gap: 12px;
      padding: 16px;
      background: #1e293b;
      border-top: 1px solid #334155;
    }
    input {
      flex: 1;
      background: #0f172a;
      border: 1px solid #334155;
      padding: 12px 16px;
      border-radius: 8px;
      color: white;
      font-family: inherit;
      outline: none;
      font-size: 14px;
    }
    input:focus { border-color: #2563eb; }
    button {
      background: #2563eb;
      color: white;
      border: none;
      padding: 0 24px;
      border-radius: 8px;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.2s;
    }
    button:hover:not(:disabled) {
      background: #1d4ed8;
    }
    button:disabled { opacity: 0.5; }
  `;

  render() {
    return html`
      <div style="background: #1e293b; border-radius: 16px; overflow: hidden; border: 1px solid #334155; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);">
        <div style="padding: 16px 20px; background: #0f172a; border-bottom: 1px solid #334155; display: flex; align-items: center; justify-content: space-between;">
          <div style="display: flex; align-items: center;">
            <h2 style="margin: 0; font-family: 'Outfit', sans-serif; font-size: 18px; color: #60a5fa;">A2UI Agent Deep Dive</h2>
            <span class="badge-v09">A2UI v0.9 (Prompt-First)</span>
          </div>
          <span style="font-size: 12px; color: #94a3b8;">Port :10001 (A2A)</span>
        </div>
        
        <div class="chat-window">
          ${this._messages.map(m => html`
            <div class="message ${m.role}">
              <div style="line-height: 1.5;">${m.text}</div>
              ${m.ui ? html`
                <a2ui-surface 
                  .surface=${m.ui.surfaceModel}
                  .components=${m.ui.components}
                  .dataModel=${m.ui.dataModel}
                  .rootId=${m.ui.rootId || 'root'}
                  @a2ui-action=${(e: CustomEvent) => this._handleUiAction(e.detail.action)}
                ></a2ui-surface>
              ` : ''}
            </div>
          `)}
          ${this._loading ? html`<div class="message agent" style="color: #94a3b8">Thinking & generating A2UI v0.9 components...</div>` : ''}
        </div>

        <div class="input-area">
          <input 
            type="text" 
            placeholder="Ask about exchange rates (e.g. 100 USD to MXN, 50 EUR to USD)..." 
            .value=${this._input}
            @input=${(e: any) => this._input = e.target.value}
            @keypress=${(e: any) => e.key === 'Enter' && this._sendMessage()}
          />
          <button @click=${() => this._sendMessage()} ?disabled=${this._loading || !this._input}>Send</button>
        </div>
      </div>
    `;
  }

  private _handleUiAction(action: string) {
    console.log('A2UI Action Triggered:', action);
    if (action === 'refresh_rate') {
      this._sendMessage('Refresh the current exchange rate');
    }
  }

  private async _sendMessage(overrideText?: string) {
    const textToSend = overrideText || this._input;
    if (!textToSend || this._loading) return;
    
    if (!overrideText) {
      this._input = '';
    }
    this._messages = [...this._messages, { role: 'user', text: textToSend }];
    this._loading = true;

    try {
      console.log('Sending message to A2UI v0.9 agent...');
      const response = await fetch('http://127.0.0.1:10001', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          jsonrpc: "2.0",
          method: "message/send",
          params: {
            message: {
              role: "user",
              parts: [{ kind: "text", text: textToSend }],
              messageId: Math.random().toString(36).substring(7)
            }
          },
          id: Math.random().toString(36).substring(7)
        })
      });

      const data = await response.json();
      console.log('Agent raw response:', data);

      if (data.error) {
        throw new Error(`Agent Error (${data.error.code}): ${data.error.message}`);
      }

      const result = data.result;
      const history = result.history || [result];
      const agentTurn = [...history].reverse().find((t: any) => t.role === 'agent');
      
      if (agentTurn) {
        const part = agentTurn.parts[0];
        let content = part.text || '';
        let ui: UiPayload | null = null;

        if (content.includes('---a2ui_JSON---')) {
          const splitParts = content.split('---a2ui_JSON---');
          content = splitParts[0].trim();
          const jsonStr = splitParts[1].trim()
            .replace(/```json/g, '')
            .replace(/```/g, '')
            .trim();
          
          try {
            const rawUiMsgs = JSON.parse(jsonStr);
            const uiMsgs: any[] = Array.isArray(rawUiMsgs) ? rawUiMsgs : [rawUiMsgs];

            // 1. Process messages using official @a2ui/web_core v0.9 MessageProcessor
            try {
              this._processor.processMessages(uiMsgs);
            } catch (procErr) {
              console.warn('Official MessageProcessor warning:', procErr);
            }

            // 2. Extract v0.9 message parts (createSurface, updateComponents, updateDataModel)
            const createMsg = uiMsgs.find((m: any) => m.createSurface);
            const updateCompMsg = uiMsgs.find((m: any) => m.updateComponents);
            const updateDataMsg = uiMsgs.find((m: any) => m.updateDataModel);
            const legacySurfaceUpdate = uiMsgs.find((m: any) => m.surfaceUpdate);

            const surfaceId = createMsg?.createSurface?.surfaceId 
              || updateCompMsg?.updateComponents?.surfaceId 
              || legacySurfaceUpdate?.surfaceUpdate?.surfaceId 
              || 'currency_view';

            const components = updateCompMsg?.updateComponents?.components 
              || legacySurfaceUpdate?.surfaceUpdate?.components 
              || [];

            const dataModel = updateDataMsg?.updateDataModel?.value || {};
            const surfaceModel = this._processor.model.getSurface(surfaceId);

            ui = {
              surfaceId,
              surfaceModel,
              components,
              dataModel,
              rootId: 'root'
            };
          } catch (e) {
            console.error('Failed to parse A2UI v0.9 JSON:', e);
          }
        }
        
        this._messages = [...this._messages, { role: 'agent', text: content, ui }];
      }
    } catch (e: any) {
      console.error('Connection Error:', e);
      this._messages = [...this._messages, { role: 'agent', text: `⚠️ ${e.message || 'Error connecting to agent'}` }];
    } finally {
      this._loading = false;
    }
  }
}
