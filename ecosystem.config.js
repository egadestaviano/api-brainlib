module.exports = {
  apps: [
    {
      name: "brainlib-backend",
      cwd: "/www/wwwroot/api-brainlib.egadestaviano.my.id",
      script: "start.sh",
      interpreter: "/bin/bash",
      env: {
        APP_ENV: "production"
      }
    }
  ]
};
