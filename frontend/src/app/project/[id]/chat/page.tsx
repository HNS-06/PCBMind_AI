'use client';

import { useState, useRef, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { Send, Loader2, Bot, User } from 'lucide-react';
import { chatAPI } from '@/lib/api';
import { useAppStore } from '@/stores';
import type { ChatMessage } from '@/types';

export default function ChatPage() {
  const params = useParams();
  const projectId = params.id as string;
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { chatMessages, addChatMessage, conversationId, setConversationId } = useAppStore();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  async function handleSend() {
    if (!input.trim() || sending) return;
    const userMsg: ChatMessage = { role: 'user', content: input.trim(), timestamp: new Date().toISOString() };
    addChatMessage(userMsg);
    setInput('');
    setSending(true);

    try {
      const res = await chatAPI.send({
        message: userMsg.content,
        project_id: projectId,
        conversation_id: conversationId || undefined,
        model: 'groq',
      });
      const assistantMsg: ChatMessage = {
        role: 'assistant',
        content: res.data.message.content,
        timestamp: res.data.message.timestamp,
      };
      addChatMessage(assistantMsg);
      setConversationId(res.data.conversation_id);
    } catch {
      addChatMessage({ role: 'assistant', content: 'Sorry, an error occurred. Please try again.' });
    } finally {
      setSending(false);
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-7rem)]">
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {chatMessages.length === 0 && (
          <div className="text-center py-20 space-y-3">
            <Bot className="w-12 h-12 text-primary mx-auto" />
            <h3 className="font-medium">AI Hardware Assistant</h3>
            <p className="text-sm text-muted-foreground max-w-md mx-auto">
              Ask questions about your circuit design, component selection, or request changes to the PCB layout.
            </p>
            <div className="flex flex-wrap justify-center gap-2 mt-4">
              {["Why is this resistor 10K?", "Can I replace ESP32 with RP2040?", "Make PCB smaller"].map((q) => (
                <button key={q} onClick={() => setInput(q)}
                  className="text-xs px-3 py-1.5 bg-secondary rounded-full hover:bg-secondary/80 transition-colors">
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {chatMessages.map((msg, i) => (
          <div key={i} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            {msg.role === 'assistant' && (
              <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4 text-primary" />
              </div>
            )}
            <div className={`max-w-[70%] p-3 rounded-xl text-sm ${
              msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-card border border-border'
            }`}>
              <div className="whitespace-pre-wrap">{msg.content}</div>
            </div>
            {msg.role === 'user' && (
              <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center shrink-0">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}
        {sending && (
          <div className="flex gap-3">
            <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center">
              <Bot className="w-4 h-4 text-primary" />
            </div>
            <div className="p-3 bg-card border border-border rounded-xl">
              <Loader2 className="w-5 h-5 animate-spin text-primary" />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 border-t border-border">
        <div className="flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
            placeholder="Ask about your circuit design..."
            className="flex-1 bg-card border border-border rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || sending}
            className="bg-primary text-primary-foreground px-4 py-2 rounded-lg hover:bg-primary/90 disabled:opacity-50"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
