"use client";

import { useState, useEffect, useRef } from "react";
import { api } from "../api/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";

interface ChatMessage {
  type: "user" | "bot";
  content: string;
  fileName?: string;
  pageNumber?: number;
  score?: number;
}

interface DocumentChatbotProps {
  sessionId?: number;
}

export default function DocumentChatbot({ sessionId }: DocumentChatbotProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement | null>(null);
  const [currentSessionId, setCurrentSessionId] = useState<number | undefined>(sessionId);

  // Sync when new session selected
  useEffect(() => {
    setCurrentSessionId(sessionId);
  }, [sessionId]);

  // Scroll to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Fetch messages when session changes
  useEffect(() => {
    if (!currentSessionId) return;

    setMessages([]);
    const fetchMessages = async () => {
      try {
        const res = await api.get(`/chat/${currentSessionId}/messages`);
        const fetchedMessages = res.data.data.map((msg: any) => ({
          type: msg.role === "user" ? "user" : "bot",
          content: msg.content,
          fileName: msg.file_name,
          pageNumber: msg.page_number,
          score: msg.score,
        }));
        setMessages(fetchedMessages);
      } catch (err) {
        console.error(err);
        toast.error("Failed to load chat messages");
      }
    };
    fetchMessages();
  }, [currentSessionId]);

  // Send new message
  const handleSend = async () => {
    if (!query.trim()) return;
    setMessages((prev) => [...prev, { type: "user", content: query }]);
    setLoading(true);

    try {
      const res = await api.post("/search/", {
        query,
        session_name: currentSessionId ? `Session ${currentSessionId}` : undefined,
      });

      const botMsg = res.data.data?.[0];
      const sessionIdFromApi = res.data.session_id;

      if (sessionIdFromApi && !currentSessionId) {
        setCurrentSessionId(sessionIdFromApi);
      }

      if (botMsg) {
        setMessages((prev) => [
          ...prev,
          {
            type: "bot",
            content: botMsg.text || botMsg.content || "No relevant documents found.",
            fileName: botMsg.file_name,
            pageNumber: botMsg.page_number,
            score: botMsg.score,
          },
        ]);
      }
    } catch (err) {
      console.error(err);
      toast.error("Failed to send message");
    } finally {
      setQuery("");
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col justify-center items-center w-full min-h-screen p-6 bg-gray-900 text-white">
      <div className="flex flex-col w-full max-w-7xl h-[80vh] bg-gray-800 rounded-lg shadow-lg p-4">
        {/* Chat messages */}
        <div className="flex-1 flex flex-col gap-2 overflow-y-auto mb-4 px-2">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`p-3 rounded max-w-[70%] whitespace-pre-wrap break-words ${
                msg.type === "user"
                  ? "bg-white text-black self-end text-right"
                  : "bg-gray-700 text-white self-start text-left"
              }`}
            >
              {msg.type === "bot" && (msg.fileName || msg.pageNumber || msg.score) ? (
                <div className="flex flex-col gap-1">
                  <span className="font-medium">{msg.content}</span>
                  {msg.fileName && <span className="text-xs text-gray-300">File: {msg.fileName}</span>}
                  {msg.pageNumber !== undefined && (
                    <span className="text-xs text-gray-300">Page: {msg.pageNumber}</span>
                  )}
                  {msg.score !== undefined && (
                    <span className="text-xs text-gray-300">Score: {msg.score.toFixed(3)}</span>
                  )}
                </div>
              ) : (
                msg.content
              )}
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

        {/* Input area */}
        <div className="flex gap-2 mt-auto">
          <Input
            placeholder="Ask about your documents..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            disabled={loading}
            className="flex-1 bg-white text-black placeholder-gray-500 rounded border border-gray-400 focus:ring focus:ring-blue-400 focus:border-blue-500"
          />
          <Button
            onClick={handleSend}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold"
          >
            {loading ? "Sending..." : "Send"}
          </Button>
        </div>
      </div>
    </div>
  );
}
