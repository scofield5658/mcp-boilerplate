# 启动脚本 (PowerShell)
# 使用 SSE 传输方式启动服务

# 设置环境变量
# $env:SOME_ENV_VAR = "SOME_ENV_VALUE"

# 启动服务器
uv run mcp-boilerplate `
    --transport sse `
    --host 0.0.0.0 `
    --port 18002 `
    --verbose

Write-Host "MCP-BOILERPLATE SSE 服务器已启动在 http://0.0.0.0:18002/sse"
