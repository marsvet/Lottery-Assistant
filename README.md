# Lottery Assistant

A tool for lottery.

## 如何使用

1. 克隆代码到服务器

   ```bash
   $ git clone git@github.com:marsvet/Lottery-Assistant.git /var/www/Lottery-Assistant
   ```

2. 进入项目根目录，修改 frontend/src/network/index.js 文件中 axios 使用的 baseURL

   ```bash
   $ cd /var/www/Lottery-Assistant
   $ vim frontend/src/network/index.js
   ```

3. 打包构建前端代码

   ```bash
   $ cd frontend
   $ npm install
   $ npm run build
   ```

4. 启动后端代码

   ```bash
   $ cd ../backend
   $ pipenv install
   $ pipenv shell
   $ pipenv install gunicorn
   $ ~/.local/share/virtualenvs/backend-xxx/bin/gunicorn -b 0.0.0.0:3001 main:app
   ```

5. 配置 nginx 服务器，添加以下内容：

   ```bash
   server {
   	listen 3000;
   	server_name localhost;

   	access_log  /var/log/nginx/access.log;
   	error_log  /var/log/nginx/error.log;

   	location /  {
   		root /var/www/Lottery-Assistant/frontend/dist;
   		try_files $uri $uri/ /index.html;
   	}

   	location /raw  {
   		alias /var/www/Lottery-Assistant/backend/raw;
   	}

   	location /api {
   		proxy_pass         http://localhost:3001/;
   		proxy_redirect     off;

   		proxy_set_header   Host             $http_host;
   		proxy_set_header   X-Real-IP        $remote_addr;
   		proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
   	}
   }
   ```

## TODO

- [ ] “回到顶部” 按钮。
- [ ] 表格导出为 EXCEL 的功能。
- [ ] 固定表格头
- [ ] 表格头适配手机的问题。具体情况参见 components/DataTable 组件中的注释
