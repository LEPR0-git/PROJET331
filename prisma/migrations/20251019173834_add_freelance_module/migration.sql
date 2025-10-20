/*
  Warnings:

  - The `role` column on the `users` table would be dropped and recreated. This will lead to data loss if there is data in the column.

*/
-- CreateEnum
CREATE TYPE "UserRole" AS ENUM ('FREELANCE', 'CLIENT', 'ADMIN');

-- CreateEnum
CREATE TYPE "Availability" AS ENUM ('AVAILABLE', 'UNAVAILABLE', 'PART_TIME');

-- AlterTable
ALTER TABLE "users" DROP COLUMN "role",
ADD COLUMN     "role" "UserRole" NOT NULL DEFAULT 'FREELANCE';

-- CreateTable
CREATE TABLE "PortfolioItems" (
    "id" SERIAL NOT NULL,
    "title" TEXT NOT NULL,
    "description" TEXT,
    "imae_url" TEXT,
    "projet_url" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "freelanceProfileId" INTEGER NOT NULL,

    CONSTRAINT "PortfolioItems_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "PortfolioItems_freelanceProfileId_key" ON "PortfolioItems"("freelanceProfileId");

-- AddForeignKey
ALTER TABLE "PortfolioItems" ADD CONSTRAINT "PortfolioItems_freelanceProfileId_fkey" FOREIGN KEY ("freelanceProfileId") REFERENCES "freelance_profiles"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
