# syntax=docker/dockerfile:1
FROM node:19-alpine

LABEL name="Capstone Dashboard Frontend"
LABEL description="Hosts the Svelte frontend of Capstone Dashboard"

WORKDIR /app

RUN apk add yarn

# Install dependencies
COPY ./package.json .
COPY ./yarn.lock .
RUN yarn install

# Copy server files
COPY . .

# Get build environment
ARG VITE_PUBLIC_BASE_PATH
ARG VITE_PUBLIC_GITHUB_OWNER
ARG VITE_PRIVATE_GOOGLE_CLIENT_ID

ENV VITE_PUBLIC_BASE_PATH $VITE_PUBLIC_BASE_PATH
ENV VITE_PUBLIC_GITHUB_OWNER $VITE_PUBLIC_GITHUB_OWNER
ENV VITE_PRIVATE_GOOGLE_CLIENT_ID $VITE_PRIVATE_GOOGLE_CLIENT_ID

# Compile Svelte files
RUN yarn build

# Run frontend server to accept all connections on port 80
EXPOSE 80
ENTRYPOINT ["yarn", "preview"]
CMD ["--host", "--port=80"]
