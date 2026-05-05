#!/bin/bash
# Script para generar certificados SSL/TLS 1.3 autofirmados para desarrollo
# Uso: bash generate_ssl.sh

set -e

CERT_DIR="./nginx/ssl"
CERT_FILE="$CERT_DIR/cert.pem"
KEY_FILE="$CERT_DIR/key.pem"

echo "🔐 Generando certificado SSL/TLS para desarrollo..."

# Crear directorio si no existe
mkdir -p $CERT_DIR

# Generar certificado autofirmado válido por 365 días
openssl req -x509 -newkey rsa:4096 -keyout $KEY_FILE -out $CERT_FILE \
    -days 365 -nodes \
    -subj "/C=CO/ST=State/L=City/O=Inventario/OU=IT/CN=localhost" \
    -addext "subjectAltName=DNS:localhost,DNS:127.0.0.1,DNS:backend,DNS:frontend"

echo "✅ Certificado generado exitosamente:"
echo "   📄 Certificado: $CERT_FILE"
echo "   🔑 Clave Privada: $KEY_FILE"
echo ""
echo "ℹ️  Información del certificado:"
openssl x509 -in $CERT_FILE -text -noout | grep -E "Subject:|Public-Key:|Not Before|Not After|CN="

echo ""
echo "⚠️  NOTA IMPORTANTE:"
echo "   - Este es un certificado AUTOFIRMADO para desarrollo"
echo "   - El navegador mostrará advertencia de seguridad"
echo "   - Para PRODUCCIÓN, usar Let's Encrypt u otro CA confiable"
echo "   - Comando: certbot certonly --standalone -d tu-dominio.com"
