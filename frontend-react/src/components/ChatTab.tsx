import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import {
  Send, ThumbsUp, ThumbsDown,
  Copy, Check, Trash2, Bot, User, Lightbulb,
  ChevronRight, AlertCircle, MessageSquare
} from 'lucide-react';
import { ShimmerButton, Badge, BlueprintStat } from './ui/Primitives';
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
    <div className="flex flex-col h-[calc(100vh-2rem)] lg:h-[calc(100vh-2rem)]">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-100 bg-white flex-shrink-0">
        <div className="flex items-center gap-2.5">
          <span className="text-lg">{college.icon}</span>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-semibold text-slate-800">{college.short}</h2>
              <Badge variant="green" dot className="hidden sm:inline-flex">Online</Badge>
            </div>
            <p className="text-xs text-slate-400 truncate max-w-xs">{college.name}</p>
          </div>
        </div>

        <div className="flex items-center gap-1">
          {messages.length > 0 && (
            <ShimmerButton variant="ghost" size="sm" onClick={() => setShowSuggestions(v => !v)}>
              <Lightbulb className="h-3.5 w-3.5" />
              <span className="hidden sm:inline">{showSuggestions ? 'Hide' : 'Ideas'}</span>
            </ShimmerButton>
          )}
          {messages.length > 0 && (
            <ShimmerButton variant="ghost" size="sm" onClick={onClearHistory}>
              <Trash2 className="h-3.5 w-3.5" />
              <span className="hidden sm:inline">Clear</span>
            </ShimmerButton>
          )}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6 relative">
        {messages.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            className="h-full flex flex-col items-center justify-center max-w-lg mx-auto text-center space-y-6"
          >
            <div className="space-y-1.5">
              <h3 className="font-display text-lg font-semibold text-slate-800">What can I help you with?</h3>
              <p className="text-sm text-slate-500">
                Ask about academics, events, contacts, or campus life.
              </p>
            </div>

            <div className="w-full space-y-2">
              <p className="text-xs text-slate-400 font-medium">Try asking</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {SUGGESTIONS.map((s, i) => (
                  <motion.button
                    key={i}
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.05 }}
                    onClick={() => setInput(s.text)}
                    className="flex items-center gap-2 px-3 py-2.5 rounded-lg bg-white hover:bg-blue-50 border border-slate-200 hover:border-blue-200 text-left text-xs text-slate-600 hover:text-slate-900 transition-all duration-150 group"
                  >
                    <span className="text-sm flex-shrink-0">{s.icon}</span>
                    <span className="flex-1 truncate">{s.text}</span>
                    <ChevronRight className="h-3 w-3 text-slate-300 group-hover:text-brand-blue transition-colors flex-shrink-0" />
                  </motion.button>
                ))}
              </div>
            </div>
          </motion.div>
        ) : (
          <div className="max-w-2xl mx-auto space-y-4">
            <AnimatePresence initial={false}>
              {messages.map((msg) => {
                const isBot = msg.role === 'assistant';
                return (
                  <motion.div
                    key={msg.id}
                    initial={{ opacity: 0, y: 12 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
                    className={cn('flex gap-2.5', isBot ? '' : 'flex-row-reverse')}
                  >
                    {/* Avatar */}
                    <div className={cn(
                      'w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5',
                      isBot ? 'bg-brand-blue' : 'bg-slate-700'
                    )}>
                      {isBot ? <Bot className="h-3 w-3 text-white" /> : <User className="h-3 w-3 text-white" />}
                    </div>

                    {/* Bubble */}
                    <div className="max-w-[80%] space-y-1">
                      <div className={cn(
                        'relative group px-3.5 py-2.5 rounded-xl text-sm leading-relaxed',
                        isBot
                          ? 'bg-white text-slate-700 border border-slate-100'
                          : 'bg-brand-blue text-white'
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
                          <div className="mt-2 pt-2 border-t border-slate-100 flex flex-wrap gap-1.5">
                            {msg.toolUsed && (
                              <BlueprintStat label="TOOL" value={msg.toolUsed} />
                            )}
                            {msg.responseTimeMs !== undefined && (
                              <BlueprintStat label="TIME" value={`${msg.responseTimeMs}ms`} />
                            )}
                          </div>
                        )}

                        {/* Hover actions */}
                        <div className={cn(
                          'absolute top-1.5 opacity-0 group-hover:opacity-100 transition-opacity duration-150',
                          isBot ? 'right-1.5' : 'left-1.5'
                        )}>
                          <div className="flex items-center gap-0.5 bg-white rounded-md p-1 border border-slate-200 shadow-sm">
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
                            <Check className="h-2.5 w-2.5" /> Logged
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
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex gap-2.5"
              >
                <div className="w-6 h-6 rounded-full bg-brand-blue flex items-center justify-center flex-shrink-0">
                  <Bot className="h-3 w-3 text-white" />
                </div>
                <div className="bg-white border border-slate-100 px-3.5 py-2.5 rounded-xl flex items-center gap-2.5">
                  <div className="flex gap-1">
                    {[0, 1, 2].map(i => (
                      <motion.div
                        key={i}
                        animate={{ y: [0, -4, 0] }}
                        transition={{ duration: 0.6, repeat: Infinity, delay: i * 0.12 }}
                        className="w-1.5 h-1.5 rounded-full bg-brand-blue"
                      />
                    ))}
                  </div>
                  <span className="text-xs text-slate-500">Searching campus data…</span>
                </div>
              </motion.div>
            )}
            <div ref={endRef} />
          </div>
        )}

        {/* Collapsible suggestions */}
        {messages.length > 0 && showSuggestions && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="max-w-2xl mx-auto space-y-2 pt-3 pb-4"
          >
            <p className="text-xs text-slate-400 font-medium px-1">Try asking</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {SUGGESTIONS.map((s, i) => (
                <button
                  key={i}
                  onClick={() => { setInput(s.text); setShowSuggestions(false); }}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg bg-white hover:bg-blue-50 border border-slate-200 hover:border-blue-200 text-left text-xs text-slate-600 hover:text-slate-900 transition-all duration-150"
                >
                  <span className="text-sm flex-shrink-0">{s.icon}</span>
                  <span className="flex-1 truncate">{s.text}</span>
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </div>

      {/* Input Area */}
      <div className="flex-shrink-0 px-4 pb-4">
        <div className="max-w-2xl mx-auto">
          <div className="bg-white rounded-xl border border-slate-200 overflow-hidden focus-within:border-brand-blue focus-within:ring-1 focus-within:ring-brand-blue/20 transition-all duration-150">
            <textarea
              ref={inputRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={`Ask about ${college.short}…`}
              aria-label={`Ask ${college.short} AI assistant a question`}
              rows={1}
              disabled={loading}
              className="w-full bg-transparent text-sm text-slate-900 placeholder-slate-400 px-4 pt-3 pb-1 focus:outline-none resize-none disabled:opacity-50 max-h-32 overflow-y-auto"
              style={{ lineHeight: '1.6' }}
            />
            <div className="flex items-center justify-between px-3 pb-2.5 pt-0.5">
              <span className="text-2xs text-slate-400">
                <AlertCircle className="h-3 w-3 inline mr-1" />
                {college.short}
              </span>
              <ShimmerButton
                onClick={handleSend}
                disabled={!input.trim() || loading}
                size="sm"
                aria-label="Send message"
              >
                <Send className="h-3.5 w-3.5" />
              </ShimmerButton>
            </div>
          </div>
          <p className="text-2xs text-slate-400 text-center mt-2">
            Enter to send · Shift+Enter for new line
          </p>
        </div>
      </div>
    </div>
  );
};
