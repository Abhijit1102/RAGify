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
      {/* Sidebar */}
      <div
        className={`fixed top-0 right-0 h-full z-40 flex flex-col transition-all duration-300 ${
          isOpen ? "w-96" : "w-0"
        }`}
      >
        <div className="bg-white h-full border-l border-gray-300 shadow-lg flex flex-col">
          {isOpen && (
            <>
              {/* Scrollable content */}
              <div className="flex-1 overflow-y-auto p-6">
                {/* Header */}
                <div className="mb-6 flex justify-between items-center">
                  <div>
                    <h2 className="text-xl font-bold">Welcome, {user.username} 👋</h2>
                    <p className="text-sm text-gray-600">Role: {user.role}</p>
                  </div>
                  <button
                    onClick={() => setIsOpen(false)}
                    className="text-gray-600 hover:text-black text-lg font-bold"
                  >
                    ✖
                  </button>
                </div>

                {/* Upload Document */}
                <div className="mb-8">
                  <h3 className="text-lg font-semibold mb-2">Upload Document</h3>
                  <DocumentUploader
                    onUploadSuccess={() => {
                      toast.success("Document uploaded successfully");
                      setRefreshDocs((prev) => !prev);
                    }}
                  />
                </div>

                {/* Documents List */}
                <div>
                  <h3 className="text-lg font-semibold mb-2">Your Documents</h3>
                  <DocumentList refreshTrigger={refreshDocs} />
                </div>
              </div>

              {/* Logout Button at bottom */}
              <div className="p-6 flex justify-center border-t border-gray-200">
                <Button onClick={handleLogout} variant="destructive">
                  Logout
                </Button>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Floating toggle button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed top-4 right-4 bg-[#FF4B4B] hover:bg-[#e64545] text-white p-2 rounded shadow-lg z-50"
        >
          <PanelRightOpen size={20} />
        </button>
      )}
    </>
  );
}
