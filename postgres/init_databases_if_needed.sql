SELECT 'CREATE DATABASE users_db'
WHERE NOT EXISTS (
    SELECT FROM pg_database WHERE datname = 'users_db'
)\gexec

SELECT 'CREATE DATABASE pathfinder_db'
WHERE NOT EXISTS (
    SELECT FROM pg_database WHERE datname = 'pathfinder_db'
)\gexec

