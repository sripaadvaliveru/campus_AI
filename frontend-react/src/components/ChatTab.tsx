import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import {
  Send, ThumbsUp, ThumbsDown,
  Copy, Check, Trash2, Bot, Lightbulb,
  ChevronRight, Sparkles
} from 'lucide-react';
import { ShimmerButton, Badge, BlueprintStat } from './ui/Primitives';
import { DoodleChat } from './ui/doodles/DoodleChat';
import { cn } from '../lib/cn';
import type { College, Message } from '../types';

interface ChatTabProps {
  selectedCollege: College | null;
  messages: Message[];
  onSendMessage: (text: string) => Promise<void>;
  onClearHistory: () => void;
  loading: boolean;
  onSendFeedback?: (id: string, rating: 1 | -1) => void;
}

const SUGGESTIONS = [
  { icon: '📋', text: 'What are the attendance requirements?' },
  { icon: '🎓', text: 'How is CGPA calculated?' },
  { icon: '🏥', text: 'Where is the campus health center?' },
  { icon: '📜', text: 'How do I get a Bonafide Certificate?' },
  { icon: '🎯', text: 'What are the placement statistics?' },
  { icon: '🏠', text: 'Tell me about hostel facilities.' },
];

export const ChatTab: React.FC<ChatTabProps> = ({
  selectedCollege, messages, onSendMessage, onClearHistory, loading, onSendFeedback,
}) => {
  const [input, setInput] = useState('');
  const [copied, setCopied] = useState<string | null>(null);
  const [feedbacks, setFeedbacks] = useState<Record<string, 1 | -1>>({});
  const [showSuggestions, setShowSuggestions] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const college = selectedCollege || { id: 'general', name: 'General', short: 'General', icon: '🇮🇳', color: '#D97706' };

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  // Auto-resize textarea with smooth transition
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.style.height = 'auto';
      inputRef.current.style.height = `${Math.min(inputRef.current.scrollHeight, 128)}px`;
    }
  }, [input]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    const text = input;
    setInput('');
    await onSendMessage(text);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text).catch(() => {});
    setCopied(id);
    setTimeout(() => setCopied(null), 2000);
  };

  const handleFeedback = (id: string, rating: 1 | -1) => {
    setFeedbacks(prev => ({ ...prev, [id]: rating }));
    onSendFeedback?.(id, rating);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)]">
      {/* ── Header ──────────────────────────────────────── */}
      <div className="flex items-center justify-between px-4 py-3 bg-[#FBF8F3]/80 backdrop-blur-md border-b border-[#E8E2D5] flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-amber-600 to-amber-700 flex items-center justify-center">
            <Sparkles className="h-4 w-4 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-semibold text-stone-800">Chat with AI</h2>
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-amber-500" />
              </span>
            </div>
            <p className="text-xs text-stone-400">
              {college.icon} {college.name}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-1">
          {messages.length > 0 && (
            <button
              onClick={() => setShowSuggestions(v => !v)}
              className="p-2 rounded-lg text-stone-400 hover:text-stone-600 hover:bg-[#F3ECE1] transition-all duration-150"
              aria-label="Show suggestions"
            >
              <Lightbulb className="h-4 w-4" />
            </button>
          )}
          {messages.length > 0 && (
            <button
              onClick={onClearHistory}
              className="p-2 rounded-lg text-stone-400 hover:text-stone-600 hover:bg-[#F3ECE1] transition-all duration-150"
              aria-label="Clear chat history"
            >
              <Trash2 className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>

      {/* ── Messages Area ───────────────────────────────── */}
      <div className="flex-1 overflow-y-auto px-4 py-6 relative">
        {/* Doodle background for empty state */}
        {messages.length === 0 && <DoodleChat />}

        {/* Subtle gradient background */}
        {messages.length > 0 && (
          <div className="absolute inset-0 bg-gradient-to-b from-amber-50/30 to-transparent pointer-events-none" />
        )}

        {messages.length === 0 ? (
          /* ── Empty State ──────────────────────────────── */
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            className="h-full flex flex-col items-center justify-center max-w-lg mx-auto text-center space-y-8 relative z-10"
          >
            {/* Large bot icon */}
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ type: 'spring', stiffness: 300, damping: 20, delay: 0.1 }}
              className="w-16 h-16 rounded-2xl bg-gradient-to-br from-amber-600 to-amber-700 flex items-center justify-center shadow-lg shadow-amber-900/25"
            >
              <Bot className="h-8 w-8 text-white" />
            </motion.div>

            <div className="space-y-2">
              <h3 className="font-display text-2xl font-bold gradient-text bg-gradient-to-r from-amber-700 to-amber-800">
                What can I help you with?
              </h3>
              <p className="text-sm text-stone-500 max-w-sm mx-auto">
                Ask about academics, events, contacts, or campus life for {college.short}.
              </p>
            </div>

            {/* Suggestion cards */}
            <div className="w-full space-y-2">
              <p className="text-xs text-stone-400 font-medium">Try asking</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {SUGGESTIONS.map((s, i) => (
                  <motion.button
                    key={i}
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 + i * 0.05 }}
                    onClick={() => setInput(s.text)}
                    className="group flex items-center gap-2.5 px-4 py-3 rounded-xl bg-[#FFFDF9] border border-[#E3D9C6] text-left text-xs text-stone-600 hover:border-amber-500/60 hover:bg-amber-50/50 hover:shadow-md hover:text-stone-900 transition-all duration-200"
                  >
                    <span className="text-base flex-shrink-0">{s.icon}</span>
                    <span className="flex-1 truncate">{s.text}</span>
                    <ChevronRight className="h-3 w-3 text-stone-300 group-hover:text-amber-600 transition-colors flex-shrink-0" />
                  </motion.button>
                ))}
              </div>
            </div>
          </motion.div>
        ) : (
          /* ── Message List ─────────────────────────────── */
          <div className="max-w-3xl mx-auto space-y-6 relative z-10">
            <AnimatePresence initial={false}>
              {messages.map((msg) => {
                const isBot = msg.role === 'assistant';
                return (
                  <motion.div
                    key={msg.id}
                    initial={{ opacity: 0, y: 12, x: isBot ? -20 : 20, scale: 0.98 }}
                    animate={{ opacity: 1, y: 0, x: 0, scale: 1 }}
                    transition={{ type: 'spring', stiffness: 400, damping: 28 }}
                    className={cn('flex gap-2.5', isBot ? '' : 'flex-row-reverse')}
                  >
                    {/* Bot icon (only for bot messages) */}
                    {isBot && (
                      <div className="w-5 h-5 rounded-md bg-gradient-to-br from-amber-600 to-amber-700 flex items-center justify-center flex-shrink-0 mt-1">
                        <Bot className="h-2.5 w-2.5 text-white" />
                      </div>
                    )}

                    {/* Message content */}
                    <div className={cn('space-y-1', isBot ? 'max-w-[85%]' : 'max-w-[75%]')}>
                      {/* Bubble */}
                      <div className={cn(
                        'relative group',
                        isBot
                          ? 'text-stone-700'
                          : 'bg-gradient-to-r from-amber-600 to-amber-700 text-white px-4 py-2.5 rounded-2xl rounded-br-md shadow-md shadow-amber-900/10'
                      )}>
                        {isBot ? (
                          <div className="chat-prose prose prose-sm max-w-none">
                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                          </div>
                        ) : (
                          <pre className="whitespace-pre-wrap font-sans text-[13px] leading-relaxed">{msg.content}</pre>
                        )}

                        {/* Bot metadata */}
                        {isBot && (msg.toolUsed || msg.responseTimeMs) && (
                          <div className="mt-2 flex flex-wrap gap-1.5">
                            {msg.toolUsed && (
                              <BlueprintStat label="TOOL" value={msg.toolUsed} />
                            )}
                            {msg.responseTimeMs !== undefined && (
                              <BlueprintStat label="TIME" value={`${msg.responseTimeMs}ms`} />
                            )}
                          </div>
                        )}
                      </div>

                      {/* Timestamp + Actions row */}
                      <div className={cn('flex items-center gap-2 px-1', isBot ? '' : 'flex-row-reverse')}>
                        <span className="text-2xs text-stone-400">{msg.timestamp}</span>

                        {isBot && (
                          <div className="flex items-center gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity duration-150">
                            <button
                              onClick={() => handleCopy(msg.content, msg.id)}
                              className="p-1 rounded text-stone-400 hover:text-stone-600 transition-colors"
                              aria-label="Copy message"
                            >
                              {copied === msg.id ? <Check className="h-3 w-3 text-amber-600" /> : <Copy className="h-3 w-3" />}
                            </button>
                            <button
                              onClick={() => handleFeedback(msg.id, 1)}
                              className={cn('p-1 rounded transition-colors', feedbacks[msg.id] === 1 ? 'text-amber-600' : 'text-stone-400 hover:text-stone-600')}
                              aria-label="Good response"
                            >
                              <ThumbsUp className="h-3 w-3" />
                            </button>
                            <button
                              onClick={() => handleFeedback(msg.id, -1)}
                              className={cn('p-1 rounded transition-colors', feedbacks[msg.id] === -1 ? 'text-rose-500' : 'text-stone-400 hover:text-stone-600')}
                              aria-label="Bad response"
                            >
                              <ThumbsDown className="h-3 w-3" />
                            </button>
                          </div>
                        )}

                        {feedbacks[msg.id] && isBot && (
                          <span className="text-2xs text-amber-600 flex items-center gap-0.5">
                            <Check className="h-2.5 w-2.5" /> Logged
                          </span>
                        )}
                      </div>
                    </div>
                  </motion.div>
                );
              })}
            </AnimatePresence>

            {/* ── Typing Indicator ─────────────────────── */}
            {loading && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex gap-2.5"
              >
                <div className="w-5 h-5 rounded-md bg-gradient-to-br from-amber-600 to-amber-700 flex items-center justify-center flex-shrink-0 mt-1">
                  <Bot className="h-2.5 w-2.5 text-white" />
                </div>
                <div className="flex items-center gap-2.5 pt-1">
                  <div className="flex gap-1">
                    {[0, 1, 2].map(i => (
                      <motion.div
                        key={i}
                        animate={{ y: [0, -4, 0] }}
                        transition={{ duration: 0.6, repeat: Infinity, delay: i * 0.12 }}
                        className="w-2 h-2 rounded-full bg-amber-400"
                      />
                    ))}
                  </div>
                  <span className="text-xs text-stone-400 italic">Searching campus data…</span>
                </div>
              </motion.div>
            )}
            <div ref={endRef} />
          </div>
        )}

        {/* ── Collapsible Suggestions ──────────────────── */}
        {messages.length > 0 && showSuggestions && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="max-w-3xl mx-auto space-y-2 pt-3 pb-4 relative z-10"
          >
            <p className="text-xs text-stone-400 font-medium px-1">Try asking</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {SUGGESTIONS.map((s, i) => (
                <button
                  key={i}
                  onClick={() => { setInput(s.text); setShowSuggestions(false); }}
                  className="group flex items-center gap-2 px-3 py-2 rounded-xl bg-[#FFFDF9] border border-[#E3D9C6] hover:border-amber-500/60 hover:bg-amber-50/50 text-left text-xs text-stone-600 hover:text-stone-900 transition-all duration-200"
                >
                  <span className="text-sm flex-shrink-0">{s.icon}</span>
                  <span className="flex-1 truncate">{s.text}</span>
                  <ChevronRight className="h-3 w-3 text-stone-300 group-hover:text-amber-600 transition-colors flex-shrink-0" />
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </div>

      {/* ── Input Area ──────────────────────────────────── */}
      <div className="flex-shrink-0 px-4 pb-4 relative z-10">
        <div className="max-w-3xl mx-auto">
          <div className="relative bg-[#FFFDF9] backdrop-blur-xl rounded-2xl border border-[#E3D9C6] shadow-lg shadow-amber-900/5 overflow-hidden transition-all duration-200 focus-within:border-amber-600/60 focus-within:ring-2 focus-within:ring-amber-500/10">
            {/* College context */}
            <div className="flex items-center gap-2 px-4 pt-3 pb-0">
              <span className="text-sm">{college.icon}</span>
              <span className="text-2xs text-stone-400 font-medium">Ask about {college.short}</span>
            </div>

            {/* Textarea */}
            <textarea
              ref={inputRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your question..."
              aria-label={`Ask ${college.short} AI assistant a question`}
              rows={1}
              disabled={loading}
              className="w-full bg-transparent text-sm text-stone-900 placeholder-stone-400 px-4 pt-2 pb-2 pr-12 focus:outline-none resize-none disabled:opacity-50 max-h-32 overflow-y-auto"
              style={{ lineHeight: '1.6', transition: 'height 0.15s ease' }}
            />

            {/* Send button */}
            <div className="absolute right-2 bottom-2">
              <button
                onClick={handleSend}
                disabled={!input.trim() || loading}
                aria-label="Send message"
                className={cn(
                  'w-8 h-8 rounded-full flex items-center justify-center transition-all duration-200',
                  input.trim() && !loading
                    ? 'bg-gradient-to-r from-amber-600 to-amber-700 text-white shadow-sm hover:shadow-md hover:shadow-amber-500/25 active:scale-95'
                    : 'bg-[#E8E2D5] text-stone-400 cursor-not-allowed'
                )}
              >
                <Send className="h-3.5 w-3.5" />
              </button>
            </div>
          </div>

          <p className="text-2xs text-stone-400 text-center mt-2">
            Enter to send · Shift+Enter for new line
          </p>
        </div>
      </div>
    </div>
  );
};
