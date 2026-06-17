CREATE DATABASE IF NOT EXISTS pet_platform
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_0900_ai_ci;

USE pet_platform;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS audit_logs;
DROP TABLE IF EXISTS support_tickets;
DROP TABLE IF EXISTS hospital_appointments;
DROP TABLE IF EXISTS mall_orders;
DROP TABLE IF EXISTS service_orders;
DROP TABLE IF EXISTS service_providers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS hospitals;
DROP TABLE IF EXISTS merchant_profiles;
DROP TABLE IF EXISTS hospital_profiles;
DROP TABLE IF EXISTS customer_profiles;
DROP TABLE IF EXISTS admin_profiles;
DROP TABLE IF EXISTS pets;
DROP TABLE IF EXISTS addresses;
DROP TABLE IF EXISTS role_permissions;
DROP TABLE IF EXISTS permissions;
DROP TABLE IF EXISTS user_roles;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS users;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE users (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  phone VARCHAR(32) NOT NULL UNIQUE,
  display_name VARCHAR(80) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at DATETIME NULL,
  INDEX idx_users_status (status)
) ENGINE=InnoDB;

CREATE TABLE roles (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  code VARCHAR(32) NOT NULL UNIQUE,
  name VARCHAR(80) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE user_roles (
  user_id BIGINT UNSIGNED NOT NULL,
  role_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (user_id, role_id),
  CONSTRAINT fk_user_roles_user FOREIGN KEY (user_id) REFERENCES users(id),
  CONSTRAINT fk_user_roles_role FOREIGN KEY (role_id) REFERENCES roles(id)
) ENGINE=InnoDB;

CREATE TABLE permissions (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  code VARCHAR(120) NOT NULL UNIQUE,
  name VARCHAR(120) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE role_permissions (
  role_id BIGINT UNSIGNED NOT NULL,
  permission_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (role_id, permission_id),
  CONSTRAINT fk_role_permissions_role FOREIGN KEY (role_id) REFERENCES roles(id),
  CONSTRAINT fk_role_permissions_permission FOREIGN KEY (permission_id) REFERENCES permissions(id)
) ENGINE=InnoDB;

CREATE TABLE customer_profiles (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL UNIQUE,
  nickname VARCHAR(80) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_customer_profiles_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE merchant_profiles (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL UNIQUE,
  store_name VARCHAR(120) NOT NULL,
  contact_phone VARCHAR(32) NOT NULL,
  review_status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_merchant_profiles_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE hospital_profiles (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL UNIQUE,
  hospital_name VARCHAR(120) NOT NULL,
  license_no VARCHAR(80) NOT NULL,
  review_status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_hospital_profiles_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE admin_profiles (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL UNIQUE,
  employee_no VARCHAR(64) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_admin_profiles_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE addresses (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL,
  contact_name VARCHAR(80) NOT NULL,
  contact_phone VARCHAR(32) NOT NULL,
  province VARCHAR(40) NOT NULL,
  city VARCHAR(40) NOT NULL,
  district VARCHAR(40) NOT NULL,
  detail VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_addresses_user FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE pets (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  owner_user_id BIGINT UNSIGNED NOT NULL,
  name VARCHAR(80) NOT NULL,
  species VARCHAR(32) NOT NULL,
  breed VARCHAR(80) NOT NULL,
  gender VARCHAR(16) NOT NULL,
  birth_date DATE NULL,
  health_notes TEXT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_pets_owner FOREIGN KEY (owner_user_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE products (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  merchant_id BIGINT UNSIGNED NOT NULL,
  name VARCHAR(160) NOT NULL,
  category VARCHAR(80) NOT NULL,
  price_cents INT UNSIGNED NOT NULL,
  stock INT UNSIGNED NOT NULL DEFAULT 0,
  status VARCHAR(32) NOT NULL DEFAULT 'ON_SALE',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_products_merchant FOREIGN KEY (merchant_id) REFERENCES merchant_profiles(id),
  INDEX idx_products_category (category),
  INDEX idx_products_status (status)
) ENGINE=InnoDB;

CREATE TABLE service_providers (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL UNIQUE,
  real_name VARCHAR(80) NOT NULL,
  service_city VARCHAR(40) NOT NULL,
  service_district VARCHAR(40) NOT NULL,
  rating DECIMAL(3,2) NOT NULL DEFAULT 5.00,
  completed_orders INT UNSIGNED NOT NULL DEFAULT 0,
  review_status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_service_providers_user FOREIGN KEY (user_id) REFERENCES users(id),
  INDEX idx_service_providers_area (service_city, service_district),
  INDEX idx_service_providers_review (review_status)
) ENGINE=InnoDB;

CREATE TABLE hospitals (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  hospital_profile_id BIGINT UNSIGNED NOT NULL,
  name VARCHAR(120) NOT NULL,
  city VARCHAR(40) NOT NULL,
  district VARCHAR(40) NOT NULL,
  address VARCHAR(255) NOT NULL,
  phone VARCHAR(32) NOT NULL,
  open_status VARCHAR(32) NOT NULL DEFAULT 'OPEN',
  rating DECIMAL(3,2) NOT NULL DEFAULT 5.00,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_hospitals_profile FOREIGN KEY (hospital_profile_id) REFERENCES hospital_profiles(id),
  INDEX idx_hospitals_location (city, district),
  INDEX idx_hospitals_status (open_status)
) ENGINE=InnoDB;

CREATE TABLE service_orders (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  order_no VARCHAR(64) NOT NULL UNIQUE,
  customer_user_id BIGINT UNSIGNED NOT NULL,
  provider_id BIGINT UNSIGNED NOT NULL,
  pet_id BIGINT UNSIGNED NOT NULL,
  service_type VARCHAR(40) NOT NULL,
  scheduled_start DATETIME NOT NULL,
  status VARCHAR(32) NOT NULL,
  amount_cents INT UNSIGNED NOT NULL,
  service_report TEXT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_service_orders_customer FOREIGN KEY (customer_user_id) REFERENCES users(id),
  CONSTRAINT fk_service_orders_provider FOREIGN KEY (provider_id) REFERENCES service_providers(id),
  CONSTRAINT fk_service_orders_pet FOREIGN KEY (pet_id) REFERENCES pets(id),
  INDEX idx_service_orders_customer (customer_user_id, status),
  INDEX idx_service_orders_provider (provider_id, status)
) ENGINE=InnoDB;

CREATE TABLE mall_orders (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  order_no VARCHAR(64) NOT NULL UNIQUE,
  customer_user_id BIGINT UNSIGNED NOT NULL,
  merchant_id BIGINT UNSIGNED NOT NULL,
  status VARCHAR(32) NOT NULL,
  total_amount_cents INT UNSIGNED NOT NULL,
  delivery_status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_mall_orders_customer FOREIGN KEY (customer_user_id) REFERENCES users(id),
  CONSTRAINT fk_mall_orders_merchant FOREIGN KEY (merchant_id) REFERENCES merchant_profiles(id),
  INDEX idx_mall_orders_customer (customer_user_id, status),
  INDEX idx_mall_orders_merchant (merchant_id, status)
) ENGINE=InnoDB;

CREATE TABLE hospital_appointments (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  appointment_no VARCHAR(64) NOT NULL UNIQUE,
  customer_user_id BIGINT UNSIGNED NOT NULL,
  hospital_id BIGINT UNSIGNED NOT NULL,
  pet_id BIGINT UNSIGNED NOT NULL,
  appointment_time DATETIME NOT NULL,
  status VARCHAR(32) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_hospital_appointments_customer FOREIGN KEY (customer_user_id) REFERENCES users(id),
  CONSTRAINT fk_hospital_appointments_hospital FOREIGN KEY (hospital_id) REFERENCES hospitals(id),
  CONSTRAINT fk_hospital_appointments_pet FOREIGN KEY (pet_id) REFERENCES pets(id),
  INDEX idx_hospital_appointments_customer (customer_user_id, status),
  INDEX idx_hospital_appointments_hospital (hospital_id, status)
) ENGINE=InnoDB;

CREATE TABLE support_tickets (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  ticket_no VARCHAR(64) NOT NULL UNIQUE,
  requester_user_id BIGINT UNSIGNED NOT NULL,
  owner_role VARCHAR(32) NOT NULL,
  category VARCHAR(64) NOT NULL,
  status VARCHAR(32) NOT NULL,
  priority VARCHAR(32) NOT NULL DEFAULT 'NORMAL',
  title VARCHAR(160) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_support_tickets_requester FOREIGN KEY (requester_user_id) REFERENCES users(id),
  INDEX idx_support_tickets_status (status, priority),
  INDEX idx_support_tickets_owner (owner_role)
) ENGINE=InnoDB;

CREATE TABLE audit_logs (
  id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
  actor_user_id BIGINT UNSIGNED NOT NULL,
  action VARCHAR(120) NOT NULL,
  resource_type VARCHAR(80) NOT NULL,
  resource_id VARCHAR(80) NOT NULL,
  detail JSON NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_audit_logs_actor FOREIGN KEY (actor_user_id) REFERENCES users(id),
  INDEX idx_audit_logs_resource (resource_type, resource_id)
) ENGINE=InnoDB;

INSERT INTO roles (code, name) VALUES
  ('CUSTOMER', '普通用户'),
  ('MERCHANT', '宠物用品店家'),
  ('HOSPITAL', '宠物医院'),
  ('ADMIN', '管理员');

INSERT INTO permissions (code, name) VALUES
  ('pet:read', '查看宠物档案'),
  ('pet:write', '维护宠物档案'),
  ('service:order:create', '创建上门服务订单'),
  ('merchant:product:write', '维护店家商品'),
  ('merchant:order:manage', '管理店家订单'),
  ('hospital:profile:write', '维护医院资料'),
  ('hospital:appointment:manage', '管理医院预约'),
  ('admin:user:manage', '管理用户'),
  ('admin:audit:read', '查看审计日志');

INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r JOIN permissions p
WHERE (r.code = 'CUSTOMER' AND p.code IN ('pet:read', 'pet:write', 'service:order:create'))
   OR (r.code = 'MERCHANT' AND p.code IN ('merchant:product:write', 'merchant:order:manage'))
   OR (r.code = 'HOSPITAL' AND p.code IN ('hospital:profile:write', 'hospital:appointment:manage'))
   OR (r.code = 'ADMIN');

INSERT INTO users (phone, display_name, password_hash, status) VALUES
  ('13800000001', '普通用户示例', 'pbkdf2_sha256$120000$customer-demo-salt$WQJnevds+AiccmamOHDOsP/iu5CDCOlUPnwvQUiSbtg=', 'ACTIVE'),
  ('13800000002', '用品店家示例', 'pbkdf2_sha256$120000$merchant-demo-salt$ZgCdH0+8zaUc4VMA+UjD1E2Ww7nG/mF4bvT7ZSofXEY=', 'ACTIVE'),
  ('13800000003', '宠物医院示例', 'pbkdf2_sha256$120000$hospital-demo-salt$oNNTx5Xqk7caSkFKCLemjS955Tl8QjrMRhxjQnYX8mE=', 'ACTIVE'),
  ('13800000004', '平台管理员示例', 'pbkdf2_sha256$120000$admin-demo-salt$lUOWsuoJVXBiDtFCT3zx+3P0lHJxhYIhs/XTvpKMkIU=', 'ACTIVE'),
  ('13800000005', '上门服务者示例', 'pbkdf2_sha256$120000$provider-demo-salt$h/VIrQ5XCcpxl+w/3reWR/XMr0BYeLMC2bESkyKxamg=', 'ACTIVE');

INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id FROM users u JOIN roles r
WHERE (u.phone = '13800000001' AND r.code = 'CUSTOMER')
   OR (u.phone = '13800000002' AND r.code = 'MERCHANT')
   OR (u.phone = '13800000003' AND r.code = 'HOSPITAL')
   OR (u.phone = '13800000004' AND r.code = 'ADMIN')
   OR (u.phone = '13800000005' AND r.code = 'CUSTOMER');

INSERT INTO customer_profiles (user_id, nickname)
SELECT id, '米粒家长' FROM users WHERE phone = '13800000001';

INSERT INTO merchant_profiles (user_id, store_name, contact_phone, review_status)
SELECT id, '爪爪优选宠物用品店', '021-60000002', 'APPROVED' FROM users WHERE phone = '13800000002';

INSERT INTO hospital_profiles (user_id, hospital_name, license_no, review_status)
SELECT id, '安心宠物医院', 'VET-2026-0001', 'APPROVED' FROM users WHERE phone = '13800000003';

INSERT INTO admin_profiles (user_id, employee_no)
SELECT id, 'ADM-0001' FROM users WHERE phone = '13800000004';

INSERT INTO addresses (user_id, contact_name, contact_phone, province, city, district, detail)
SELECT id, '夏女士', '13800000001', '上海市', '上海市', '长宁区', '天山路 100 号' FROM users WHERE phone = '13800000001';

INSERT INTO pets (owner_user_id, name, species, breed, gender, birth_date, health_notes)
SELECT id, '米粒', 'CAT', '英短', 'FEMALE', '2023-04-10', '已绝育，换粮需要过渡 7 天' FROM users WHERE phone = '13800000001';

INSERT INTO products (merchant_id, name, category, price_cents, stock, status)
SELECT id, '无谷鸡肉全价猫粮 2kg', '猫粮', 15900, 120, 'ON_SALE' FROM merchant_profiles WHERE store_name = '爪爪优选宠物用品店';

INSERT INTO products (merchant_id, name, category, price_cents, stock, status)
SELECT id, '豆腐混合猫砂 6L', '猫砂', 3900, 300, 'ON_SALE' FROM merchant_profiles WHERE store_name = '爪爪优选宠物用品店';

INSERT INTO hospitals (hospital_profile_id, name, city, district, address, phone, open_status, rating)
SELECT id, '安心宠物医院长宁店', '上海市', '长宁区', '天山路 200 号', '021-60000003', 'OPEN', 4.90
FROM hospital_profiles WHERE hospital_name = '安心宠物医院';

INSERT INTO service_providers (user_id, real_name, service_city, service_district, rating, completed_orders, review_status)
SELECT id, '林小夏', '上海市', '长宁区', 4.98, 268, 'APPROVED' FROM users WHERE phone = '13800000005';

INSERT INTO service_orders (order_no, customer_user_id, provider_id, pet_id, service_type, scheduled_start, status, amount_cents, service_report)
SELECT 'SO202606150001', u.id, sp.id, p.id, 'FEEDING', '2026-06-15 18:30:00', 'ACCEPTED', 8800, '待服务，需要回传照片和饮水情况'
FROM users u
JOIN service_providers sp ON sp.real_name = '林小夏'
JOIN pets p ON p.owner_user_id = u.id
WHERE u.phone = '13800000001';

INSERT INTO service_orders (order_no, customer_user_id, provider_id, pet_id, service_type, scheduled_start, status, amount_cents, service_report)
SELECT 'SO202606120001', u.id, sp.id, p.id, 'FEEDING', '2026-06-12 18:30:00', 'COMPLETED', 8800, '米粒进食正常，猫砂已清理，照片已回传'
FROM users u
JOIN service_providers sp ON sp.real_name = '林小夏'
JOIN pets p ON p.owner_user_id = u.id
WHERE u.phone = '13800000001';

INSERT INTO mall_orders (order_no, customer_user_id, merchant_id, status, total_amount_cents, delivery_status)
SELECT 'MO202606150001', u.id, m.id, 'PAID', 19800, 'SHIPPING'
FROM users u JOIN merchant_profiles m
WHERE u.phone = '13800000001' AND m.store_name = '爪爪优选宠物用品店';

INSERT INTO hospital_appointments (appointment_no, customer_user_id, hospital_id, pet_id, appointment_time, status, reason)
SELECT 'HA202606160001', u.id, h.id, p.id, '2026-06-16 10:30:00', 'PENDING_CONFIRM', '年度体检和疫苗咨询'
FROM users u
JOIN pets p ON p.owner_user_id = u.id
JOIN hospitals h ON h.name = '安心宠物医院长宁店'
WHERE u.phone = '13800000001';

INSERT INTO support_tickets (ticket_no, requester_user_id, owner_role, category, status, priority, title)
SELECT 'TK202606150001', id, 'ADMIN', 'SERVICE_COMPLAINT', 'OPEN', 'HIGH', '上门服务照片回传延迟'
FROM users WHERE phone = '13800000001';

INSERT INTO audit_logs (actor_user_id, action, resource_type, resource_id, detail)
SELECT id, 'database.seed', 'database', 'pet_platform', JSON_OBJECT('roles', 4, 'sample_users', 5, 'dashboards', 4)
FROM users WHERE phone = '13800000004';
