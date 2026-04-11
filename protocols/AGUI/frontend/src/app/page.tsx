"use client";

import { useEffect, useState } from "react";
import { CopilotPopup } from "@copilotkit/react-ui";
import { Terminal, Cpu, ShieldCheck } from "lucide-react";

interface AgentInfo {
  name: string;
  description: string;
  instruction: string;
  tools: { name: string; description: string }[];
}

export default function Home() {
  const [agentInfo, setAgentInfo] = useState<AgentInfo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchInfo() {
      try {
        const res = await fetch("http://127.0.0.1:8000/info");
        if (res.ok) {
          const data = await res.json();
          setAgentInfo(data);
        }
      } catch (err) {
        console.error("Failed to fetch agent info", err);
      } finally {
        setLoading(false);
      }
    }
    fetchInfo();
  }, []);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[400px_1fr] min-h-screen bg-[#020617] text-slate-200">
      {/* Sidebar: Capabilities Log */}
      <aside className="border-r border-slate-800 bg-slate-900/50 p-6 overflow-y-auto">
        <div className="flex items-center gap-2 mb-8">
          <Terminal className="text-blue-500 w-6 h-6" />
          <h2 className="text-xl font-bold font-['Outfit'] text-white">Agent Capabilities</h2>
        </div>

        {loading ? (
          <div className="animate-pulse space-y-4">
            <div className="h-4 bg-slate-800 rounded w-3/4"></div>
            <div className="h-20 bg-slate-800 rounded"></div>
            <div className="h-4 bg-slate-800 rounded w-1/4"></div>
            <div className="h-32 bg-slate-800 rounded"></div>
          </div>
        ) : agentInfo ? (
          <div className="space-y-8">
            <section>
              <div className="flex items-center gap-2 mb-3 text-blue-400">
                <Cpu className="w-4 h-4" />
                <h3 className="text-xs font-bold uppercase tracking-wider">Identity</h3>
              </div>
              <div className="p-4 bg-slate-950 rounded-lg border border-slate-800">
                <div className="text-white font-semibold mb-1">{agentInfo.name}</div>
                <div className="text-sm text-slate-400">{agentInfo.description}</div>
              </div>
            </section>

            <section>
              <div className="flex items-center gap-2 mb-3 text-blue-400">
                <ShieldCheck className="w-4 h-4" />
                <h3 className="text-xs font-bold uppercase tracking-wider">Tools & Skills</h3>
              </div>
              <div className="space-y-3">
                {agentInfo.tools.map((tool) => (
                  <div key={tool.name} className="p-3 bg-slate-950/50 rounded-lg border border-slate-800 hover:border-blue-500/50 transition-colors">
                    <div className="text-blue-300 font-mono text-sm mb-1">{tool.name}</div>
                    <div className="text-xs text-slate-500 leading-relaxed">{tool.description}</div>
                  </div>
                ))}
              </div>
            </section>

            <section>
               <div className="flex items-center gap-2 mb-3 text-blue-400">
                <Terminal className="w-4 h-4" />
                <h3 className="text-xs font-bold uppercase tracking-wider">System Logic</h3>
              </div>
              <div className="p-4 bg-slate-950 rounded-lg border border-slate-800 text-xs text-slate-400 font-mono whitespace-pre-wrap leading-relaxed max-h-60 overflow-y-auto">
                {agentInfo.instruction}
              </div>
            </section>
          </div>
        ) : (
          <div className="text-slate-500 text-sm">Failed to connect to agent server.</div>
        )}
      </aside>

      {/* Main Content */}
      <main className="flex flex-col items-center justify-center p-8 lg:p-20 text-center sm:text-left">
        <div className="max-w-2xl">
          <h1 className="text-5xl font-bold text-white mb-6 font-['Outfit'] bg-gradient-to-r from-blue-500 to-cyan-400 bg-clip-text text-transparent">
            Google ADK + AG-UI
          </h1>
          <p className="text-xl text-slate-400 mb-12 leading-relaxed">
            Interoperability protocol in action. The **Capabilities Log** on the left shows exactly what the agent "thinks" it can do, synced directly from the backend via AG-UI.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="p-6 bg-slate-900/50 border border-slate-800 rounded-2xl">
              <div className="text-blue-500 font-bold mb-2">01. Discovery</div>
              <div className="text-sm text-slate-500">The frontend queries the backend for its manifest and tool definitions.</div>
            </div>
            <div className="p-6 bg-slate-900/50 border border-slate-800 rounded-2xl">
              <div className="text-blue-500 font-bold mb-2">02. Execution</div>
              <div className="text-sm text-slate-500">Actions are standardized using the AG-UI event protocol.</div>
            </div>
          </div>
        </div>
      </main>

      <CopilotPopup
        instructions="Help the user with currency exchange rates using the currency_agent."
        labels={{
          title: "Currency Assistant",
          initial: "Hi! How can I help you with exchange rates today?",
        }}
        defaultOpen={true}
        clickOutsideToClose={false}
      />
    </div>
  );
}
