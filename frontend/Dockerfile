# Dockerfile

# Build the React app
FROM node:20-alpine AS build

WORKDIR /app
COPY . /app

RUN npm install
RUN npm run build 

# Set up Nginx to serve the built app
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html
RUN chmod -R 755 /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf

COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80