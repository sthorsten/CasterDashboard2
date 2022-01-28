###############
# Build stage #
###############

FROM node:14 as build

WORKDIR /frontend

# Install node dependencies
COPY package.json .
COPY yarn.lock .
RUN yarn install

# Copy all (other) files
COPY . .

# Build for production, but with devtools enabled (for now)
RUN yarn build --devtools

# Copy deploy files to subdir
RUN mkdir deploy
RUN cp -r .nuxt deploy/
RUN cp -r static deploy/
RUN cp -r node_modules deploy/
RUN cp package.json deploy/
RUN cp yarn.lock deploy/

################
# Docker image #
################
FROM node:lts-alpine

WORKDIR /frontend

# Copy from build files
COPY --from=build /frontend/deploy .
