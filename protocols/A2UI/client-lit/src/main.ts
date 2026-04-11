import { LitElement, html, css } from 'lit';
import { customElement, state } from 'lit/decorators.js';
import './components/a2ui-surface';

@customElement('a2ui-app')
export class A2UIApp extends LitElement {
  @state() private _messages: { role: string; text: string; ui?: any }[] = [];
  @state() private _input = '';
  @state() private _loading = false;

  static styles = css`
    :host { display: block; }
    .chat-window {
      height: 500px;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      scrollbar-width: thin;
    }
    .message { max-width: 80%; padding: 12px 16px; border-radius: 12px; font-family: 'Inter', sans-serif; }
    .user { align-self: flex-end; background: #2563eb; color: white; }
    .agent { align-self: flex-start; background: #1e293b; border: 1px solid #334155; }
    
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
      padding: 12px;
      border-radius: 8px;
      color: white;
      font-family: inherit;
      outline: none;
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
      transition: opacity 0.2s;
    }
    button:disabled { opacity: 0.5; }
  `;

  render() {
    return html`
      <div style="background: #1e293b; border-radius: 16px; overflow: hidden; border: 1px solid #334155; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);">
        <div style="padding: 16px; background: #0f172a; border-bottom: 1px solid #334155;">
          <h2 style="margin: 0; font-family: 'Outfit'; font-size: 18px; color: #60a5fa;">A2UI Agent Deep Dive</h2>
        </div>
        
        <div class="chat-window">
          ${this._messages.map(m => html`
            <div class="message ${m.role}">
              <div style="line-height: 1.5;">${m.text}</div>
              ${m.ui ? html`<a2ui-surface .components=${m.ui.components} .rootId=${m.ui.rootId || 'root'}></a2ui-surface>` : ''}
            </div>
          `)}
          ${this._loading ? html`<div class="message agent" style="color: #94a3b8">Thinking...</div>` : ''}
        </div>

        <div class="input-area">
          <input 
            type="text" 
            placeholder="Ask about exchange rates..." 
            .value=${this._input}
            @input=${(e: any) => this._input = e.target.value}
            @keypress=${(e: any) => e.key === 'Enter' && this._sendMessage()}
          />
          <button @click=${this._sendMessage} ?disabled=${this._loading || !this._input}>Send</button>
        </div>
      </div>
    `;
  }

  private async _sendMessage() {
    if (!this._input || this._loading) return;
    
    const text = this._input;
    this._input = '';
    this._messages = [...this._messages, { role: 'user', text }];
    this._loading = true;

    try {
      console.log('Sending message to agent...');
      const response = await fetch('http://127.0.0.1:10001', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          jsonrpc: "2.0",
          method: "message/send",
          params: {
            message: {
              role: "user",
              parts: [{ kind: "text", text: text }],
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
      // In Task-based response, history is in result.history
      // In direct Message response, result is the Message itself
      const history = result.history || [result];
      
      const agentTurn = [...history].reverse().find((t: any) => t.role === 'agent');
      
      if (agentTurn) {
        const part = agentTurn.parts[0];
        let content = part.text || '';
        let ui = null;

        if (content.includes('---a2ui_JSON---')) {
          const splitParts = content.split('---a2ui_JSON---');
          content = splitParts[0].trim();
          const jsonStr = splitParts[1].trim()
            .replace(/```json/g, '')
            .replace(/```/g, '')
            .trim();
          
          try {
            const uiMsgs = JSON.parse(jsonStr);
            const surfaceUpdate = uiMsgs.find((m: any) => m.surfaceUpdate);
            if (surfaceUpdate) {
              ui = surfaceUpdate.surfaceUpdate;
            }
          } catch (e) {
            console.error('Failed to parse A2UI JSON', e);
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
