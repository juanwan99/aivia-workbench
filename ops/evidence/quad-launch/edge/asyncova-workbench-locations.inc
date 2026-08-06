# QUAD-LAUNCH public edge locations (inside asyncova.com SSL server)

location = /experts {
    return 302 /experts/;
}
location ^~ /experts/ {
    alias /var/www/aivia-experts/;
    index index.html;
    add_header Cache-Control "no-cache" always;
    add_header X-Aivia-Experts "1" always;
}

location ^~ /chat/ {
    proxy_pass http://aivia_workbench_tunnel;
    proxy_http_version 1.1;
    proxy_set_header Host workbench.aivia.asia;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Accept-Encoding "";
    sub_filter_types text/css application/javascript application/json;
    sub_filter 'https://workbench.aivia.asia' 'https://asyncova.com';
    sub_filter 'http://workbench.aivia.asia' 'https://asyncova.com';
    sub_filter_once off;
    proxy_read_timeout 3600s;
    proxy_buffering off;
}

location ^~ /_next/ {
    proxy_pass http://aivia_workbench_tunnel;
    proxy_http_version 1.1;
    proxy_set_header Host workbench.aivia.asia;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_read_timeout 120s;
}

location ^~ /dl/ {
    proxy_pass http://aivia_workbench_tunnel;
    proxy_http_version 1.1;
    proxy_set_header Host workbench.aivia.asia;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_buffering off;
    proxy_read_timeout 120s;
}

location ^~ /api {
    proxy_pass http://aivia_workbench_tunnel;
    proxy_http_version 1.1;
    proxy_set_header Host workbench.aivia.asia;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_set_header Accept-Encoding "";
    sub_filter_types application/json;
    sub_filter 'https://workbench.aivia.asia' 'https://asyncova.com';
    sub_filter_once off;
    proxy_read_timeout 3600s;
    proxy_buffering off;
}

location ^~ /files {
    proxy_pass http://aivia_workbench_tunnel;
    proxy_http_version 1.1;
    proxy_set_header Host workbench.aivia.asia;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_read_timeout 120s;
}

location ^~ /v1 {
    proxy_pass http://aivia_workbench_tunnel;
    proxy_http_version 1.1;
    proxy_set_header Host workbench.aivia.asia;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_read_timeout 3600s;
    proxy_buffering off;
}

location ^~ /console {
    proxy_pass http://aivia_workbench_tunnel;
    proxy_http_version 1.1;
    proxy_set_header Host workbench.aivia.asia;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 3600s;
    proxy_buffering off;
}

location ^~ /socket.io/ {
    proxy_pass http://aivia_workbench_tunnel;
    proxy_http_version 1.1;
    proxy_set_header Host workbench.aivia.asia;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 3600s;
    proxy_buffering off;
}

location ^~ /e/ {
    proxy_pass http://aivia_workbench_tunnel;
    proxy_http_version 1.1;
    proxy_set_header Host workbench.aivia.asia;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_read_timeout 120s;
}

location ^~ /explore {
    proxy_pass http://aivia_workbench_tunnel;
    proxy_http_version 1.1;
    proxy_set_header Host workbench.aivia.asia;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_read_timeout 120s;
}

location ^~ /mcp {
    proxy_pass http://aivia_workbench_tunnel;
    proxy_http_version 1.1;
    proxy_set_header Host workbench.aivia.asia;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_read_timeout 120s;
}

location ^~ /triggers {
    proxy_pass http://aivia_workbench_tunnel;
    proxy_http_version 1.1;
    proxy_set_header Host workbench.aivia.asia;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_read_timeout 120s;
}

location ^~ /openapi {
    proxy_pass http://aivia_workbench_tunnel;
    proxy_http_version 1.1;
    proxy_set_header Host workbench.aivia.asia;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;
    proxy_read_timeout 60s;
}

location = /aivia {
    return 302 /chat/lOMVPbz7rZmbJSJl;
}

location = /workbench {
    return 302 /chat/lOMVPbz7rZmbJSJl;
}
