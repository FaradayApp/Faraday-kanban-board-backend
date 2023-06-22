# бекенд nginx
FROM nginx:1.19.0-alpine
COPY ./nginx.backend.conf /etc/nginx/conf.d/default.conf