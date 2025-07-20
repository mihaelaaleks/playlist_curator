# build stage 
FROM node:lts-alpine AS build-stage

# zero config - simple http server for serving static content
# RUN npm install -g http-server

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Set default for Kubernetes, can be overridden
ARG VITE_API_BASE_URL=http://curator-api:8000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

# production stage
FROM nginx:stable-alpine AS production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]