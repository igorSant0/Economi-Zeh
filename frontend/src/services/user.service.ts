import { api } from "@/lib/api";
import { UserCreateData, UserUpdateData, UserQuerys, UserResponse, UserListResponse } from "@/types/user.types";

export const userService = {
    // Corresponde a: @router.post("")
    create: async (data: UserCreateData): Promise<UserResponse> => {
        const response = await api.post("/users", data);
        return response.data;
    },

    // Corresponde a: @router.get("")
    getMany: async (filters?: UserQuerys): Promise<UserListResponse> => {
        // O axios passa o objeto filters como query params (ex: ?page=1&limit=10)
        const response = await api.get("/users", { params: filters });
        return response.data;
    },

    // Corresponde a: @router.get("/{user_id}")
    getOne: async (userId: string): Promise<UserResponse> => {
        const response = await api.get(`/users/${userId}`);
        return response.data;
    },

    // Corresponde a: @router.put("/{user_id}")
    update: async (userId: string, data: UserUpdateData): Promise<UserResponse> => {
        const response = await api.put(`/users/${userId}`, data);
        return response.data;
    },

    // Corresponde a: @router.delete("/{user_id}")
    delete: async (userId: string): Promise<void> => {
        await api.delete(`/users/${userId}`);
    },
};
