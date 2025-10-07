"use client";

import { useState, type ChangeEvent } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";

interface UploadedFile {
  file_name: string;
  url: string;
}

interface DocumentUploaderProps {
  onUploadSuccess?: (file: UploadedFile) => void;
}

const DocumentUploader: React.FC<DocumentUploaderProps> = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  // Handle file selection
  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  // Upload file to FastAPI
  const handleUpload = async () => {
    if (!selectedFile) {
      toast.error("Please select a file to upload");
      return;
    }

    setUploading(true);
    try {
      const formData = new FormData();
      formData.append("file", selectedFile); // ✅ Must match FastAPI parameter

      const response = await fetch("http://localhost:8000/api/v1/documents/upload/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          // Do NOT set Content-Type; browser sets it automatically for FormData
        },
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => null);
        throw new Error(errData?.message || "Upload failed");
      }

      const data = await response.json();
      const uploadedFile: UploadedFile = {
        file_name: data.data.file_name,
        url: data.data.url,
      };

      toast.success("File uploaded successfully!");
      onUploadSuccess?.(uploadedFile);
      setSelectedFile(null);
    } catch (err: any) {
      console.error(err);
      toast.error(err.message || "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="flex flex-col gap-2 w-full max-w-md mx-auto p-4 border rounded shadow-md">
      <Input
        type="file"
        onChange={handleFileChange}
        disabled={uploading}
        accept=".pdf,.doc,.docx,.txt" // optional: restrict file types
      />
      {selectedFile && (
        <p className="text-sm text-gray-500">Selected: {selectedFile.name}</p>
      )}
      <Button onClick={handleUpload} disabled={uploading || !selectedFile}>
        {uploading ? "Uploading..." : "Upload"}
      </Button>
    </div>
  );
};

export default DocumentUploader;
