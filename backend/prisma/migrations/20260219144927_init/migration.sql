-- CreateTable
CREATE TABLE "user" (
    "id_user" TEXT NOT NULL,
    "user_name" TEXT NOT NULL,
    "user_cpf" TEXT NOT NULL,
    "user_email" TEXT NOT NULL,
    "user_password" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_deleted" BOOLEAN NOT NULL DEFAULT false,
    "deleted_date" TIMESTAMP(3),

    CONSTRAINT "user_pkey" PRIMARY KEY ("id_user")
);

-- CreateTable
CREATE TABLE "category" (
    "id_category" TEXT NOT NULL,
    "category_title" TEXT NOT NULL,
    "category_color_hex" TEXT,
    "fk_id_user" TEXT NOT NULL,

    CONSTRAINT "category_pkey" PRIMARY KEY ("id_category")
);

-- CreateTable
CREATE TABLE "expense" (
    "id_expense" TEXT NOT NULL,
    "expense_description" TEXT,
    "expense_unit_value" DOUBLE PRECISION,
    "expense_quantity" DOUBLE PRECISION,
    "expense_date" TIMESTAMP(3) NOT NULL,
    "expense_total_value" DOUBLE PRECISION,
    "fk_id_user" TEXT NOT NULL,

    CONSTRAINT "expense_pkey" PRIMARY KEY ("id_expense")
);

-- CreateTable
CREATE TABLE "planning" (
    "id_planning" TEXT NOT NULL,
    "planning_reference_month" TIMESTAMP(3),
    "planning_target_value" DOUBLE PRECISION,
    "planning_title" TEXT,
    "planning_description" TEXT,
    "planning_type" TEXT,
    "fk_id_user" TEXT NOT NULL,

    CONSTRAINT "planning_pkey" PRIMARY KEY ("id_planning")
);

-- CreateTable
CREATE TABLE "category_expense" (
    "fk_id_expense" TEXT NOT NULL,
    "fk_id_category" TEXT NOT NULL,

    CONSTRAINT "category_expense_pkey" PRIMARY KEY ("fk_id_expense","fk_id_category")
);

-- CreateIndex
CREATE UNIQUE INDEX "user_user_cpf_key" ON "user"("user_cpf");

-- AddForeignKey
ALTER TABLE "category" ADD CONSTRAINT "category_fk_id_user_fkey" FOREIGN KEY ("fk_id_user") REFERENCES "user"("id_user") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "expense" ADD CONSTRAINT "expense_fk_id_user_fkey" FOREIGN KEY ("fk_id_user") REFERENCES "user"("id_user") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "planning" ADD CONSTRAINT "planning_fk_id_user_fkey" FOREIGN KEY ("fk_id_user") REFERENCES "user"("id_user") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "category_expense" ADD CONSTRAINT "category_expense_fk_id_expense_fkey" FOREIGN KEY ("fk_id_expense") REFERENCES "expense"("id_expense") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "category_expense" ADD CONSTRAINT "category_expense_fk_id_category_fkey" FOREIGN KEY ("fk_id_category") REFERENCES "category"("id_category") ON DELETE CASCADE ON UPDATE CASCADE;
