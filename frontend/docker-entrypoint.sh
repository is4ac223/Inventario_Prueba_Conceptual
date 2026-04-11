#!/bin/sh
# Script para inyectar la URL de la API en el index.html

API_URL="${API_URL:-http://localhost:8000/api}"

# Reemplazar la URL de la API en el index.html
sed -i "s|window\.__API_URL__ = window\.__API_URL__ || '[^']*'|window.__API_URL__ = window.__API_URL__ || '${API_URL}'|g" /app/public/index.html

# Iniciar sirv
exec sirv public --single --port 5000 --host
