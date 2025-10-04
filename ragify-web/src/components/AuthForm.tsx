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
        // Save token after login
        if (res.data?.data?.token) {
          localStorage.setItem("token", res.data.data.token);
        }
        navigate("/"); // redirect to home
      } else if (type === "register") {
        // Redirect to login page after registration
        navigate("/auth/login");
      }

      // Reset form fields
      setUsername("");
      setPassword("");

    } catch (err: any) {
      toast.error(err.response?.data?.message || "Error occurred");
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle className="text-center">
            {type === "login" ? "Login" : "Register"}
          </CardTitle>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="flex flex-col gap-4">
            <Input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <Input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </CardContent>
          <CardFooter className="flex flex-col gap-3">
            <Button type="submit" className="w-full">
              {type === "login" ? "Login" : "Register"}
            </Button>
            <p className="text-sm text-center text-muted-foreground">
              {type === "login" ? (
                <>
                  Don’t have an account?{" "}
                  <Link to="/auth/register" className="text-blue-500 hover:underline">
                    Register
                  </Link>
                </>
              ) : (
                <>
                  Already have an account?{" "}
                  <Link to="/auth/login" className="text-blue-500 hover:underline">
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
