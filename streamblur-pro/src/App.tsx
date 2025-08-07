import { useState } from "react";
import { invoke } from "@tauri-apps/api/tauri";

function App() {
  const [greetMsg, setGreetMsg] = useState("");
  const [name, setName] = useState("");

  async function greet() {
    // Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
    setGreetMsg(await invoke("greet", { name }));
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 text-white flex items-center justify-center">
      <div className="text-center space-y-6">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
          🎥 StreamBlur Pro
        </h1>
        <p className="text-xl text-gray-300">Tauri v1 + React Setup Complete!</p>
        
        <div className="space-y-4">
          <input
            className="px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-gray-400"
            onChange={(e) => setName(e.currentTarget.value)}
            placeholder="Enter a name..."
          />
          <br />
          <button
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition-all"
            onClick={greet}
          >
            Greet
          </button>
        </div>
        
        {greetMsg && (
          <p className="text-green-400 font-semibold">{greetMsg}</p>
        )}
      </div>
    </div>
  );
}

export default App;