-- ==============================================================================
-- MERYL SHOES SYSTEM - RESTORE FRONTEND DATA ACCESS
-- Run this in your Supabase SQL Editor (Dashboard > SQL Editor)
--
-- Why this is needed:
-- The pentest remediation script revoked all table permissions from the 'anon' role.
-- Because this application uses custom users stored in public."user", the frontend
-- connects to Supabase using the 'anon' key.
--
-- This script:
-- 1. Restores table SELECT/INSERT/UPDATE/DELETE permissions to the frontend.
-- 2. Maintains column-level security so passwords CANNOT be read via the API.
-- 3. Enables RLS policies for all business data.
-- ==============================================================================

BEGIN;

-- 1. Grant schema usage
GRANT USAGE ON SCHEMA public TO anon, authenticated;

-- 2. Grant table permissions to anon & authenticated
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;

-- 3. Column-Level Security: KEEP PASSWORDS STRICTLY PROTECTED
-- Ensure the 'password' column CAN NEVER be selected by anon or authenticated
REVOKE SELECT ON TABLE public."user" FROM anon, authenticated, public;
GRANT SELECT (user_id, name, username, role_id, status, email, avatar_url, staff_code, created_at, updated_at)
ON TABLE public."user" TO anon, authenticated;

-- 4. Row Level Security Policies for all tables
-- Product & Category
DROP POLICY IF EXISTS "app_product_all" ON public.product;
CREATE POLICY "app_product_all" ON public.product FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "app_category_all" ON public.category;
CREATE POLICY "app_category_all" ON public.category FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);

-- Customers
DROP POLICY IF EXISTS "app_customer_all" ON public.customer;
CREATE POLICY "app_customer_all" ON public.customer FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);

-- Sales & Sales Details & Payments
DROP POLICY IF EXISTS "app_sales_all" ON public.sales_transaction;
CREATE POLICY "app_sales_all" ON public.sales_transaction FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "app_sales_details_all" ON public.sales_details;
CREATE POLICY "app_sales_details_all" ON public.sales_details FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "app_payment_all" ON public.payment;
CREATE POLICY "app_payment_all" ON public.payment FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);

-- Inventory & Inventory Logs
DROP POLICY IF EXISTS "app_inventory_all" ON public.inventory;
CREATE POLICY "app_inventory_all" ON public.inventory FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "app_inventory_log_all" ON public.inventory_log;
CREATE POLICY "app_inventory_log_all" ON public.inventory_log FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);

-- Returns & Return Details
DROP POLICY IF EXISTS "app_returns_all" ON public.returns;
CREATE POLICY "app_returns_all" ON public.returns FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "app_return_details_all" ON public.return_details;
CREATE POLICY "app_return_details_all" ON public.return_details FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);

-- Promotions & Promo Products
DROP POLICY IF EXISTS "app_promotion_all" ON public.promotion;
CREATE POLICY "app_promotion_all" ON public.promotion FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "app_promo_product_all" ON public.promo_product;
CREATE POLICY "app_promo_product_all" ON public.promo_product FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);

-- Notifications & Audit Logs
DROP POLICY IF EXISTS "app_notification_all" ON public.notification;
CREATE POLICY "app_notification_all" ON public.notification FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "app_audit_log_all" ON public.audit_log;
CREATE POLICY "app_audit_log_all" ON public.audit_log FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);

-- User table (non-password fields)
DROP POLICY IF EXISTS "app_user_select" ON public."user";
CREATE POLICY "app_user_select" ON public."user" FOR SELECT TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "app_user_update" ON public."user";
CREATE POLICY "app_user_update" ON public."user" FOR UPDATE TO anon, authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "app_user_insert" ON public."user";
CREATE POLICY "app_user_insert" ON public."user" FOR INSERT TO anon, authenticated WITH CHECK (true);

DROP POLICY IF EXISTS "app_user_delete" ON public."user";
CREATE POLICY "app_user_delete" ON public."user" FOR DELETE TO anon, authenticated USING (true);

-- Roles
DROP POLICY IF EXISTS "app_role_all" ON public.role;
CREATE POLICY "app_role_all" ON public.role FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);

COMMIT;
