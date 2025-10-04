import { useEffect, useState } from "react";
import type { ReactNode } from "react";

import { Navigate } from "react-router-dom";
import { api } from "../api/api";

interface Props {
  children: ReactNode;
}

const ProtectedRoute = ({ children }: Props) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        setIsAuthenticated(false);
        return;
      }

      try {
        await api.get("/auth/user"); // verify token
        setIsAuthenticated(true);
      } catch (err) {
        localStorage.removeItem("token"); // clear invalid token
        setIsAuthenticated(false);
      }
    };

    checkAuth();
  }, []);

  if (isAuthenticated === null) return <div>Loading...</div>;

  if (!isAuthenticated) return <Navigate to="/auth/login" replace />;

  return <>{children}</>;
};

export default ProtectedRoute;
