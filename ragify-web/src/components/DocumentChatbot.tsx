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

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (!sessionId) return;

    setMessages([]); // clear UI for new session

    const fetchMessages = async () => {
      try {
        const res = await api.get(`/chat/${sessionId}/messages`);
        const fetchedMessages = res.data.map((msg: any) => ({
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
  }, [sessionId]);

  const handleSend = async () => {
    if (!query.trim() || !sessionId) return;

    setMessages((prev) => [...prev, { type: "user", content: query }]);
    setLoading(true);

    try {
      const res = await api.post("/chat/messages/", { content: query, session_id: sessionId });
      const data = res.data;

      if (data) {
        setMessages((prev) => [
          ...prev,
          { type: "bot", content: data.content },
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
    <div className="flex flex-col justify-center items-center w-full h-screen p-4 bg-gray-50">
      <div className="flex flex-col w-full max-w-7xl h-[80vh] bg-white rounded shadow-lg p-4">
        <div className="flex-1 flex flex-col gap-2 overflow-y-auto mb-4 px-2">
          {messages.map((msg, idx) => (
            <div key={idx}
                 className={`p-2 rounded max-w-[70%] whitespace-pre-wrap ${msg.type === "user" ? "bg-blue-100 self-end text-right" : "bg-gray-200 self-start text-left"}`}>
              {msg.type === "bot" && (msg.fileName || msg.pageNumber || msg.score) ? (
                <div className="flex flex-col gap-1">
                  <span className="font-medium">{msg.content}</span>
                  {msg.fileName && <span className="text-xs text-gray-500">File: {msg.fileName}</span>}
                  {msg.pageNumber !== undefined && <span className="text-xs text-gray-500">Page: {msg.pageNumber}</span>}
                  {msg.score !== undefined && <span className="text-xs text-gray-500">Score: {msg.score.toFixed(3)}</span>}
                </div>
              ) : (
                msg.content
              )}
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

        <div className="flex gap-2">
          <Input
            placeholder="Ask about your documents..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            disabled={loading || !sessionId}
            className="flex-1"
          />
          <Button onClick={handleSend} disabled={loading || !sessionId}>
            {loading ? "Searching..." : "Send"}
          </Button>
        </div>
      </div>
    </div>
  );
}
