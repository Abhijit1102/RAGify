"use client";

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { api } from "../api/api";

import ChatSidebarLeft from "@/components/ChatSidebarLeft";
import DocumentChatbot from "@/components/DocumentChatbot";
import Rightbar from "@/components/Rightbar";

interface User {
  username: string;
  role: string;
}

export default function Home() {
  const [user, setUser] = useState<User | null>(null);
  const [selectedSessionId, setSelectedSessionId] = useState<number | undefined>();
  const [refreshDocs, setRefreshDocs] = useState(false);
  const navigate = useNavigate();

  // Fetch logged-in user
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await api.get("/auth/user");
        setUser(res.data.data);
      } catch (err) {
        toast.error("Please log in");
        navigate("/auth/login");
      }
    };
    fetchUser();
  }, [navigate]);

  if (!user)
    return (
      <div className="flex justify-center items-center h-screen text-gray-500">
        Loading...
      </div>
    );

  return (
    <div className="flex flex-col w-full h-screen bg-gray-50">
      {/* Header aligned like table */}
      <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        {/* Left spacer (optional, like table first column) */}
        <div className="flex-1"></div>

        {/* Centered title */}
        <h1 className="text-lg font-semibold text-gray-800 text-center flex-1">
          📚 AI Document Chat
        </h1>

        {/* Right user info (like table last column) */}
        <div className="flex items-center gap-4 flex-1 justify-end">
          <span className="text-gray-600 text-sm">
            Hello, <strong>{user.username}</strong> 👋
          </span>
          <span className="px-2 py-1 text-xs rounded bg-blue-100 text-blue-800">
            {user.role}
          </span>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar */}
        <ChatSidebarLeft
          selectedSessionId={selectedSessionId}
          onSelectSession={(id) => setSelectedSessionId(id)}
          darkMode={true} // optional
        />

        {/* Center Chat */}
        <main className="flex-1 overflow-auto p-6">
          <DocumentChatbot sessionId={selectedSessionId} />
        </main>

        {/* Right Sidebar */}
        <Rightbar
          user={user}
          refreshDocs={refreshDocs}
          setRefreshDocs={setRefreshDocs}
        />
      </div>
    </div>
  );
}
