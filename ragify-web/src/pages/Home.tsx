"use client";

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/api";
import Rightbar from "@/components/Rightbar";

interface User {
  username: string;
  role: string;
}

export default function Home() {
  const [user, setUser] = useState<User | null>(null);
  const [refreshDocs, setRefreshDocs] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await api.get("/auth/user");
        setUser(res.data.data);
      } catch {
        navigate("/auth/login");
      }
    };
    fetchUser();
  }, [navigate]);

  if (!user) return <div>Loading...</div>;

  return (
    <div className="p-10">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      <p>Welcome to your dashboard, {user.username}!</p>

      {/* Rightbar handles its own toggle */}
      <Rightbar user={user} refreshDocs={refreshDocs} setRefreshDocs={setRefreshDocs} />
    </div>
  );
}
