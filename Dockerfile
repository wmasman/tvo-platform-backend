FROM directus/directus:latest

USER root
RUN apk add --no-cache postgresql-client
RUN corepack enable
USER node

WORKDIR /directus

COPY ./schema/package.json ./schema/package-lock.json ./
RUN npm install --prefix ./schema

COPY . .

CMD ["npx", "directus", "start"]