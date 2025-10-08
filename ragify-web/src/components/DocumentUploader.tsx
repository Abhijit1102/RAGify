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

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      toast.error("Please select a file to upload");
      return;
    }

    setUploading(true);
    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch("http://localhost:8000/api/v1/documents/upload/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => null);
        throw new Error(errData?.message || "Upload failed");
      }

      const data = await response.json();
      onUploadSuccess?.({
        file_name: data.data.file_name,
        url: data.data.url,
      });

      toast.success("File uploaded successfully!");
      setSelectedFile(null);
    } catch (err: any) {
      console.error(err);
      toast.error(err.message || "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="flex flex-col gap-2 w-full p-4 border border-gray-700 rounded bg-gray-800 text-white">
      <label className="flex items-center justify-center p-2 border border-gray-600 rounded cursor-pointer hover:bg-gray-700">
        <span>{selectedFile ? selectedFile.name : "Choose File"}</span>
        <input
          type="file"
          onChange={handleFileChange}
          disabled={uploading}
          className="hidden"
          accept=".pdf,.doc,.docx,.txt"
        />
      </label>

      {selectedFile && (
        <p className="text-sm text-gray-400">Selected: {selectedFile.name}</p>
      )}

      <Button
        onClick={handleUpload}
        disabled={uploading || !selectedFile}
        className="bg-blue-600 hover:bg-blue-700 text-white"
      >
        {uploading ? "Uploading..." : "Upload"}
      </Button>
  </div>
  );
};

export default DocumentUploader;
