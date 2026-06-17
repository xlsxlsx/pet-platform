from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.dashboard.entities import DashboardMetric, DashboardTask, RoleDashboard


class MySQLDashboardRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_role_dashboard(self, role: str) -> RoleDashboard:
        builders = {
            "CUSTOMER": self._customer_dashboard,
            "MERCHANT": self._merchant_dashboard,
            "HOSPITAL": self._hospital_dashboard,
            "ADMIN": self._admin_dashboard,
        }
        builder = builders.get(role)
        if builder is None:
            raise ValueError(f"unsupported role: {role}")
        return await builder()

    async def _scalar(self, sql: str) -> int:
        result = await self._session.execute(text(sql))
        return int(result.scalar_one() or 0)

    async def _customer_dashboard(self) -> RoleDashboard:
        pet_count = await self._scalar("SELECT COUNT(*) FROM pets")
        service_orders = await self._scalar("SELECT COUNT(*) FROM service_orders")
        mall_orders = await self._scalar("SELECT COUNT(*) FROM mall_orders")
        appointments = await self._scalar("SELECT COUNT(*) FROM hospital_appointments")
        return RoleDashboard(
            role="CUSTOMER",
            title="普通用户工作台",
            metrics=(
                DashboardMetric("宠物档案", str(pet_count), "健康资料驱动服务推荐"),
                DashboardMetric("服务订单", str(service_orders), "包含待服务与历史服务"),
                DashboardMetric("商城订单", str(mall_orders), "用品购买与配送状态"),
                DashboardMetric("医院预约", str(appointments), "体检、疫苗和问诊意向"),
            ),
            tasks=(
                DashboardTask("确认今晚喂养服务", "ACCEPTED", "服务者将于 18:30 上门并回传报告"),
                DashboardTask("查看猫粮配送", "SHIPPING", "商城订单正在配送中"),
                DashboardTask("确认医院预约", "PENDING_CONFIRM", "等待医院确认明日体检时间"),
            ),
        )

    async def _merchant_dashboard(self) -> RoleDashboard:
        product_count = await self._scalar("SELECT COUNT(*) FROM products")
        low_stock = await self._scalar("SELECT COUNT(*) FROM products WHERE stock < 150")
        order_count = await self._scalar("SELECT COUNT(*) FROM mall_orders")
        paid_orders = await self._scalar("SELECT COUNT(*) FROM mall_orders WHERE status = 'PAID'")
        return RoleDashboard(
            role="MERCHANT",
            title="宠物用品店家工作台",
            metrics=(
                DashboardMetric("在售商品", str(product_count), "商品和库存需要持续维护"),
                DashboardMetric("库存预警", str(low_stock), "低于阈值的 SKU"),
                DashboardMetric("商城订单", str(order_count), "当前店铺订单总量"),
                DashboardMetric("待发货", str(paid_orders), "支付完成等待履约"),
            ),
            tasks=(
                DashboardTask("处理猫粮订单", "PAID", "尽快发货并填写物流单号"),
                DashboardTask("补充猫粮库存", "LOW_STOCK", "无谷鸡肉全价猫粮库存低于补货线"),
                DashboardTask("配置复购优惠", "TODO", "面向 30 天复购用户发券"),
            ),
        )

    async def _hospital_dashboard(self) -> RoleDashboard:
        hospital_count = await self._scalar("SELECT COUNT(*) FROM hospitals")
        appointment_count = await self._scalar("SELECT COUNT(*) FROM hospital_appointments")
        pending = await self._scalar(
            "SELECT COUNT(*) FROM hospital_appointments WHERE status = 'PENDING_CONFIRM'"
        )
        open_hospitals = await self._scalar("SELECT COUNT(*) FROM hospitals WHERE open_status = 'OPEN'")
        return RoleDashboard(
            role="HOSPITAL",
            title="宠物医院工作台",
            metrics=(
                DashboardMetric("医院门店", str(hospital_count), "已接入平台的门店"),
                DashboardMetric("预约意向", str(appointment_count), "用户提交的就诊需求"),
                DashboardMetric("待确认", str(pending), "需要医院处理"),
                DashboardMetric("营业中", str(open_hospitals), "当前可接待门店"),
            ),
            tasks=(
                DashboardTask("确认米粒体检预约", "PENDING_CONFIRM", "用户希望明日 10:30 到院"),
                DashboardTask("维护医生排班", "TODO", "补齐本周医生出诊时间"),
                DashboardTask("更新疫苗套餐", "TODO", "发布猫三联和狂犬疫苗提醒"),
            ),
        )

    async def _admin_dashboard(self) -> RoleDashboard:
        user_count = await self._scalar("SELECT COUNT(*) FROM users")
        merchant_count = await self._scalar("SELECT COUNT(*) FROM merchant_profiles")
        hospital_count = await self._scalar("SELECT COUNT(*) FROM hospital_profiles")
        open_tickets = await self._scalar("SELECT COUNT(*) FROM support_tickets WHERE status = 'OPEN'")
        return RoleDashboard(
            role="ADMIN",
            title="管理员工作台",
            metrics=(
                DashboardMetric("平台账号", str(user_count), "四类角色统一账号体系"),
                DashboardMetric("店家入驻", str(merchant_count), "用品供给侧"),
                DashboardMetric("医院入驻", str(hospital_count), "医疗供给侧"),
                DashboardMetric("待处理工单", str(open_tickets), "投诉、退款和风险事件"),
            ),
            tasks=(
                DashboardTask("处理高优先级投诉", "OPEN", "上门服务照片回传延迟"),
                DashboardTask("复核店家商品资质", "TODO", "重点检查食品和药品类目"),
                DashboardTask("查看审计日志", "TODO", "关注退款、封禁、审核操作"),
            ),
        )
