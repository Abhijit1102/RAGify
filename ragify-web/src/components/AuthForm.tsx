"use client";

import { useState } from "react";
import { api } from "../api/api";
import { useNavigate, Link } from "react-router-dom";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

interface Props {
  type: "login" | "register";
}

const AuthForm = ({ type }: Props) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await api.post(`/auth/${type}`, { username, password });

      toast.success(res.data.message);

      if (type === "login") {
        if (res.data?.data?.token) {
          localStorage.setItem("token", res.data.data.token);
        }
        navigate("/");
      } else {
        navigate("/auth/login");
      }

      setUsername("");
      setPassword("");
    } catch (err: any) {
      toast.error(err.response?.data?.message || "Error occurred");
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-900">
      <Card className="w-[380px] bg-gray-800 text-white shadow-xl hover:shadow-2xl transition-shadow duration-300">
        <CardHeader>
          <CardTitle className="text-center text-2xl font-bold">
            {type === "login" ? "Login" : "Register"}
          </CardTitle>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="flex flex-col gap-6"> {/* increased gap from 4 → 6 */}
            <Input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="bg-gray-700 text-white placeholder-gray-400 focus:ring-blue-500"
            />
            <Input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="bg-gray-700 text-white placeholder-gray-400 focus:ring-blue-500"
            />
          </CardContent>
          <CardFooter className="flex flex-col gap-4 mt-2"> {/* added mt-2 for extra spacing */}
            <Button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2"
            >
              {type === "login" ? "Login" : "Register"}
            </Button>
            <p className="text-sm text-center text-gray-400">
              {type === "login" ? (
                <>
                  Don’t have an account?{" "}
                  <Link to="/auth/register" className="text-blue-400 hover:underline">
                    Register
                  </Link>
                </>
              ) : (
                <>
                  Already have an account?{" "}
                  <Link to="/auth/login" className="text-blue-400 hover:underline">
                    Login
                  </Link>
                </>
              )}
            </p>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
};

export default AuthForm;
