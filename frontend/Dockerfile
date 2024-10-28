# frontend/Dockerfile
FROM node:16

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Run tests
RUN npm test

# Build the app
RUN npm run build

# Serve with a lightweight HTTP server (you could replace with Nginx for a more production-ready setup)
RUN npm install -g serve
CMD ["serve", "-s", "build"]
