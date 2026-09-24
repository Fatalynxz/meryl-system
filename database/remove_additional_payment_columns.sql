-- ==============================================================================
-- Migration: Remove Additional Payment and Store Credit Columns / Tables
-- Purpose: Aligns the database strictly with the store policy:
-- 1:1 direct even exchange for same product / size replacement only.
-- No cash refunds, no additional payments, no store credit issuance.
-- ==============================================================================

-- 1. Drop unused additional payment and credit columns from returns if they exist
ALTER TABLE IF EXISTS public.returns 
  DROP COLUMN IF EXISTS additional_payment CASCADE,
  DROP COLUMN IF EXISTS adjustment_amount CASCADE,
  DROP COLUMN IF EXISTS total_replacement_payments CASCADE,
  DROP COLUMN IF EXISTS total_credits_issued CASCADE,
  DROP COLUMN IF EXISTS mode_of_payment CASCADE,
  DROP COLUMN IF EXISTS net_amount CASCADE,
  DROP COLUMN IF EXISTS payment_date CASCADE;

-- 2. Drop unused price difference columns from return_details if they exist
ALTER TABLE IF EXISTS public.return_details
  DROP COLUMN IF EXISTS price_difference CASCADE,
  DROP COLUMN IF EXISTS net_difference CASCADE,
  DROP COLUMN IF EXISTS returned_price_unit CASCADE,
  DROP COLUMN IF EXISTS new_price_unit CASCADE;

-- 3. Drop unused customer credit tables if they exist
DROP TABLE IF EXISTS public.customer_credit_transactions CASCADE;
DROP TABLE IF EXISTS public.customer_credits CASCADE;
