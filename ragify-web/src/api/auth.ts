import { api } from "./api";

export const login = (username: string, password: string) => {
  return api.post("/auth/login", { username, password });
};

export const register = (username: string, password: string) => {
  return api.post("/auth/register", { username, password });
};
