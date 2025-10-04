import { useState, useEffect } from "react";
import { api } from "../api/api";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
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
      setDocuments(res.data);
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
      await api.delete(`/documents/${id}`);
      setDocuments((prev) => prev.filter((doc) => doc.id !== id));
      toast.success("Document deleted successfully");
    } catch (err) {
      console.error(err);
      toast.error("Failed to delete document");
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, [refreshTrigger]);

  if (loading) return <div>Loading documents...</div>;
  if (!documents.length) return <div>No documents uploaded yet.</div>;

  return (
    <div className="grid gap-4">
      {documents.map((doc) => (
        <Card key={doc.id} className="border shadow-sm">
          <CardHeader>
            <CardTitle>{doc.file_name}</CardTitle>
          </CardHeader>
          <CardContent>
            <a 
              href={doc.url} 
              download={doc.file_name}   // <-- forces download
              className="text-blue-600 underline"
            >
              Download Document
            </a>
          </CardContent>
          <CardFooter>
            <Button variant="destructive" onClick={() => handleDelete(doc.id)}>
              Delete
            </Button>
          </CardFooter>
        </Card>
      ))}
    </div>
  );
};

export default DocumentList;
