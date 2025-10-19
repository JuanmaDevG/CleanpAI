
FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

# instalar cli global (ajusta versión si quieres fijarla)
RUN npm i -g @angular/cli@19

COPY . .
RUN ng build --configuration=production



# ---------- Stage 2: Apache ----------
FROM httpd:2.4-alpine

# Copia el build cliente
COPY --from=builder /app/dist/sabadell-mock/browser/ /usr/local/apache2/htdocs/

# Añade tu conf sin machacar httpd.conf
COPY spa.conf /usr/local/apache2/conf/extra/spa.conf

# Activa mod_rewrite y carga tu spa.conf
RUN set -eux; \
  echo 'LoadModule rewrite_module modules/mod_rewrite.so' >> /usr/local/apache2/conf/httpd.conf; \
  echo 'Include conf/extra/spa.conf' >> /usr/local/apache2/conf/httpd.conf

EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD wget -qO- http://localhost/ || exit 1