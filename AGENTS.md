# CLAUDE.md

## 1. 项目开发原则

本项目是 Python 后端 + MySQL + 多端前端的宠物生活服务平台。开发时优先保证业务边界清晰、接口契约稳定、数据安全和多端体验一致。

通用原则：

- 先理解现有模块边界，再修改代码。
- 保持改动小而聚焦。
- 不引入无必要的新框架。
- 核心业务状态必须有明确状态机。
- 支付、退款、审核、封禁等高风险操作必须记录审计日志。
- 用户敏感信息必须脱敏展示。
- 代码结构遵循高内聚、低耦合、SOLID 和依赖倒置原则。
- 普通用户、店家、医院、管理员共享账号体系，通过角色和权限区分能力。
- 本地启动和联调只使用可见终端命令，不新增隐藏后台启动器或静默拉起脚本。

## 2. 仓库结构

```text
pet/
  backend/
    app/
      core/
      domain/
      application/
      infrastructure/
      interfaces/
    database/
    pyproject.toml
  web/
  docs/
  scripts/
  PRD.md
  DESIGN.md
  TECH.md
  SPEC.md
  TEST_ACCOUNTS.md
```

## 3. 后端规范

### 3.1 Python

- 使用 Python 3.12+。
- 使用 FastAPI、Pydantic v2、SQLAlchemy 2.x、MySQL 8.0。
- 所有公共函数和 DTO 使用类型标注。
- `domain/` 放实体、枚举、领域规则和 repository port。
- `application/` 放用例编排和 DTO。
- `infrastructure/` 放 MySQL、缓存、外部服务适配器。
- `interfaces/` 放 HTTP 路由、依赖注入和请求/响应 schema。
- 路由函数只做参数校验、鉴权、调用用例和异常映射。
- 禁止让 `domain/` 依赖 FastAPI、SQLAlchemy、Redis 或第三方 SDK。

### 3.2 API

- API 前缀使用 `/api/v1`。
- 路由按业务资源组织。
- 错误响应必须稳定，不能直接暴露数据库异常。
- 写操作必须做权限校验。
- 管理后台接口必须校验管理员角色和权限点。
- 注册、登录、权限失败应返回明确状态码。

### 3.3 数据库

- 表使用 InnoDB 和 utf8mb4。
- 所有核心表包含 `id`、`created_at`、`updated_at`。
- 需要软删除的表使用 `deleted_at`。
- 金额使用整数分，不使用浮点数。
- 订单号、支付单号使用独立唯一字段。
- 状态字段使用枚举字符串。
- 初始化 SQL 用于本地演示，生产 schema 必须迁移到 Alembic。

### 3.4 安全

- 不提交真实密钥。
- `.env` 只保留本地配置，不提交生产密钥。
- 日志不得输出完整手机号、地址、门锁信息、token。
- 管理员注册必须有配置开关。
- Demo 登录只能由用户显式开启。
- 生产环境必须开启真实鉴权 token 和 RBAC。

### 3.5 测试

- 使用 pytest。
- 认证、注册、权限和工作台接口必须有集成测试。
- 订单、支付、退款、库存和预约时段必须有状态流转测试。
- 修复 bug 时优先补回归测试。

## 4. 前端规范

### 4.1 当前静态 Web

- 保持 `web/index.html`、`web/styles.css`、`web/app.js` 可直接运行。
- API 请求集中封装，不在多个地方拼接同一接口。
- 登录失败展示真实错误。
- 提交期间按钮必须 disabled。
- Demo 模式必须显式勾选。
- 关键模块必须处理 loading、empty、error。

### 4.2 后续 React Web

- 使用 React + TypeScript + Vite。
- 使用 React Router 管理路由。
- 使用 TanStack Query 管理服务端状态。
- 使用 Zustand 或框架内状态管理本地 UI。
- 页面组件只负责组合，复杂业务逻辑抽到 hooks 或 service。
- 类型定义放在 `types/` 或业务模块内。

### 4.3 UI

- 遵循 `DESIGN.md`。
- 移动端点击热区不小于 44px。
- 表单字段必须有 label。
- 金额、时间、订单状态统一格式化。
- 工作台以可扫描的信息密度为主，不做过度营销化布局。

## 5. Git 与提交

- 分支命名建议：`feature/xxx`、`fix/xxx`、`chore/xxx`。
- 提交信息建议使用 Conventional Commits。
- 每个 PR 只解决一个明确问题。
- PR 描述包含改动说明、测试结果和风险点。

## 6. 质量门禁

合并前至少通过：

- 后端编译检查。
- 后端单元或集成测试。
- 前端语法检查。
- 核心页面本地冒烟测试。
- 文档无乱码和过期技术描述。

## 7. 禁止事项

- 禁止在代码中提交真实密钥。
- 禁止绕过权限直接访问管理接口。
- 禁止用浮点数处理金额。
- 禁止前端信任订单金额。
- 禁止把临时调试代码提交到主分支。
- 禁止在后端不可用时默认伪造登录成功。
