# Using an older version of the node image known to have vulnerabilities
FROM node:10.16.0

# Install a package that might have vulnerabilities
RUN npm install lodash@4.17.10

# Set the working directory
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json
COPY package*.json ./

# Install application dependencies
RUN npm install

# Bundle app source
COPY . .

CMD [ "node", "sunday-app.js" ]
