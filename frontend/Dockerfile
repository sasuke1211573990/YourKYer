# 第一阶段：构建前端项目
FROM node:18-alpine as build-stage

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装依赖（使用淘宝镜像加速）
RUN npm config set registry https://registry.npmmirror.com/
RUN npm install

# 复制所有文件
COPY . .

# 构建项目
RUN npm run build

# 第二阶段：生产环境 Nginx
FROM nginx:stable-alpine as production-stage

# 复制构建产物到 Nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 复制自定义 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露 80 端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
