import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import {
  Send, Clock, Terminal, ThumbsUp, ThumbsDown,
  Copy, Check, Trash2, Bot, User, Lightbulb, Zap,
  ChevronRight, AlertCircle, MessageSquare
} from 'lucide-react';
import { ShimmerButton, Badge } from './ui/Primitives';
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

  const college = selectedCollege || { id: 'general', name: 'General', short: 'General', icon: '🇮🇳', color: '#2563EB' };

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  // Auto-grow textarea
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
    <div className="flex flex-col h-[calc(100vh-2rem)] lg:h-[calc(100vh-2rem)] bg-slate-50">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-3.5 border-b border-slate-200 bg-white flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="text-xl p-2 bg-slate-50 rounded-xl">{college.icon}</div>
            <div className="absolute -bottom-0.5 -right-0.5 w-2 h-2 rounded-full bg-emerald-500 border-2 border-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-bold text-slate-900">{college.short} AI Assistant</h2>
              <Badge variant="green" dot pulse className="hidden sm:inline-flex">Online</Badge>
            </div>
            <p className="text-2xs text-slate-500 truncate max-w-xs">{college.name}</p>
          </div>
        </div>

        {messages.length > 0 && (
          <>
            <ShimmerButton variant="ghost" size="sm" onClick={() => setShowSuggestions(v => !v)}>
              <Lightbulb className="h-3.5 w-3.5" />
              <span className="hidden sm:inline">{showSuggestions ? 'Hide' : 'Ideas'}</span>
            </ShimmerButton>
            <ShimmerButton variant="danger" size="sm" onClick={onClearHistory}>
              <Trash2 className="h-3.5 w-3.5" />
              <span className="hidden sm:inline">Clear</span>
            </ShimmerButton>
          </>
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4 relative">
        {messages.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="h-full flex flex-col items-center justify-center max-w-xl mx-auto text-center space-y-8 py-10"
          >
            <div className="relative">
              <div className="w-16 h-16 rounded-2xl bg-blue-50 border border-blue-100 flex items-center justify-center">
                <MessageSquare className="h-7 w-7 text-brand-blue" />
              </div>
            </div>

            <div className="space-y-2">
              <h3 className="font-display text-xl font-bold text-slate-900">Ask CampusAI anything</h3>
              <p className="text-sm text-slate-500 leading-relaxed">
                I can help with academic regulations, events, campus facilities,
                contacts, scholarships, and campus life — powered by real data.
              </p>
            </div>

            <div className="w-full space-y-2">
              <div className="flex items-center gap-1.5 text-2xs text-slate-400 uppercase tracking-wider font-semibold">
                <Lightbulb className="h-3 w-3" /> Try asking
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {SUGGESTIONS.map((s, i) => (
                  <motion.button
                    key={i}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.07 }}
                    onClick={() => setInput(s.text)}
                    className="flex items-center gap-2.5 px-3 py-2.5 rounded-xl bg-white hover:bg-blue-50 border border-slate-200 hover:border-blue-200 text-left text-xs text-slate-600 hover:text-slate-900 transition-all duration-150 group"
                  >
                    <span className="text-base flex-shrink-0">{s.icon}</span>
                    <span className="flex-1 truncate">{s.text}</span>
                    <ChevronRight className="h-3 w-3 text-slate-300 group-hover:text-brand-blue group-hover:translate-x-0.5 transition-all flex-shrink-0" />
                  </motion.button>
                ))}
              </div>
            </div>
          </motion.div>
        ) : (
          <div className="max-w-3xl mx-auto space-y-5">
            <AnimatePresence initial={false}>
              {messages.map((msg) => {
                const isBot = msg.role === 'assistant';
                return (
                  <motion.div
                    key={msg.id}
                    initial={{ opacity: 0, y: 16 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
                    className={cn('flex gap-3', isBot ? '' : 'flex-row-reverse')}
                  >
                    {/* Avatar */}
                    <div className={cn(
                      'w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5',
                      isBot
                        ? 'bg-brand-blue'
                        : 'bg-slate-700'
                    )}>
                      {isBot ? <Bot className="h-3.5 w-3.5 text-white" /> : <User className="h-3.5 w-3.5 text-white" />}
                    </div>

                    {/* Bubble */}
                    <div className={cn('max-w-[80%] space-y-1.5', isBot ? '' : '')}>
                      <div className={cn(
                        'relative group px-4 py-3 rounded-2xl text-sm leading-relaxed border',
                        isBot
                          ? 'bg-white text-slate-700 border-slate-200 shadow-sm'
                          : 'bg-brand-blue text-white border-blue-600'
                      )}>
                        {isBot ? (
                          <div className="prose prose-sm max-w-none prose-p:my-1 prose-headings:my-2 prose-pre:bg-slate-50 prose-pre:border prose-pre:border-slate-200 prose-code:text-brand-blue prose-code:bg-blue-50 prose-code:px-1 prose-code:rounded">
                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                          </div>
                        ) : (
                          <pre className="whitespace-pre-wrap font-sans text-[13px] leading-relaxed">{msg.content}</pre>
                        )}

                        {/* Bot metadata */}
                        {isBot && (msg.toolUsed || msg.responseTimeMs) && (
                          <div className="mt-3 pt-2.5 border-t border-slate-100 flex flex-wrap gap-2">
                            {msg.toolUsed && (
                              <span className="flex items-center gap-1 text-2xs font-medium text-slate-500 bg-slate-50 px-2 py-0.5 rounded border border-slate-200">
                                <Terminal className="h-2.5 w-2.5 text-brand-blue" />
                                {msg.toolUsed}
                              </span>
                            )}
                            {msg.responseTimeMs !== undefined && (
                              <span className="flex items-center gap-1 text-2xs text-slate-400">
                                <Clock className="h-2.5 w-2.5" />
                                {msg.responseTimeMs}ms
                              </span>
                            )}
                          </div>
                        )}

                        {/* Hover actions */}
                        <div className={cn(
                          'absolute top-2 opacity-0 group-hover:opacity-100 transition-opacity duration-150',
                          isBot ? 'right-2' : 'left-2'
                        )}>
                          <div className="flex items-center gap-1 bg-white rounded-lg p-1.5 border border-slate-200 shadow-sm">
                            <button
                              onClick={() => handleCopy(msg.content, msg.id)}
                              className="p-1 rounded text-slate-400 hover:text-slate-700 transition-colors"
                            >
                              {copied === msg.id ? <Check className="h-3 w-3 text-emerald-500" /> : <Copy className="h-3 w-3" />}
                            </button>
                            {isBot && (
                              <>
                                <button
                                  onClick={() => handleFeedback(msg.id, 1)}
                                  className={cn('p-1 rounded transition-colors', feedbacks[msg.id] === 1 ? 'text-brand-blue' : 'text-slate-400 hover:text-slate-700')}
                                >
                                  <ThumbsUp className="h-3 w-3" />
                                </button>
                                <button
                                  onClick={() => handleFeedback(msg.id, -1)}
                                  className={cn('p-1 rounded transition-colors', feedbacks[msg.id] === -1 ? 'text-rose-500' : 'text-slate-400 hover:text-slate-700')}
                                >
                                  <ThumbsDown className="h-3 w-3" />
                                </button>
                              </>
                            )}
                          </div>
                        </div>
                      </div>

                      <div className={cn('flex items-center gap-2 px-1 text-2xs text-slate-400', isBot ? '' : 'flex-row-reverse')}>
                        <span>{msg.timestamp}</span>
                        {feedbacks[msg.id] && (
                          <span className="text-emerald-500 flex items-center gap-0.5">
                            <Check className="h-2.5 w-2.5" /> Feedback logged
                          </span>
                        )}
                      </div>
                    </div>
                  </motion.div>
                );
              })}
            </AnimatePresence>

            {/* Typing indicator */}
            {loading && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex gap-3"
              >
                <div className="w-7 h-7 rounded-lg bg-brand-blue flex items-center justify-center flex-shrink-0">
                  <Bot className="h-3.5 w-3.5 text-white" />
                </div>
                <div className="bg-white border border-slate-200 shadow-sm px-4 py-3 rounded-2xl flex items-center gap-3">
                  <div className="flex gap-1">
                    {[0, 1, 2].map(i => (
                      <motion.div
                        key={i}
                        animate={{ y: [0, -6, 0] }}
                        transition={{ duration: 0.7, repeat: Infinity, delay: i * 0.15 }}
                        className="w-1.5 h-1.5 rounded-full bg-brand-blue"
                      />
                    ))}
                  </div>
                  <span className="text-xs text-slate-500">Searching campus data…</span>
                  <Zap className="h-3 w-3 text-amber-500 animate-bounce" />
                </div>
              </motion.div>
            )}
            <div ref={endRef} />
          </div>
        )}

        {/* Collapsible suggestions when messages exist */}
        {messages.length > 0 && showSuggestions && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="max-w-3xl mx-auto space-y-2 pt-2 pb-4"
          >
            <div className="flex items-center gap-1.5 text-2xs text-slate-400 uppercase tracking-wider font-semibold px-1">
              <Lightbulb className="h-3 w-3" /> Try asking
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {SUGGESTIONS.map((s, i) => (
                <button
                  key={i}
                  onClick={() => { setInput(s.text); setShowSuggestions(false); }}
                  className="flex items-center gap-2.5 px-3 py-2.5 rounded-xl bg-white hover:bg-blue-50 border border-slate-200 hover:border-blue-200 text-left text-xs text-slate-600 hover:text-slate-900 transition-all duration-150 group"
                >
                  <span className="text-base flex-shrink-0">{s.icon}</span>
                  <span className="flex-1 truncate">{s.text}</span>
                  <ChevronRight className="h-3 w-3 text-slate-300 group-hover:text-brand-blue group-hover:translate-x-0.5 transition-all flex-shrink-0" />
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </div>

      {/* Input Area */}
      <div className="flex-shrink-0 px-4 pb-4">
        <div className="max-w-3xl mx-auto">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden focus-within:ring-2 focus-within:ring-brand-blue focus-within:border-transparent transition-all duration-200">
            <textarea
              ref={inputRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={`Ask about ${college.short}… (Shift+Enter for new line)`}
              aria-label={`Ask ${college.short} AI assistant a question`}
              rows={1}
              disabled={loading}
              className="w-full bg-transparent text-sm text-slate-900 placeholder-slate-400 px-4 pt-3.5 pb-1 focus:outline-none resize-none disabled:opacity-50 max-h-32 overflow-y-auto"
              style={{ lineHeight: '1.6' }}
            />
            <div className="flex items-center justify-between px-3 pb-3 pt-1">
              <div className="flex items-center gap-1.5 text-2xs text-slate-400">
                <AlertCircle className="h-3 w-3" />
                <span>Context: {college.short}</span>
              </div>
              <ShimmerButton
                onClick={handleSend}
                disabled={!input.trim() || loading}
                size="sm"
                aria-label="Send message"
              >
                <Send className="h-3.5 w-3.5" />
                <span>Send</span>
              </ShimmerButton>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
