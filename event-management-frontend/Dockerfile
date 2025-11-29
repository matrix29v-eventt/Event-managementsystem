# Stage 1: Build the React application
FROM node:18 AS build
WORKDIR /app
COPY package.json .
COPY package-lock.json .
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the application using a lightweight web server (Nginx)
FROM nginx:alpine
# Copy the compiled React code from the build stage
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
# Nginx default start command
CMD ["nginx", "-g", "daemon off;"]
# Inside event-management-frontend/Dockerfile (Stage 2)

# Copy the custom configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf 

# Copy the compiled React code
COPY --from=build /app/build /usr/share/nginx/html
# ...