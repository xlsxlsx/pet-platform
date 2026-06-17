# Pet Platform Tech Stack

## 1. 总体架构

项目采用“模块化单体后端 + 统一 API + 多端前端”的路线。MVP 先保证网页端和后端完整可运行，后续再扩展 App、小程序和独立管理后台。

当前实现：

- 后端：Python 3.12 + FastAPI + SQLAlchemy Async + MySQL。
- 前端：静态 HTML/CSS/JavaScript MVP。
- 数据库：MySQL 8.0，数据库名 `pet_platform`。
- 本地脚本：PowerShell 初始化数据库和冒烟验证；服务启动使用可见终端命令。

推荐演进：

- Web 用户端：React + TypeScript + Vite。
- 管理后台：React + TypeScript + Ant Design。
- App：Flutter 或 React Native。
- 小程序：Taro 或 uni-app。
- 缓存与异步任务：Redis + Celery/RQ。
- 对象存储：S3 兼容存储或云厂商 OSS/COS。

## 2. 后端技术栈

- Python 3.12+
- FastAPI
- Pydantic v2
- SQLAlchemy 2.x async
- aiomysql
- Uvicorn
- pytest、httpx、pytest-asyncio
- ruff

当前认证主链路为手机号 + 图形验证码 + 短信验证码。`users.password_hash` 仅为兼容现有表结构的占位字段，不参与登录注册 API；后续迁移可将该字段改为可空或移动到独立凭证表。

## 3. 后端分层

```text
backend/app/
  core/             配置、数据库、安全工具
  domain/           实体、枚举、repository port
  application/      用例和 DTO
  infrastructure/   MySQL repository 实现
  interfaces/       FastAPI 路由、依赖、HTTP DTO
```

依赖规则：

- `domain` 不依赖 FastAPI、SQLAlchemy 或第三方 SDK。
- `application` 编排业务用例，依赖抽象 repository。
- `infrastructure` 实现持久化和外部系统适配。
- `interfaces` 处理 HTTP、认证、参数校验和异常映射。

## 4. 数据库

- MySQL 8.0。
- 字符集：`utf8mb4`。
- 排序规则：`utf8mb4_0900_ai_ci`。
- 存储引擎：InnoDB。
- 金额使用整数分。
- 业务状态使用字符串枚举。
- 初始化脚本位于 `backend/database/init_mysql.sql`。

核心表：

- `users`
- `roles`
- `user_roles`
- `permissions`
- `role_permissions`
- `customer_profiles`
- `merchant_profiles`
- `hospital_profiles`
- `admin_profiles`
- `pets`
- `products`
- `hospitals`
- `service_orders`
- `mall_orders`
- `hospital_appointments`
- `support_tickets`
- `audit_logs`

## 5. API 规范

- API 前缀：`/api/v1`。
- 健康检查：`GET /api/v1/health`。
- 图形验证码：`GET /api/v1/auth/captcha`。
- 短信验证码：`POST /api/v1/auth/sms-code`。
- 登录：`POST /api/v1/auth/login`。
- 注册：`POST /api/v1/auth/register`。
- 角色工作台：`GET /api/v1/dashboards/{role}`。
- 商品目录：`GET /api/v1/catalog/products`。
- 医院目录：`GET /api/v1/catalog/hospitals`。
- OpenAPI 文档：`/docs`。

错误处理要求：

- 图形验证码错误返回明确 400。
- 登录短信验证码错误返回明确 401。
- 禁止注册管理员时返回 403。
- 注册重复手机号返回 400。
- 不把数据库异常直接暴露给前端。

## 6. 前端技术路线

当前静态 Web MVP：

- `web/index.html`
- `web/styles.css`
- `web/app.js`
- `web/assets/`

职责：

- 手机号验证码登录注册。
- 四角色工作台展示。
- 服务、商品、医院和订单概览展示。
- 后端不可用时仅在用户勾选 Demo 模式后使用本地模拟数据。

后续 React 化建议：

- React + TypeScript + Vite。
- React Router 管理路由。
- TanStack Query 管理服务端状态。
- Zustand 管理局部 UI 状态。
- OpenAPI 生成 API 类型。
- 管理后台使用 Ant Design。

## 7. 本地开发

推荐入口：

```powershell
.\scripts\init_mysql.ps1 -User root -Password <your-local-mysql-password>
cd backend
.\.venv312\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

常用地址：

- Web：`http://127.0.0.1:5173`
- Backend：`http://127.0.0.1:8000`
- API Docs：`http://127.0.0.1:8000/docs`

测试账号见根目录 `TEST_ACCOUNTS.md`。

## 8. 后续技术提升

优先级从高到低：

1. 引入 Alembic 管理 schema 版本。
2. 为认证、注册、工作台和目录接口补充自动化测试。
3. 将静态 Web 迁移到 React + TypeScript。
4. 引入 Redis 做验证码、限流、token 黑名单和热点数据缓存。
5. 引入异步任务处理提醒、订单超时、图片处理和统计。
6. 接入真实支付、地图、短信和对象存储。
7. 增加结构化日志、request id、指标和链路追踪。
