"use client";

import { useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import DocumentUploader from "@/components/DocumentUploader";
import DocumentList from "@/components/DocumentList";
import { PanelRightOpen } from "lucide-react";

interface User {
  username: string;
  role: string;
}

interface RightbarProps {
  user: User;
  refreshDocs: boolean;
  setRefreshDocs: React.Dispatch<React.SetStateAction<boolean>>;
}

export default function Rightbar({ user, refreshDocs, setRefreshDocs }: RightbarProps) {
  const [isOpen, setIsOpen] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem("token");
    toast("Logged out successfully");
    window.location.href = "/auth/login";
  };

  return (
    <>
      <div
        className={`fixed top-0 right-0 h-full z-40 flex flex-col transition-all duration-300 ${
          isOpen ? "w-96" : "w-0"
        }`}
      >
        <div className="bg-gray-800 h-full flex flex-col shadow-lg text-white">
          {isOpen && (
            <>
              <div className="flex-1 overflow-y-auto p-6">
                <div className="mb-6 flex justify-between items-center">
                  <div>
                    <h2 className="text-xl font-bold">Welcome, {user.username} 👋</h2>
                    <p className="text-sm text-gray-400">Role: {user.role}</p>
                  </div>
                  <button
                    onClick={() => setIsOpen(false)}
                    className="text-gray-300 hover:text-white text-lg font-bold"
                  >
                    ✖
                  </button>
                </div>

                <div className="mb-8">
                  <h3 className="text-lg font-semibold mb-2">Upload Document</h3>
                  <DocumentUploader
                    onUploadSuccess={() => setRefreshDocs((prev) => !prev)}
                  />
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-2">Your Documents</h3>
                  <DocumentList refreshTrigger={refreshDocs} />
                </div>
              </div>

              <div className="p-6 flex justify-center border-t border-gray-700">
                <Button
                  onClick={handleLogout}
                  variant="destructive"
                  className="bg-red-600 hover:bg-red-700 text-white"
                >
                  Logout
                </Button>
              </div>
            </>
          )}
        </div>
      </div>

      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed top-4 right-4 bg-blue-600 hover:bg-blue-700 text-white p-2 rounded shadow-lg z-50"
        >
          <PanelRightOpen size={20} />
        </button>
      )}
    </>
  );
}
