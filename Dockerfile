FROM directus/directus:10.8.3

USER root
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*
RUN corepack enable
USER node

WORKDIR /directus

COPY ./schema/package.json ./schema/package-lock.json ./
RUN npm install --prefix ./schema

COPY . .

CMD ["npx", "directus", "start"]