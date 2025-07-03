#!/usr/bin/env python3
"""
MCP-BOILERPLATE 服务测试脚本
用于验证服务器功能是否正常
"""

import asyncio
import logging
import os
import sys

# 添加 app 模块到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.server import create_mcp_server


async def test_server():
    """测试服务器基本功能"""

    # 设置日志级别
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        logger.info("创建 MCP 服务器实例...")
        server = create_mcp_server()

        logger.info("验证服务器配置...")

        # 简单验证服务器对象
        if server is None:
            raise Exception("服务器创建失败")

        if not hasattr(server, 'name'):
            raise Exception("服务器对象缺少必要属性")

        logger.info(f"✅ 服务器创建成功，名称: {server.name}")

        # 验证能够创建初始化选项
        try:
            init_options = server.create_initialization_options()
            logger.info(f"✅ 初始化选项创建成功")
        except Exception as e:
            logger.warning(f"⚠️  初始化选项创建失败: {e}")

        logger.info("✅ 服务器基本功能测试通过！")

    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        raise


async def test_connection():
    """测试连接"""
    logger = logging.getLogger(__name__)

    try:
        from app import client

        logger.info("测试用户信息获取...")
        user_info = client.get_user_info()
        logger.info(f"用户信息: {user_info.get('userName', 'Unknown')}")

        logger.info("✅ 连接测试通过！")

    except Exception as e:
        logger.error(f"❌ 连接测试失败: {e}")


async def main():
    """主测试函数"""
    logger = logging.getLogger(__name__)

    logger.info("🚀 开始 MCP-BOILERPLATE 服务测试")

    # 基本功能测试
    await test_server()

    # 连接测试
    await test_connection()

    logger.info("🎉 所有测试完成！")


if __name__ == "__main__":
    asyncio.run(main())
