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

  if (!user) return <div className="flex justify-center items-center h-screen text-gray-500">Loading...</div>;

  return (
    <div className="flex flex-col w-full h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-md p-4 flex justify-center items-center border-b border-gray-200 relative">
        {/* Title centered */}
        <h1 className="text-2xl font-bold text-gray-800">📚 AI Document Chat</h1>

        {/* User info on the right */}
        <div className="absolute right-4 flex items-center gap-4">
          <span className="text-gray-600">Hello, <strong>{user.username}</strong> 👋</span>
          <span className="px-2 py-1 text-xs rounded bg-blue-100 text-blue-800">{user.role}</span>
        </div>
      </header>


      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar: Chat Sessions */}
        <ChatSidebarLeft
          selectedSessionId={selectedSessionId}
          onSelectSession={(id) => setSelectedSessionId(id)}
        />

        {/* Center: Chat Messages */}
        <main className="flex-1 overflow-hidden">
          <DocumentChatbot sessionId={selectedSessionId} />
        </main>

        {/* Right Sidebar: User info / documents */}
        <Rightbar
          user={user}
          refreshDocs={refreshDocs}
          setRefreshDocs={setRefreshDocs}
        />
      </div>
    </div>
  );
}
