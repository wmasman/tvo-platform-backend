FROM directus/directus:10.8.3

USER root
RUN apk add --no-cache postgresql-client
RUN corepack enable
USER node

WORKDIR /directus

COPY . .

ENV HOST="0.0.0.0"
ENV PORT="8055"

CMD ["npx", "directus", "start"]