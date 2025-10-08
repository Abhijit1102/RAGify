"use client";

import { useState, useEffect } from "react";
import { api } from "@/api/api";
import { toast } from "sonner";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import DashboardCard from "@/components/DashboardCard";
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";

interface PerUserStats {
  username: string;
  documents: number;
  chat_sessions: number;
  chat_messages: number;
}

interface AnalyticsData {
  users: { total: number; admins: number; regular_users: number };
  per_user_stats: PerUserStats[];
  documents: { total: number };
  chat: { total_sessions: number; total_messages: number };
  chunks: { total: number };
}

export default function AdminAnalyticsPage() {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const res = await api.get("/admin/analytics/");
        setData(res.data.data); // using api_response format
      } catch (err) {
        console.error(err);
        toast.error("Failed to load analytics");
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading)
    return <p className="text-center mt-20 text-gray-400">Loading analytics...</p>;
  if (!data)
    return <p className="text-center mt-20 text-red-500">No data available</p>;

  return (
    <div className="p-6 bg-gray-900 min-h-screen flex flex-col items-center text-white">
      <h1 className="text-4xl font-bold mb-8 text-center">Admin Analytics Dashboard</h1>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12 w-full max-w-7xl">
        <DashboardCard title="Total Users" value={data.users.total} description="All users" />
        <DashboardCard title="Admins" value={data.users.admins} description="Admin users" />
        <DashboardCard title="Regular Users" value={data.users.regular_users} description="Normal users" />
        <DashboardCard title="Total Documents" value={data.documents.total} description="Uploaded documents" />
        <DashboardCard title="Total Chat Sessions" value={data.chat.total_sessions} description="All chat sessions" />
        <DashboardCard title="Total Chat Messages" value={data.chat.total_messages} description="All chat messages" />
        <DashboardCard title="Total Chunks" value={data.chunks.total} description="All document chunks" />
      </div>

      {/* Tabs for per-user stats */}
      <div className="w-full max-w-7xl">
        <Tabs defaultValue="perUser">
          <TabsList className="mb-6 flex justify-center border-b border-gray-700">
            <TabsTrigger
              value="perUser"
              className="text-gray-200 data-[state=active]:text-white data-[state=active]:bg-gray-800 rounded-lg px-8 py-3 text-lg font-semibold hover:bg-gray-700 transition-colors"
            >
              Per User Stats
            </TabsTrigger>
          </TabsList>


          <TabsContent value="perUser">
            <ScrollArea className="h-[60vh] bg-gray-800 rounded p-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {data.per_user_stats.map((user) => (
                  <Card
                    key={user.username}
                    className="border border-gray-600 bg-gray-700 text-white hover:shadow-lg transition-shadow"
                  >
                    <CardHeader>
                      <CardTitle>{user.username}</CardTitle>
                      <CardDescription className="text-gray-300 text-xs">
                        User activity overview
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="grid grid-cols-2 gap-2">
                      <div className="flex flex-col items-center p-2 bg-blue-900 rounded">
                        <p className="text-xl font-bold">{user.documents}</p>
                        <p className="text-sm text-gray-200">Documents</p>
                      </div>
                      <div className="flex flex-col items-center p-2 bg-green-900 rounded">
                        <p className="text-xl font-bold">{user.chat_sessions}</p>
                        <p className="text-sm text-gray-200">Chat Sessions</p>
                      </div>
                      <div className="flex flex-col items-center p-2 bg-yellow-900 rounded col-span-2">
                        <p className="text-xl font-bold">{user.chat_messages}</p>
                        <p className="text-sm text-gray-200">Chat Messages</p>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </ScrollArea>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
