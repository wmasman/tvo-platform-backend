FROM directus/directus:latest

USER root
RUN apk add --no-cache postgresql-client
RUN corepack enable
USER node

WORKDIR /directus

COPY . .

CMD ["npx", "directus", "start"]