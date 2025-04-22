FROM node:20-bullseye

WORKDIR /home/node/app
EXPOSE 3000
COPY . /home/node/app
RUN npm i
CMD ["npm", "run", "dev"]