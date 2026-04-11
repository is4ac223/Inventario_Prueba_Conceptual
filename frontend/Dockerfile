# Stage 1: Build de la aplicación Svelte
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar código fuente
COPY . .

# Build de la aplicación
RUN npm run build

# Stage 2: Servir la aplicación con sirv
FROM node:18-alpine

WORKDIR /app

# Instalar sirv-cli globalmente y herramientas
RUN npm install -g sirv-cli && apk add --no-cache bash

# Copiar archivos compilados desde el stage anterior
COPY --from=builder /app/public ./public

# Copiar script de entrada
COPY docker-entrypoint.sh ./
RUN chmod +x ./docker-entrypoint.sh

# Exponer puerto
EXPOSE 5000

# Comando para iniciar el servidor
ENTRYPOINT ["./docker-entrypoint.sh"]
