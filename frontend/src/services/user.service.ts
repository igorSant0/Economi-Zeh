import { api } from "@/lib/api";
import type {
  UserCreateData,
  UserUpdateData,
  UserQuerys,
  UserResponse,
  UserListResponse,
} from "@/types/user.types";

export const userService = {
  create: async (data: UserCreateData): Promise<UserResponse> => {
    const response = await api.post("/user", data);
    return response.data;
  },

  getMany: async (filters?: UserQuerys): Promise<UserListResponse> => {
    const response = await api.get("/user", { params: filters });
    return response.data;
  },

  getOne: async (userId: string): Promise<UserResponse> => {
    const response = await api.get(`/user/${userId}`);
    return response.data;
  },

  update: async (
    userId: string,
    data: UserUpdateData,
  ): Promise<UserResponse> => {
    const response = await api.put(`/user/${userId}`, data);
    return response.data;
  },

  delete: async (userId: string): Promise<void> => {
    await api.delete(`/users/${userId}`);
  },
};
