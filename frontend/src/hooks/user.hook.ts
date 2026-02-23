import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { User } from "@/types/user.types";

const fetchUsers = async (): Promise<User[]> => {
    const response = await api.get("/user");
    return response.data;
};

export const useUsers = () => {
    return useQuery({
        queryKey: ["users"],
        queryFn: fetchUsers,
    });
};
