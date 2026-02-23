import { z } from "zod";

export const createUserSchema = z
    .object({
        user_name: z.string().min(3),
        user_email: z.string().email(),
        user_cpf: z.string().min(11).max(14),
        user_password: z.string().min(6),
    })
    .strict();

export const updateUserSchema = z
    .object({
        user_name: z.string().min(3).optional(),
        user_email: z.string().email().optional(),
        user_cpf: z.string().min(11).max(14).optional(),
        user_password: z.string().min(6).optional(),
    })
    .strict();

export const userQuerySchema = z.object({
    page: z.number().int().positive().optional(),
    limit: z.number().int().positive().optional(),
    user_name: z.string().optional(),
    user_email: z.string().email().optional(),
    user_cpf: z.string().optional(),
});

export const userResponseSchema = z.object({
    id_user: z.string().uuid(),
    user_name: z.string(),
    user_email: z.string().email(),
    user_cpf: z.string(),
    created_at: z.string(),
    updated_at: z.string(),
    is_deleted: z.boolean(),
});

export const userListResponseSchema = z.object({
    data: z.array(userResponseSchema),
    total: z.number(),
    page: z.number(),
    limit: z.number(),
    total_pages: z.number().optional(),
});

export type UserCreateData = z.infer<typeof createUserSchema>;
export type UserUpdateData = z.infer<typeof updateUserSchema>;
export type UserQuerys = z.infer<typeof userQuerySchema>;
export type UserResponse = z.infer<typeof userResponseSchema>;
export type UserListResponse = z.infer<typeof userListResponseSchema>;
