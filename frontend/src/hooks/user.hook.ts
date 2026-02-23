import { useQuery } from "@tanstack/react-query";
import { userService } from "@/services/user.service";
import type { UserQuerys } from "@/types/user.types";

export const useUsers = (filters?: UserQuerys) => {
  return useQuery({
    queryKey: ["users", filters],
    queryFn: () => userService.getMany(filters),
  });
};
