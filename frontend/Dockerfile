# build stage
FROM node:latest as build
WORKDIR /app
COPY package*.json ./
RUN yarn install
COPY . .
RUN yarn build

# production stage
FROM node:latest as production
COPY --from=build /app/dist /app
WORKDIR /app
EXPOSE 3500
CMD npx http-server . -p 3500