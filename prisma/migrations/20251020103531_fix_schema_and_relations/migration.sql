/*
  Warnings:

  - The primary key for the `client_profiles` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `Id` on the `client_profiles` table. All the data in the column will be lost.
  - You are about to drop the column `updates_at` on the `freelance_profiles` table. All the data in the column will be lost.
  - The `availability` column on the `freelance_profiles` table would be dropped and recreated. This will lead to data loss if there is data in the column.
  - You are about to drop the `PortfolioItems` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "public"."PortfolioItems" DROP CONSTRAINT "PortfolioItems_freelanceProfileId_fkey";

-- AlterTable
ALTER TABLE "client_profiles" DROP CONSTRAINT "client_profiles_pkey",
DROP COLUMN "Id",
ADD COLUMN     "id" SERIAL NOT NULL,
ADD CONSTRAINT "client_profiles_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "freelance_profiles" DROP COLUMN "updates_at",
ADD COLUMN     "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
DROP COLUMN "availability",
ADD COLUMN     "availability" "Availability" DEFAULT 'AVAILABLE';

-- DropTable
DROP TABLE "public"."PortfolioItems";

-- CreateTable
CREATE TABLE "portfolio_items" (
    "id" SERIAL NOT NULL,
    "title" TEXT NOT NULL,
    "description" TEXT,
    "image_url" TEXT,
    "project_url" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "freelanceProfileId" INTEGER NOT NULL,

    CONSTRAINT "portfolio_items_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "portfolio_items" ADD CONSTRAINT "portfolio_items_freelanceProfileId_fkey" FOREIGN KEY ("freelanceProfileId") REFERENCES "freelance_profiles"("id") ON DELETE CASCADE ON UPDATE CASCADE;
