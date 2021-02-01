###############
# Build stage #
###############

FROM node:lts-alpine as build

WORKDIR /frontend

# Install node dependencies
COPY package.json .
RUN yarn install

# Copy all (other) files
COPY . .

# Build for production, but with devtools enabled (for now)
RUN yarn build --devtools


################
# Docker image #
################
FROM node:lts-alpine

WORKDIR /frontend

# Copy from build files
COPY --from=build /frontend/.nuxt ./.nuxt
COPY --from=build /frontend/package.json .
COPY --from=build /frontend/yarn.lock .
COPY --from=build /frontend/node_modules ./node_modules