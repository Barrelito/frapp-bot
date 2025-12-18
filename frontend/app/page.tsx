'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, Upload, Info } from 'lucide-react';

export default function Home() {
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant'; content: string }[]>([
    { role: 'assistant', content: 'Hej! Jag är din FRAPP-support. Jag har läst manualen. Vad undrar du?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input;
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMessage }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Kunde inte nå servern. Kontrollera att backenden är igång.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async () => {
    // Hidden file input trigger could be added here
    alert("För prototypen laddas manualen manuellt via backend, men här skulle du kunna ladda upp nya filer.");
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 text-gray-900 font-sans">
      {/* Header */}
      <header className="bg-blue-700 text-white p-4 shadow-md flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className="bg-white p-1 rounded-full">
            <Info className="text-blue-700 w-6 h-6" />
          </div>
          <h1 className="text-xl font-bold tracking-tight">FRAPP Support Agent</h1>
        </div>
        <button className="text-sm bg-blue-600 hover:bg-blue-500 px-3 py-1 rounded transition">
          Driftstatus: OK
        </button>
      </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin scrollbar-thumb-gray-300">
        <div className="max-w-3xl mx-auto space-y-4">
          {messages.map((m, i) => (
            <div
              key={i}
              className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 shadow-sm ${m.role === 'user'
                    ? 'bg-blue-600 text-white rounded-br-none'
                    : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none'
                  }`}
              >
                <p className="leading-relaxed whitespace-pre-wrap text-sm md:text-base">{m.content}</p>
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-white text-gray-500 border border-gray-200 rounded-2xl rounded-bl-none px-4 py-3 shadow-sm">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input Area */}
      <footer className="bg-white border-t border-gray-200 p-4">
        <div className="max-w-3xl mx-auto">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <button
              type="button"
              onClick={handleUpload}
              className="p-3 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition"
              title="Ladda upp dokument"
            >
              <Upload className="w-6 h-6" />
            </button>
            <input
              className="flex-1 bg-gray-100 border-0 text-gray-900 placeholder:text-gray-500 focus:ring-2 focus:ring-blue-500 rounded-xl px-4 py-3 outline-none transition"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Beskriv problemet..."
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white p-3 rounded-xl transition shadow-md"
            >
              <Send className="w-6 h-6" />
            </button>
          </form>
          <p className="text-center text-xs text-gray-400 mt-2">
            AI kan göra misstag. Kontrollera alltid med manualen om du är osäker.
          </p>
        </div>
      </footer>
    </div>
  );
}
