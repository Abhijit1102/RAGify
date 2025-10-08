"use client";

import { useState, useEffect } from "react";
import { toast } from "sonner";
import { PanelRightOpen } from "lucide-react";
import { api } from "../api/api";

interface ChatSession {
  id: number;
  session_name: string | null;
  created_at: string;
}

// Props for Sidebar
interface ChatSidebarLeftProps {
  selectedSessionId?: number;
  onSelectSession: (id: number) => void;
  darkMode?: boolean;
}

export default function ChatSidebarLeft({
  selectedSessionId,
  onSelectSession,
  darkMode = false,
}: ChatSidebarLeftProps) {
  const [isOpen, setIsOpen] = useState(true);
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [loading, setLoading] = useState(false);

  // Fetch chat sessions
  const fetchSessions = async () => {
    setLoading(true);
    try {
      const res = await api.get("/chat/sessions");
      // Handle api_response format: data is under res.data.data
      const data = res.data.data || [];
      setSessions(data);
    } catch (err) {
      console.error(err);
      toast.error("Failed to fetch chat sessions");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) fetchSessions();
  }, [isOpen]);

  // Start a new chat session
  const handleNewChat = async () => {
    try {
      // Create new session via empty message
      const res = await api.post("/chat/messages/", { content: "New session" });
      const newSessionId = res.data.extra?.session_id || res.data.data?.id;

      if (!newSessionId) {
        toast.error("Failed to create new session");
        return;
      }

      toast.success("New chat started!");
      await fetchSessions();
      onSelectSession(newSessionId);
    } catch (err) {
      console.error(err);
      toast.error("Failed to start new chat");
    }
  };

  return (
    <>
      {/* Sidebar */}
      <div
        className={`fixed top-0 left-0 h-full z-40 flex flex-col transition-all duration-300 overflow-hidden ${
          isOpen ? "w-80" : "w-0"
        }`}
      >
        <div
          className={`h-full shadow-lg p-6 flex-1 overflow-y-auto ${
            darkMode ? "bg-gray-900 text-white" : "bg-gray-100 text-gray-900"
          }`}
        >
          {isOpen && (
            <>
              {/* Header */}
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold">Chat Sessions</h2>
                <button
                  onClick={() => setIsOpen(false)}
                  className={`text-lg font-bold ${
                    darkMode ? "text-gray-400 hover:text-white" : "text-gray-700 hover:text-black"
                  }`}
                >
                  ✖
                </button>
              </div>

              {/* New Chat Button */}
              <button
                onClick={handleNewChat}
                disabled={loading}
                className={`w-full p-2 rounded mb-4 font-semibold transition-colors ${
                  darkMode
                    ? "bg-blue-700 hover:bg-blue-800 text-white"
                    : "bg-blue-400 hover:bg-blue-500 text-black"
                }`}
              >
                {loading ? "Loading..." : "+ Start New Chat"}
              </button>

              {/* Chat Sessions List */}
              <ul className="flex flex-col gap-2">
                {sessions.map((session) => (
                  <li
                    key={session.id}
                    className={`p-2 rounded cursor-pointer transition-colors ${
                      selectedSessionId === session.id
                        ? darkMode
                          ? "bg-blue-800 font-semibold"
                          : "bg-blue-300 font-semibold"
                        : darkMode
                        ? "hover:bg-gray-700"
                        : "hover:bg-gray-200"
                    }`}
                    onClick={() => onSelectSession(session.id)}
                  >
                    <div>{session.session_name || `Session ${session.id}`}</div>
                    <div className={`text-xs ${darkMode ? "text-gray-400" : "text-gray-600"}`}>
                      {new Date(session.created_at).toLocaleString()}
                    </div>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      </div>

      {/* Toggle Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className={`fixed top-4 left-4 p-2 rounded shadow-lg z-50 transition-colors ${
            darkMode
              ? "bg-blue-700 hover:bg-blue-800 text-white"
              : "bg-blue-400 hover:bg-blue-500 text-black"
          }`}
        >
          <PanelRightOpen size={20} />
        </button>
      )}
    </>
  );
}
