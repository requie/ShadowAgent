# Use official Node.js image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY frontend/package.json .
RUN npm install --production

# Copy the rest of the frontend code
COPY frontend .

# Build the Next.js app
RUN npm run build

# Expose port 3000 for Next.js
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
