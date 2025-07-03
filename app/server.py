"""
MCP-BOILERPLATE 服务器实现
使用原生 MCP Server 支持 stdio 和 sse 传输方式
"""

import json
import logging
from collections.abc import Sequence
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from mcp.server import Server
from mcp.types import Resource, TextContent, Tool

from . import client

logger = logging.getLogger("mcp-boilerplate")

class AppContext:
    """应用上下文"""

    def __init__(self):
        self.initialized = False

    async def initialize(self):
        """初始化连接"""
        if not self.initialized:
            logger.info("初始化连接...")
            # 这里可以添加连接验证逻辑
            try:
                # 测试连接
                user_info = client.get_user_info()
                logger.info(f"连接成功，当前用户: {user_info.get('userName', 'Unknown')}")
                self.initialized = True
            except Exception as e:
                logger.error(f"连接失败: {e}")
                raise


@asynccontextmanager
async def server_lifespan(server: Server) -> AsyncIterator[AppContext]:
    """服务器生命周期管理"""
    context = AppContext()

    try:
        logger.info("启动 MCP-BOILERPLATE 服务器")
        await context.initialize()
        yield context
    finally:
        logger.info("关闭 MCP-BOILERPLATE 服务器")


def create_mcp_server(user_id: str = None) -> Server:
    """创建 MCP 服务器实例，支持动态 user_id"""

    # 创建服务器实例
    app = Server("mcp-boilerplate", lifespan=server_lifespan)

    @app.list_resources()
    async def list_resources() -> list[Resource]:
        """列出可用资源"""
        return [
            Resource(
                uri="demo://user",
                name="用户信息",
                mimeType="application/json",
                description="获取当前用户的基本信息，包括用户代码、姓名等"
            ),
            Resource(
                uri="demo://resources",
                name="示例资源数据",
                mimeType="application/json",
                description="获取当前用户可访问的资源数据列表"
            )
        ]

    @app.read_resource()
    async def read_resource(uri: str) -> tuple[str, str]:
        """读取资源内容"""
        if uri == "demo://user":
            try:
                user_info = client.get_user_info(user_id=user_id)
                return (
                    json.dumps(user_info, ensure_ascii=False, indent=2),
                    "application/json"
                )
            except Exception as e:
                logger.error(f"获取用户信息失败: {e}")
                return f"错误: {str(e)}", "text/plain"

        elif uri == "demo://resources":
            try:
                resources = client.query_resources(criteria=None, user_id=user_id)
                return (
                    json.dumps(resources, ensure_ascii=False, indent=2),
                    "application/json"
                )
            except Exception as e:
                logger.error(f"获取文档列表失败: {e}")
                return f"错误: {str(e)}", "text/plain"

        else:
            return f"未知的资源 URI: {uri}", "text/plain"

    @app.list_tools()
    async def list_tools() -> list[Tool]:
        """列出可用工具"""
        return [
            Tool(
                name="get_user_info",
                description="获取当前用户信息",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="query_resources",
                description="获取当前用户可访问的资源数据",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "criteria": {
                            "type": "string",
                            "description": "查询条件",
                        }
                    },
                    "required": []
                }
            ),
        ]

    @app.call_tool()
    async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
        """调用工具"""
        try:
            if name == "get_user_info":
                result = client.get_user_info(user_id=user_id)
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(result, ensure_ascii=False, indent=2)
                    )
                ]

            elif name == "query_resources":
                criteria = arguments.get("criteria")

                # 如果 criteria 是字符串，尝试解析为字典
                if criteria and isinstance(criteria, str):
                    try:
                        criteria = json.loads(criteria)
                    except json.JSONDecodeError:
                        logger.warning(f"无法解析查询条件: {criteria}")
                        criteria = None

                result = client.query_resources(
                    criteria=criteria,
                    user_id=user_id
                )

                return [
                    TextContent(
                        type="text",
                        text=json.dumps(result, ensure_ascii=False, indent=2)
                    )
                ]

            else:
                raise ValueError(f"未知工具: {name}")

        except Exception as e:
            logger.error(f"工具执行错误 {name}: {e}")
            return [
                TextContent(
                    type="text",
                    text=f"错误: {str(e)}"
                )
            ]

    return app
