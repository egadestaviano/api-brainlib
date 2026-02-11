module.exports = {
  apps: [
    {
      name: "brainlib-backend",
      cwd: "/www/wwwroot/api-brainlib.egadestaviano.my.id",
      script: "/www/wwwroot/api-brainlib.egadestaviano.my.id/.venv/bin/uvicorn",
      args: "app.main:app --host 127.0.0.1 --port 8003 --workers 3 --proxy-headers --forwarded-allow-ips='*'",
      interpreter: "none",
      env: {
        APP_ENV: "production"
      }
    }
  ]
};
