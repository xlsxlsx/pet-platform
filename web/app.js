const API_BASE_URL = "http://127.0.0.1:8000/api/v1";
const PHONE_PATTERN = /^1[3-9]\d{9}$/;
const SETTINGS_STORAGE_KEY = "petcare-settings";
const PROFILE_STORAGE_KEY = "petcare-profile";
const SETTINGS_THEME_MAP = {
  light: "light",
  dark: "dark",
};
const FONT_SCALE_LABELS = {
  "0.92": "小",
  "1.00": "中",
  "1.12": "大",
};

const roleMap = {
  customer: {
    apiRole: "CUSTOMER",
    label: "普通用户",
    title: "普通用户工作台",
    loginTitle: "普通用户登录",
    action: "创建预约",
    defaultPhone: "13800000001",
    sampleName: "米粒家长",
    sampleOrg: "",
    metrics: [
      ["宠物档案", "1", "健康和喂养记录"],
      ["照护任务", "2", "上门喂养和医院预约"],
      ["商城订单", "1", "宠物食品配送中"],
      ["健康提醒", "3", "疫苗、驱虫、体检"],
    ],
    tasks: [
      ["确认上门喂养", "ACCEPTED", "服务者将于 18:30 到达并上传报告"],
      ["跟踪猫粮配送", "SHIPPING", "商城订单正在配送中"],
      ["确认医院预约", "PENDING", "医院需要确认明日体检时间"],
    ],
  },
  merchant: {
    apiRole: "MERCHANT",
    label: "店家",
    title: "店家工作台",
    loginTitle: "宠物用品店家登录",
    action: "新增商品",
    defaultPhone: "13800000002",
    sampleName: "店铺运营",
    sampleOrg: "爪选宠物用品店",
    metrics: [
      ["在售商品", "2", "当前可售商品"],
      ["待发货", "1", "已支付等待履约"],
      ["库存预警", "1", "宠物食品低于补货线"],
      ["售后", "0", "今日无新增售后"],
    ],
    tasks: [
      ["发出猫粮订单", "PAID", "填写物流单号"],
      ["补充猫粮库存", "LOW_STOCK", "鸡肉猫粮低于补货线"],
      ["创建复购优惠券", "TODO", "面向 30 天复购用户"],
    ],
  },
  hospital: {
    apiRole: "HOSPITAL",
    label: "医院",
    title: "宠物医院工作台",
    loginTitle: "宠物医院登录",
    action: "管理排班",
    defaultPhone: "13800000003",
    sampleName: "医院运营",
    sampleOrg: "安心宠物医院",
    metrics: [
      ["预约", "1", "用户到院需求"],
      ["待确认", "1", "需要医院处理"],
      ["营业门店", "1", "当前可接待门店"],
      ["健康内容", "3", "疫苗、驱虫、体检主题"],
    ],
    tasks: [
      ["确认米粒体检", "PENDING", "用户希望明日 10:30 到院"],
      ["维护医生排班", "TODO", "补齐本周医生班次"],
      ["更新疫苗套餐", "TODO", "发布猫咪疫苗提醒"],
    ],
  },
  admin: {
    apiRole: "ADMIN",
    label: "管理员",
    title: "管理员工作台",
    loginTitle: "管理员登录",
    action: "处理工单",
    defaultPhone: "13800000004",
    sampleName: "平台管理员",
    sampleOrg: "",
    metrics: [
      ["账号", "5", "统一账号体系"],
      ["店家", "1", "用品供给侧"],
      ["医院", "1", "医疗供给侧"],
      ["待处理工单", "1", "投诉、退款、风险事件"],
    ],
    tasks: [
      ["处理紧急投诉", "OPEN", "上门服务照片上传延迟"],
      ["复核商品资质", "TODO", "重点关注食品和药品类目"],
      ["检查审计日志", "TODO", "退款、封禁、审核操作"],
    ],
  },
};

const services = [
  {
    id: 1,
    type: "feeding",
    title: "上门喂养与猫砂清理",
    provider: "林小夏",
    rating: "4.98",
    distance: "1.2km",
    price: 88,
    image: "./assets/service-feeding.png",
    tags: ["已认证", "猫砂清理", "照片报告"],
  },
  {
    id: 2,
    type: "walking",
    title: "遛狗 45 分钟",
    provider: "陈牧",
    rating: "4.95",
    distance: "2.4km",
    price: 68,
    image: "./assets/service-walking.png",
    tags: ["路线记录", "大型犬", "晚间"],
  },
  {
    id: 3,
    type: "boarding",
    title: "家庭寄养咨询",
    provider: "安心寄养",
    rating: "4.92",
    distance: "3.1km",
    price: 128,
    image: "./assets/service-boarding.png",
    tags: ["独立房间", "每日视频", "可接送"],
  },
  {
    id: 4,
    type: "feeding",
    title: "多宠家庭上门照护",
    provider: "周安",
    rating: "4.90",
    distance: "1.8km",
    price: 108,
    image: "./assets/service-feeding.png",
    tags: ["多宠", "辅助喂药", "服务报告"],
  },
];

let products = [
  {
    id: 1,
    title: "无谷鸡肉全价猫粮 2kg",
    subtitle: "成猫适用，温和配方",
    price: 159,
    image: "./assets/product-food.png",
    tags: ["猫咪", "高蛋白"],
  },
  {
    id: 2,
    title: "犬用关节营养咀嚼片",
    subtitle: "中大型犬日常护理",
    price: 89,
    image: "./assets/product-care.png",
    tags: ["犬用", "关节"],
  },
  {
    id: 3,
    title: "豆腐混合猫砂 6L",
    subtitle: "低粉尘，快速结团",
    price: 39,
    image: "./assets/product-care.png",
    tags: ["低粉尘", "可冲厕"],
  },
  {
    id: 4,
    title: "宠物饮水机滤芯",
    subtitle: "三片装，月度替换",
    price: 45,
    image: "./assets/product-care.png",
    tags: ["饮水", "滤芯"],
  },
];

let hospitals = [
  {
    name: "安心宠物医院长宁店",
    status: "营业中",
    distance: "1.6km",
    rating: "4.9",
    image: "./assets/hospital-care.png",
    specialty: "内科、疫苗、影像",
  },
  {
    name: "瑞派宠物医院",
    status: "可预约",
    distance: "2.3km",
    rating: "4.8",
    image: "./assets/hospital-care.png",
    specialty: "猫科、皮肤科、绝育",
  },
  {
    name: "宠医笙动物医院",
    status: "急诊",
    distance: "4.8km",
    rating: "4.9",
    image: "./assets/hospital-care.png",
    specialty: "急诊、外科、留观",
  },
];

const serviceOrders = [
  {
    title: "米粒 - 上门喂养",
    status: "已接单",
    time: "2026-06-15 18:30",
    detail: "服务者林小夏，预计服务 40 分钟",
  },
  {
    title: "米粒 - 上门喂养",
    status: "已完成",
    time: "2026-06-12 18:30",
    detail: "食物、饮水和猫砂报告已提交",
  },
];

const shopOrders = [
  {
    title: "无谷鸡肉全价猫粮 2kg",
    status: "配送中",
    time: "明日送达",
    detail: "同城配送单号 SF2039",
  },
  {
    title: "豆腐混合猫砂 6L",
    status: "已签收",
    time: "2026-06-10",
    detail: "可评价并领取复购券",
  },
];

const profileOrders = [
  {
    kind: "service",
    title: "米粒 - 上门喂养",
    status: "已完成",
    time: "2026-06-15 18:30",
    detail: "服务报告已上传，包含饮水和猫砂状态。",
  },
  {
    kind: "shop",
    title: "无谷鸡肉全价猫粮 2kg",
    status: "配送中",
    time: "2026-06-16",
    detail: "订单号 SF2039，预计明日送达。",
  },
  {
    kind: "hospital",
    title: "安心宠物医院体检",
    status: "待确认",
    time: "2026-06-18 10:30",
    detail: "基础体检、驱虫复查与疫苗咨询。",
  },
  {
    kind: "service",
    title: "可乐 - 遛狗 45 分钟",
    status: "已接单",
    time: "2026-06-12 19:00",
    detail: "夜间路线已确认，支持实时消息。",
  },
];

const defaultProfile = {
  nickname: "米粒家长",
  avatarStyle: "blue",
  gender: "female",
  phone: "13800000001",
  bio: "专注上门喂养、宠物健康和日常陪伴。",
};

const defaultSettings = {
  theme: "light",
  fontScale: "1.00",
};

let activeRole = "customer";
let authMode = "login";
let cartCount = 0;
let currentCaptchaId = "";
let profileFilter = "all";
let profileState = readProfileState();
let settingsState = readSettingsState();

const pageTitles = {
  home: "工作台",
  services: "上门服务",
  shop: "宠物商城",
  hospitals: "宠物医院",
  orders: "订单",
  profile: "我的",
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function readProfileState() {
  try {
    const raw = window.localStorage.getItem(PROFILE_STORAGE_KEY);
    return raw ? { ...defaultProfile, ...JSON.parse(raw) } : { ...defaultProfile };
  } catch (error) {
    return { ...defaultProfile };
  }
}

function readSettingsState() {
  try {
    const raw = window.localStorage.getItem(SETTINGS_STORAGE_KEY);
    return raw ? { ...defaultSettings, ...JSON.parse(raw) } : { ...defaultSettings };
  } catch (error) {
    return { ...defaultSettings };
  }
}

function persistProfileState() {
  window.localStorage.setItem(PROFILE_STORAGE_KEY, JSON.stringify(profileState));
}

function persistSettingsState() {
  window.localStorage.setItem(SETTINGS_STORAGE_KEY, JSON.stringify(settingsState));
}

function avatarGradient(style) {
  const map = {
    blue: "linear-gradient(135deg, #2f80ed, #6bb3ff)",
    green: "linear-gradient(135deg, #27ae60, #6bcf95)",
    orange: "linear-gradient(135deg, #f2994a, #ffbf80)",
    violet: "linear-gradient(135deg, #7f5af0, #b18cff)",
  };
  return map[style] || map.blue;
}

function avatarFillColor(style) {
  return {
    blue: "#2f80ed",
    green: "#27ae60",
    orange: "#f2994a",
    violet: "#7f5af0",
  }[style] || "#2f80ed";
}

function genderLabel(value) {
  return {
    female: "女",
    male: "男",
    secret: "保密",
  }[value] || "保密";
}

function settingsThemeLabel(theme) {
  return theme === "dark" ? "深色" : "浅色";
}

function setBodyTheme() {
  document.body.dataset.theme = settingsState.theme;
  document.body.style.setProperty("--app-font-scale", settingsState.fontScale);
}

function renderProfileSummary() {
  const nickname = profileState.nickname || defaultProfile.nickname;
  const gender = genderLabel(profileState.gender);
  const phone = profileState.phone || defaultProfile.phone;
  const bio = profileState.bio || defaultProfile.bio;
  const avatarSvg = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
      <rect width="200" height="200" rx="32" fill="${avatarFillColor(profileState.avatarStyle)}"/>
      <circle cx="100" cy="82" r="34" fill="white" fill-opacity="0.9"/>
      <path d="M46 168c8-26 32-42 54-42s46 16 54 42" fill="white" fill-opacity="0.9"/>
    </svg>
  `;

  $("#profile-avatar-image").alt = `${nickname} 的头像`;
  $("#profile-avatar-image").style.background = avatarGradient(profileState.avatarStyle);
  $("#profile-avatar-image").src = `data:image/svg+xml;base64,${window.btoa(avatarSvg)}`;
  $("#profile-nickname-label").textContent = nickname;
  $("#profile-meta-line").textContent = `普通用户 · ${gender} · ${phone}`;
  $("#profile-role-tag").textContent = "普通用户";
  $("#profile-level-tag").textContent = "白银会员";
  $("#profile-city-tag").textContent = "上海长宁";
  $("#profile-nickname").value = nickname;
  $("#profile-gender").value = profileState.gender;
  $("#profile-avatar-style").value = profileState.avatarStyle;
  $("#profile-phone").value = phone;
  $("#profile-bio").value = bio;
}

function renderProfileOrders() {
  const items = profileOrders.filter((order) => profileFilter === "all" || order.kind === profileFilter);
  $("#profile-order-list").innerHTML = items
    .map(
      (order) => `
        <article class="order-item profile-order-item">
          <div class="item-topline">
            <div>
              <h3>${escapeHtml(order.title)}</h3>
              <p>${escapeHtml(order.detail)}</p>
            </div>
            <span class="tag">${escapeHtml(order.status)}</span>
          </div>
          <p>${escapeHtml(order.time)}</p>
        </article>
      `,
    )
    .join("");
}

function renderSettings() {
  $("#theme-toggle").checked = settingsState.theme === SETTINGS_THEME_MAP.dark;
  $("#font-scale").value = settingsState.fontScale;
  $("#font-scale").dataset.label = FONT_SCALE_LABELS[settingsState.fontScale] || "中";
}

function applySettings() {
  setBodyTheme();
  renderSettings();
}

async function fetchJson(path) {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(await response.text());
  }
  return response.json();
}

async function postJson(path, payload) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error(await response.text());
  }
  return response.json();
}

function showToast(message) {
  const toast = $("#toast");
  toast.textContent = message;
  toast.classList.add("show");
  window.clearTimeout(showToast.timer);
  showToast.timer = window.setTimeout(() => toast.classList.remove("show"), 2200);
}

function getAuthFormValues() {
  return {
    phone: $("#auth-phone").value.trim(),
    captchaCode: $("#auth-captcha-code").value.trim(),
    smsCode: $("#auth-sms-code").value.trim(),
  };
}

function ensureValidPhone(phone) {
  if (!PHONE_PATTERN.test(phone)) {
    showToast("请输入正确的 11 位手机号");
    return false;
  }
  return true;
}

function tagMarkup(tags) {
  return tags.map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join("");
}

function serviceCard(service) {
  return `
    <article class="service-card" data-type="${service.type}">
      <img class="service-image" src="${service.image}" alt="${escapeHtml(service.title)}" />
      <div class="service-body">
        <h3>${escapeHtml(service.title)}</h3>
        <p>${escapeHtml(service.provider)} - ${escapeHtml(service.distance)} - 评分 ${escapeHtml(service.rating)}</p>
        <div class="tag-row">${tagMarkup(service.tags)}</div>
        <div class="card-footer">
          <span class="price">¥${service.price}</span>
          <button class="secondary-button" type="button" data-book="${service.id}">预约</button>
        </div>
      </div>
    </article>
  `;
}

function productCard(product) {
  return `
    <article class="product-card">
      <img class="product-cover" src="${product.image}" alt="${escapeHtml(product.title)}" />
      <div class="product-body">
        <h3>${escapeHtml(product.title)}</h3>
        <p>${escapeHtml(product.subtitle)}</p>
        <div class="tag-row">${tagMarkup(product.tags)}</div>
        <div class="card-footer">
          <span class="price">¥${product.price}</span>
          <button class="secondary-button" type="button" data-cart="${product.id}">加入</button>
        </div>
      </div>
    </article>
  `;
}

function hospitalItem(hospital) {
  return `
    <article class="hospital-item">
      <img class="hospital-image" src="${hospital.image}" alt="${escapeHtml(hospital.name)}" />
      <div class="item-topline">
        <div>
          <h3>${escapeHtml(hospital.name)}</h3>
          <p>${escapeHtml(hospital.specialty)}</p>
        </div>
        <span class="tag">${escapeHtml(hospital.status)}</span>
      </div>
      <p>${escapeHtml(hospital.distance)} - 评分 ${escapeHtml(hospital.rating)}</p>
      <div class="item-actions">
        <button class="secondary-button" type="button" data-toast="预约意向已保存">预约</button>
        <button class="secondary-button" type="button" data-toast="地图导航待接入">导航</button>
        <button class="secondary-button" type="button" data-toast="电话能力待接入">电话</button>
      </div>
    </article>
  `;
}

function orderItem(order) {
  return `
    <article class="order-item">
      <div class="item-topline">
        <div>
          <h3>${escapeHtml(order.title)}</h3>
          <p>${escapeHtml(order.detail)}</p>
        </div>
        <span class="tag">${escapeHtml(order.status)}</span>
      </div>
      <p>${escapeHtml(order.time)}</p>
    </article>
  `;
}

function renderRoleWorkspace(role) {
  const workspace = roleMap[role];
  activeRole = role;
  $("#role-eyebrow").textContent = workspace.label;
  $("#role-panel-eyebrow").textContent = workspace.label;
  $("#role-panel-title").textContent = workspace.title;
  $("#role-primary-action").textContent = workspace.action;
  $("#auth-title").textContent = workspace.loginTitle;
  $("#auth-phone").value = workspace.defaultPhone;
  $("#auth-display-name").value = workspace.sampleName;
  $("#auth-organization").value = workspace.sampleOrg;
  $("#auth-sms-code").value = "";

  $("#role-metrics").innerHTML = workspace.metrics
    .map(
      ([label, value, hint]) => `
        <article class="role-metric">
          <span>${escapeHtml(label)}</span>
          <strong>${escapeHtml(value)}</strong>
          <p>${escapeHtml(hint)}</p>
        </article>
      `,
    )
    .join("");

  $("#role-tasks").innerHTML = workspace.tasks
    .map(
      ([title, status, detail]) => `
        <article class="role-task">
          <div>
            <h3>${escapeHtml(title)}</h3>
            <p>${escapeHtml(detail)}</p>
          </div>
          <span class="tag">${escapeHtml(status)}</span>
        </article>
      `,
    )
    .join("");
  loadRoleDashboard(role);
}

function renderDashboard(dashboard) {
  $("#role-panel-title").textContent = dashboard.title;
  $("#role-metrics").innerHTML = dashboard.metrics
    .map(
      (metric) => `
        <article class="role-metric">
          <span>${escapeHtml(metric.label)}</span>
          <strong>${escapeHtml(metric.value)}</strong>
          <p>${escapeHtml(metric.hint)}</p>
        </article>
      `,
    )
    .join("");
  $("#role-tasks").innerHTML = dashboard.tasks
    .map(
      (task) => `
        <article class="role-task">
          <div>
            <h3>${escapeHtml(task.title)}</h3>
            <p>${escapeHtml(task.detail)}</p>
          </div>
          <span class="tag">${escapeHtml(task.status)}</span>
        </article>
      `,
    )
    .join("");
}

async function loadRoleDashboard(role) {
  try {
    const dashboard = await fetchJson(`/dashboards/${roleMap[role].apiRole}`);
    if (activeRole === role) {
      renderDashboard(dashboard);
    }
  } catch (error) {
    // Keep local role seed data when the backend is not running.
  }
}

async function loadCatalogs() {
  try {
    const [apiProducts, apiHospitals] = await Promise.all([
      fetchJson("/catalog/products"),
      fetchJson("/catalog/hospitals"),
    ]);
    products = apiProducts.map((item) => ({
      id: item.id,
      title: item.name,
      subtitle: `${item.merchant_name} - ${item.category} - 库存 ${item.stock}`,
      price: Math.round(item.price_cents / 100),
      image: item.category.includes("粮") ? "./assets/product-food.png" : "./assets/product-care.png",
      tags: [item.category, item.status],
    }));
    hospitals = apiHospitals.map((item) => ({
      name: item.name,
      status: item.open_status,
      distance: `${item.district} · ${item.address}`,
      rating: String(item.rating),
      image: "./assets/hospital-care.png",
      specialty: `${item.city} ${item.phone}`,
    }));
    $("#product-list").innerHTML = products.map(productCard).join("");
    $("#hospital-list").innerHTML = hospitals.map(hospitalItem).join("");
  } catch (error) {
    // Static seed data keeps the page usable without the backend.
  }
}

async function refreshCaptcha() {
  try {
    const captcha = await fetchJson("/auth/captcha");
    currentCaptchaId = captcha.captcha_id;
    $("#auth-captcha-image").src = `data:image/svg+xml;base64,${captcha.image_base64}`;
    $("#auth-captcha-code").value = captcha.debug_code || "";
    $("#auth-sms-code").value = "";
  } catch (error) {
    currentCaptchaId = "";
    $("#auth-captcha-image").removeAttribute("src");
  }
}

function renderSession(session) {
  const card = $("#session-card");
  card.innerHTML = `
    <span>Current session</span>
    <strong>${escapeHtml(session.display_name)}</strong>
    <p>${escapeHtml(session.phone)} - ${escapeHtml(session.active_role)}</p>
  `;
  profileState = {
    ...profileState,
    nickname: session.display_name || profileState.nickname,
    phone: session.phone || profileState.phone,
  };
  persistProfileState();
  renderProfileSummary();
}

function switchView(view) {
  $$(".view").forEach((node) => node.classList.toggle("active", node.id === `view-${view}`));
  $$(".nav-item").forEach((node) => node.classList.toggle("active", node.dataset.view === view));
  $("#page-title").textContent = pageTitles[view];
  if (view === "profile") {
    renderProfileSummary();
    renderProfileOrders();
    renderSettings();
  }
}

function openBooking() {
  const dialog = $("#booking-dialog");
  if (typeof dialog.showModal === "function") {
    dialog.showModal();
  } else {
    showToast("Dialog is not supported by this browser");
  }
}

function setAuthMode(mode) {
  authMode = mode;
  $$("[data-auth-mode]").forEach((button) => {
    button.classList.toggle("active", button.dataset.authMode === mode);
  });
  $$(".register-only").forEach((node) => node.classList.toggle("hidden", mode !== "register"));
  $("#auth-submit").textContent = mode === "login" ? "登录" : "注册";
  $("#auth-sms-code").value = "";
  refreshCaptcha();
}

async function sendSmsCode() {
  const sendButton = $("#auth-send-sms");
  const { phone, captchaCode } = getAuthFormValues();
  if (!ensureValidPhone(phone)) {
    return;
  }
  if (!captchaCode || !currentCaptchaId) {
    showToast("请先填写图形验证码");
    return;
  }

  sendButton.disabled = true;
  sendButton.textContent = "发送中";
  try {
    const result = await postJson("/auth/sms-code", {
      phone,
      captcha_id: currentCaptchaId,
      captcha_code: captchaCode,
      purpose: authMode === "login" ? "LOGIN" : "REGISTER",
    });
    if (result.debug_code) {
      $("#auth-sms-code").value = result.debug_code;
      showToast(`本地短信验证码：${result.debug_code}`);
    } else {
      showToast("短信验证码已发送");
    }
  } catch (error) {
    showToast("验证码发送失败，请刷新图片后重试");
    refreshCaptcha();
  } finally {
    sendButton.disabled = false;
    sendButton.textContent = "发送验证码";
  }
}

async function submitAuth(event) {
  event.preventDefault();
  const workspace = roleMap[activeRole];
  const submitButton = $("#auth-submit");
  const demoMode = $("#auth-demo-mode").checked;
  const { phone, smsCode } = getAuthFormValues();
  if (!ensureValidPhone(phone)) {
    return;
  }
  if (!smsCode) {
    showToast("请先填写短信验证码");
    return;
  }
  const payload = {
    phone,
    sms_code: smsCode,
    role: workspace.apiRole,
  };
  if (authMode === "register") {
    payload.display_name = $("#auth-display-name").value.trim() || workspace.sampleName;
    payload.organization_name = $("#auth-organization").value.trim() || null;
  }

  submitButton.disabled = true;
  submitButton.textContent = authMode === "login" ? "登录中..." : "注册中...";

  try {
    const session = await postJson(`/auth/${authMode}`, payload);
    renderSession(session);
    showToast(authMode === "login" ? "登录成功" : "注册成功");
    refreshCaptcha();
  } catch (error) {
    if (!demoMode) {
      showToast("后端接口不可用，请启动本地后端或勾选演示模式。");
      return;
    }

    const fallbackSession = {
      phone: payload.phone,
      display_name: authMode === "register" ? payload.display_name : workspace.label,
      active_role: workspace.apiRole,
    };
    renderSession(fallbackSession);
    showToast("接口不可用，已使用本地演示会话");
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = authMode === "login" ? "登录" : "注册";
  }
}

function bindEvents() {
  $$(".nav-item").forEach((button) => {
    button.addEventListener("click", () => switchView(button.dataset.view));
  });

  $$("[data-switch]").forEach((button) => {
    button.addEventListener("click", () => switchView(button.dataset.switch));
  });

  $$("[data-profile-order-filter]").forEach((button) => {
    button.addEventListener("click", () => {
      $$("[data-profile-order-filter]").forEach((node) => node.classList.remove("active"));
      button.classList.add("active");
      profileFilter = button.dataset.profileOrderFilter;
      renderProfileOrders();
    });
  });

  $$("[data-role]").forEach((button) => {
    button.addEventListener("click", () => {
      $$("[data-role]").forEach((node) => node.classList.remove("active"));
      button.classList.add("active");
      renderRoleWorkspace(button.dataset.role);
      switchView("home");
      showToast(`已切换为${roleMap[button.dataset.role].label}`);
    });
  });

  $$("[data-auth-mode]").forEach((button) => {
    button.addEventListener("click", () => setAuthMode(button.dataset.authMode));
  });

  $$(".segmented button[data-filter]").forEach((button) => {
    button.addEventListener("click", () => {
      $$(".segmented button[data-filter]").forEach((node) => node.classList.remove("active"));
      button.classList.add("active");
      const filter = button.dataset.filter;
      $$("#service-list .service-card").forEach((card) => {
        card.style.display = filter === "all" || card.dataset.type === filter ? "" : "none";
      });
    });
  });

  document.body.addEventListener("click", (event) => {
    const toastButton = event.target.closest("[data-toast]");
    const bookButton = event.target.closest("[data-book]");
    const cartButton = event.target.closest("[data-cart]");
    if (toastButton) showToast(toastButton.dataset.toast);
    if (bookButton) openBooking();
    if (cartButton) {
      cartCount += 1;
      $("#cart-count").textContent = String(cartCount);
      showToast("已加入购物车");
    }
  });

  $("#auth-form").addEventListener("submit", submitAuth);
  $("#auth-send-sms").addEventListener("click", sendSmsCode);
  $("#auth-refresh-captcha").addEventListener("click", refreshCaptcha);
  $("#open-booking").addEventListener("click", openBooking);
  $("#submit-booking").addEventListener("click", () => showToast("预约已提交"));
  $("#checkout-button").addEventListener("click", () => {
    showToast(cartCount > 0 ? `正在结算 ${cartCount} 件商品` : "购物车为空");
  });
  $("#notify-button").addEventListener("click", () => showToast("你有 2 条订单提醒"));
  $("#role-primary-action").addEventListener("click", () => showToast(roleMap[activeRole].action));
  $("#save-profile-button").addEventListener("click", () => {
    profileState = {
      ...profileState,
      nickname: $("#profile-nickname").value.trim() || defaultProfile.nickname,
      gender: $("#profile-gender").value,
      avatarStyle: $("#profile-avatar-style").value,
      bio: $("#profile-bio").value.trim() || defaultProfile.bio,
      phone: $("#profile-phone").value.trim() || defaultProfile.phone,
    };
    persistProfileState();
    renderProfileSummary();
    showToast("个人资料已保存");
  });
  $("#profile-nickname").addEventListener("input", (event) => {
    profileState.nickname = event.target.value;
    renderProfileSummary();
  });
  $("#profile-gender").addEventListener("change", (event) => {
    profileState.gender = event.target.value;
    renderProfileSummary();
  });
  $("#profile-avatar-style").addEventListener("change", (event) => {
    profileState.avatarStyle = event.target.value;
    renderProfileSummary();
  });
  $("#profile-bio").addEventListener("input", (event) => {
    profileState.bio = event.target.value;
  });
  $("#theme-toggle").addEventListener("change", (event) => {
    settingsState.theme = event.target.checked ? "dark" : "light";
    persistSettingsState();
    applySettings();
  });
  $("#font-scale").addEventListener("input", (event) => {
    settingsState.fontScale = Number.parseFloat(event.target.value).toFixed(2);
    persistSettingsState();
    applySettings();
  });
  $("#global-search").addEventListener("input", (event) => {
    const keyword = event.target.value.trim();
    if (keyword.length >= 2) showToast(`正在搜索：${keyword}`);
  });
}

function render() {
  $("#home-service-list").innerHTML = services.slice(0, 3).map(serviceCard).join("");
  $("#service-list").innerHTML = services.map(serviceCard).join("");
  $("#product-list").innerHTML = products.map(productCard).join("");
  $("#hospital-list").innerHTML = hospitals.map(hospitalItem).join("");
  $("#service-orders").innerHTML = serviceOrders.map(orderItem).join("");
  $("#shop-orders").innerHTML = shopOrders.map(orderItem).join("");
  renderRoleWorkspace(activeRole);
  setAuthMode("login");
  renderProfileSummary();
  renderProfileOrders();
  applySettings();
  loadCatalogs();
}

render();
bindEvents();
