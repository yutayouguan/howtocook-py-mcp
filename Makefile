# HowToCook MCP 项目 Makefile

.PHONY: help install dev test lint format clean run inspect

# 默认目标
help:
	@echo "HowToCook MCP 项目管理命令:"
	@echo ""
	@echo "  install     安装项目依赖"
	@echo "  dev         安装开发依赖"
	@echo "  test        运行测试"
	@echo "  lint        代码检查"
	@echo "  format      代码格式化"
	@echo "  clean       清理缓存文件"
	@echo "  run         启动服务器"
	@echo "  inspect     检查服务器配置"
	@echo "  dev-server  启动开发服务器"

# 安装依赖
install:
	pip install -r requirements.txt

# 安装开发依赖
dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"
	pre-commit install

# 运行测试
test:
	python test_server.py
	python example_usage.py

# 代码检查
lint:
	black --check src/
	isort --check-only src/
	flake8 src/
	mypy src/

# 代码格式化
format:
	black src/
	isort src/

# 清理缓存文件
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name "*.pyo" -delete 2>/dev/null || true
	find . -name ".DS_Store" -delete 2>/dev/null || true

# 启动服务器
run:
	python main.py

# 检查服务器配置
inspect:
	fastmcp inspect server.py

# 启动开发服务器
dev-server:
	fastmcp dev server.py

# 运行完整测试套件
test-full:
	pytest tests/ -v
	python test_server.py
	python example_usage.py

# 构建项目
build:
	python -m build

# 发布到 PyPI
publish:
	python -m twine upload dist/*