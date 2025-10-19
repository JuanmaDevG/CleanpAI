# ---------- Base con Node + pnpm ----------
FROM node:20-alpine AS base
WORKDIR /app
# habilita corepack para tener pnpm sin instalarlo globalmente
RUN corepack enable

# ---------- Stage deps (instala dependencias) ----------
FROM base AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
# instalar deps de prod y dev (para compilar); usa lock exacto
RUN pnpm install --frozen-lockfile

# ---------- Stage build (compila Next) ----------
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# Si necesitas variables públicas de API, puedes pasarlas como ARG/ENV
# ARG NEXT_PUBLIC_API_URL
# ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
RUN pnpm build

# ---------- Stage runtime (imagen final, ligera) ----------
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
# Puerto en el que escuchará Next
EXPOSE 3000

# Copia salida standalone + assets estáticos
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

# Si usas rutas internas que leen next.config en runtime:
# COPY --from=builder /app/next.config.mjs ./next.config.mjs

# Healthcheck opcional
HEALTHCHECK --interval=30s --timeout=5s --retries=5 CMD wget -qO- http://localhost:3000 || exit 1

# Ejecuta el servidor standalone de Next
CMD ["node", "server.js"]
