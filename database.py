import os
from urllib.parse import urlparse, unquote

import mysql.connector


def _config_from_env():
    """Build the MySQL connection settings from environment variables.

    Two options (the first one found wins):
      1. DATABASE_URL / MYSQL_URL  → mysql://user:password@host:port/dbname
         (format provided by Railway, PlanetScale, Aiven, etc.)
      2. Individual DB_HOST / DB_PORT / DB_USER / DB_PASSWORD / DB_NAME vars.

    Falls back to the local development database when nothing is set.
    """
    url = os.environ.get("DATABASE_URL") or os.environ.get("MYSQL_URL")
    if url:
        parsed = urlparse(url)
        config = {
            "host": parsed.hostname or "localhost",
            "port": parsed.port or 3306,
            "user": unquote(parsed.username or "root"),
            "password": unquote(parsed.password or ""),
            "database": (parsed.path or "/ecommerce").lstrip("/"),
        }
    else:
        config = {
            "host": os.environ.get("DB_HOST", "localhost"),
            "port": int(os.environ.get("DB_PORT", "3306")),
            "user": os.environ.get("DB_USER", "root"),
            "password": os.environ.get("DB_PASSWORD", "amine"),
            "database": os.environ.get("DB_NAME", "ecommerce"),
        }

    # Most hosted MySQL providers require TLS. Set DB_SSL_CA to a CA bundle
    # path if your provider hands you one (e.g. /etc/ssl/cert.pem).
    ssl_ca = os.environ.get("DB_SSL_CA")
    if ssl_ca:
        config["ssl_ca"] = ssl_ca
        config["ssl_verify_identity"] = True

    return config


_CONFIG = _config_from_env()

# On Vercel (serverless), functions are short-lived and may run in parallel:
# a fresh connection per request is the reliable pattern. Locally we keep a
# small pool for snappier page loads. The pool is created lazily so a
# missing local MySQL doesn't crash the import.
_IS_SERVERLESS = bool(os.environ.get("VERCEL"))
_pool = None


def get_db():
    """Return a fresh (connection, cursor) pair. Caller closes both."""
    global _pool
    if _IS_SERVERLESS:
        conn = mysql.connector.connect(**_CONFIG)
    else:
        if _pool is None:
            from mysql.connector import pooling
            _pool = pooling.MySQLConnectionPool(
                pool_name="ecommerce_pool", pool_size=5, **_CONFIG
            )
        conn = _pool.get_connection()
    cur = conn.cursor(dictionary=True)
    return conn, cur
