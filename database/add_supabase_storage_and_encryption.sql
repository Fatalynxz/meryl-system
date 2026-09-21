-- ==============================================================================
-- MERYL SHOES ENTERPRISE SYSTEM
-- Supabase Storage Buckets & pgcrypto Field-Level Encryption Migration
-- Run this in Supabase SQL Editor (https://supabase.com/dashboard)
-- ==============================================================================

begin;

-- 1. Ensure required database columns exist
alter table if exists public."user"
  add column if not exists avatar_url text;

alter table if exists public.returns
  add column if not exists receipt_proof_name text,
  add column if not exists receipt_proof_path text,
  add column if not exists receipt_proof_url text,
  add column if not exists receipt_verified_at timestamp with time zone;

-- ==============================================================================
-- 2. SUPABASE STORAGE BUCKETS (Encrypted at rest with AES-256)
-- ==============================================================================

-- A. user-avatars bucket (profile pictures)
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'user-avatars',
  'user-avatars',
  true,
  5242880, -- 5 MB limit
  array['image/jpeg', 'image/png', 'image/webp', 'image/gif']
)
on conflict (id) do update
set
  public = excluded.public,
  file_size_limit = excluded.file_size_limit,
  allowed_mime_types = excluded.allowed_mime_types;

-- B. return-receipts bucket (replacement receipt proof photos)
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'return-receipts',
  'return-receipts',
  true,
  10485760, -- 10 MB limit
  array['image/jpeg', 'image/png', 'image/webp', 'image/gif']
)
on conflict (id) do update
set
  public = excluded.public,
  file_size_limit = excluded.file_size_limit,
  allowed_mime_types = excluded.allowed_mime_types;

-- ==============================================================================
-- 3. STORAGE ROW-LEVEL SECURITY (RLS) POLICIES
-- ==============================================================================

-- Clean up existing policies if previously applied
drop policy if exists "user_avatars_public_select" on storage.objects;
drop policy if exists "user_avatars_authenticated_insert" on storage.objects;
drop policy if exists "user_avatars_authenticated_update" on storage.objects;
drop policy if exists "user_avatars_authenticated_delete" on storage.objects;

drop policy if exists "return_receipts_select" on storage.objects;
drop policy if exists "return_receipts_insert" on storage.objects;
drop policy if exists "return_receipts_update" on storage.objects;

-- user-avatars: Anyone can view profile avatars (clean CDN URLs)
create policy "user_avatars_public_select"
on storage.objects
for select
using (bucket_id = 'user-avatars');

-- user-avatars: Authenticated or anon client with token can upload/update
create policy "user_avatars_authenticated_insert"
on storage.objects
for insert
with check (bucket_id = 'user-avatars');

create policy "user_avatars_authenticated_update"
on storage.objects
for update
using (bucket_id = 'user-avatars')
with check (bucket_id = 'user-avatars');

create policy "user_avatars_authenticated_delete"
on storage.objects
for delete
using (bucket_id = 'user-avatars');

-- return-receipts: Viewable and uploadable for return validation
create policy "return_receipts_select"
on storage.objects
for select
using (bucket_id = 'return-receipts');

create policy "return_receipts_insert"
on storage.objects
for insert
with check (bucket_id = 'return-receipts');

create policy "return_receipts_update"
on storage.objects
for update
using (bucket_id = 'return-receipts')
with check (bucket_id = 'return-receipts');

-- ==============================================================================
-- 4. PGCRYPTO EXTENSION & FIELD-LEVEL ENCRYPTION FUNCTIONS
-- ==============================================================================

create extension if not exists pgcrypto;

-- Symmetric encryption helper (AES-256 with HMAC integrity check)
create or replace function public.meryl_encrypt_text(
  p_plain text,
  p_key text default current_setting('app.encryption_key', true)
)
returns bytea
language plpgsql
security definer
set search_path = public
as $$
declare
  v_effective_key text;
begin
  if p_plain is null or length(trim(p_plain)) = 0 then
    return null;
  end if;

  v_effective_key := coalesce(nullif(p_key, ''), 'MerylSystem_SecureKey_2026_AES256');
  return pgp_sym_encrypt(p_plain, v_effective_key, 'cipher-algo=aes256, compress-algo=0');
end;
$$;

-- Symmetric decryption helper
create or replace function public.meryl_decrypt_text(
  p_cipher bytea,
  p_key text default current_setting('app.encryption_key', true)
)
returns text
language plpgsql
security definer
set search_path = public
as $$
declare
  v_effective_key text;
begin
  if p_cipher is null then
    return null;
  end if;

  v_effective_key := coalesce(nullif(p_key, ''), 'MerylSystem_SecureKey_2026_AES256');
  begin
    return pgp_sym_decrypt(p_cipher, v_effective_key);
  exception when others then
    return '[Decryption Error: Key Mismatch]';
  end;
end;
$$;

-- Blind index hash helper for fast searching without decrypting
create or replace function public.meryl_hash_lookup(
  p_text text,
  p_salt text default 'meryl_salt_lookup_2026'
)
returns text
language plpgsql
immutable
as $$
begin
  if p_text is null or length(trim(p_text)) = 0 then
    return null;
  end if;
  return encode(hmac(lower(trim(p_text)), p_salt, 'sha256'), 'hex');
end;
$$;

commit;
