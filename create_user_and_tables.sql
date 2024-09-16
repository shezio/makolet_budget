/* DROP and CREATE will run in psql
    GRANT will run in pgAdmin
   

-- Drop the database if it exists
DROP DATABASE IF EXISTS makoletdb;

-- Create the database
CREATE DATABASE makoletdb;

-- Revoke all privileges from the user if it exists
DO $$
BEGIN
   IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'makoletuser') THEN
      REVOKE ALL PRIVILEGES ON SCHEMA public FROM makoletuser;
      REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM makoletuser;
      REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM makoletuser;
      REVOKE ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public FROM makoletuser;
      ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON TABLES FROM makoletuser;
      DROP ROLE makoletuser;
   END IF;
END
$$;

-- Create the user with the necessary privileges
CREATE USER makoletuser WITH PASSWORD '0192pqowL@';

-- Set role attributes
ALTER ROLE makoletuser SET client_encoding TO 'utf8';
ALTER ROLE makoletuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE makoletuser SET timezone TO 'UTC';
 */
-- Grant all privileges on the database
GRANT ALL PRIVILEGES ON DATABASE makoletdb TO makoletuser;

-- Grant all privileges on the public schema
GRANT USAGE ON SCHEMA public TO makoletuser;
GRANT CREATE ON SCHEMA public TO makoletuser;
GRANT ALL PRIVILEGES ON SCHEMA public TO makoletuser;

-- Grant all privileges on all tables in the public schema
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO makoletuser;

-- Grant all privileges on all sequences in the public schema
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO makoletuser;

-- Grant all privileges on all functions in the public schema
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO makoletuser;

-- Ensure default privileges are set
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO makoletuser;




SELECT schema_name, schema_owner
FROM information_schema.schemata;
SELECT grantee, privilege_type
FROM information_schema.role_table_grants
WHERE table_schema = 'public';

--psql -U postgres
--cd frontend && npm run dev