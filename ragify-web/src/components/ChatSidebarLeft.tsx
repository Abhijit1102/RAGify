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

interface ChatSidebarLeftProps {
  selectedSessionId?: number;
  onSelectSession: (id: number) => void;
}

export default function ChatSidebarLeft({ selectedSessionId, onSelectSession }: ChatSidebarLeftProps) {
  const [isOpen, setIsOpen] = useState(true);
  const [sessions, setSessions] = useState<ChatSession[]>([]);

  const fetchSessions = async () => {
    try {
      const res = await api.get("/chat/sessions");
      setSessions(res.data);
    } catch (err) {
      console.error(err);
      toast.error("Failed to fetch chat sessions");
    }
  };

  useEffect(() => {
    if (isOpen) fetchSessions();
  }, [isOpen]);

  const handleNewChat = async () => {
    try {
      // Create new empty session by sending a placeholder message
      const res = await api.post("/chat/messages/", { content: " " });
      const newSessionId = res.data.session_id;
      toast.success("New chat started!");
      fetchSessions();
      onSelectSession(newSessionId);
    } catch (err) {
      console.error(err);
      toast.error("Failed to start new chat");
    }
  };

  return (
    <>
      <div className={`fixed top-0 left-0 h-full z-40 flex flex-col transition-all duration-300 overflow-hidden ${isOpen ? "w-80" : "w-0"}`}>
        <div className="bg-white h-full border-r border-gray-300 shadow-lg p-6 flex-1 overflow-y-auto">
          {isOpen && (
            <>
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold">Chat Sessions</h2>
                <button onClick={() => setIsOpen(false)} className="text-gray-600 hover:text-black text-lg font-bold">✖</button>
              </div>

              <button onClick={handleNewChat} className="w-full bg-green-500 hover:bg-green-600 text-white p-2 rounded mb-4">
                + Start New Chat
              </button>

              <ul className="flex flex-col gap-2">
                {sessions.map((session) => (
                  <li key={session.id}
                      className={`p-2 rounded cursor-pointer ${selectedSessionId === session.id ? "bg-blue-200 font-semibold" : "hover:bg-gray-100"}`}
                      onClick={() => onSelectSession(session.id)}>
                    {session.session_name || `Session ${session.id}`}
                    <div className="text-xs text-gray-500">{new Date(session.created_at).toLocaleString()}</div>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      </div>

      {!isOpen && (
        <button onClick={() => setIsOpen(true)}
                className="fixed top-4 left-4 bg-blue-500 hover:bg-blue-600 text-white p-2 rounded shadow-lg z-50">
          <PanelRightOpen size={20} />
        </button>
      )}
    </>
  );
}
