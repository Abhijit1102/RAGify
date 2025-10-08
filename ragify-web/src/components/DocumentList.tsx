"use client";

import { useState, useEffect } from "react";
import { api } from "../api/api";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

interface UploadedFile {
  id: number;
  file_name: string;
  url: string;
}

interface DocumentListProps {
  refreshTrigger?: boolean;
}

const DocumentList = ({ refreshTrigger }: DocumentListProps) => {
  const [documents, setDocuments] = useState<UploadedFile[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchDocuments = async () => {
    setLoading(true);
    try {
      const res = await api.get("/documents/");
      setDocuments(res.data.data || []);
    } catch (err) {
      console.error(err);
      toast.error("Failed to fetch documents");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this document?")) return;

    try {
      const res = await api.delete(`/documents/${id}`);
      if (res.data.status === "success") {
        setDocuments((prev) => prev.filter((doc) => doc.id !== id));
        toast.success("Document deleted successfully");
      } else {
        toast.error(res.data.message || "Failed to delete document");
      }
    } catch (err) {
      console.error(err);
      toast.error("Failed to delete document");
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, [refreshTrigger]);

  if (loading) return <div className="text-white">Loading documents...</div>;
  if (!documents.length) return <div className="text-gray-400">No documents uploaded yet.</div>;

  return (
    <div className="flex flex-col gap-2">
      {documents.map((doc) => (
        <div
          key={doc.id}
          className="flex justify-between items-center p-2 border border-gray-700 rounded hover:bg-gray-700"
        >
          <a
            href={doc.url}
            download={doc.file_name}
            className="text-blue-400 underline truncate max-w-xs"
            title={doc.file_name}
          >
            {doc.file_name}
          </a>
          <Button
            variant="destructive"
            size="sm"
            onClick={() => handleDelete(doc.id)}
            className="bg-red-600 hover:bg-red-700 text-white"
          >
            Delete
          </Button>
        </div>
      ))}
    </div>
  );
};

export default DocumentList;
