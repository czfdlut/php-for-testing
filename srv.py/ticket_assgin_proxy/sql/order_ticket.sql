/*
 Navicat Premium Data Transfer

 Source Server         : sssss
 Source Server Type    : MySQL
 Source Server Version : 50643
 Source Host           : localhost:3306
 Source Schema         : ticket_proxy

 Target Server Type    : MySQL
 Target Server Version : 50643
 File Encoding         : 65001

 Date: 04/03/2019 10:43:44
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for order_ticket
-- ----------------------------
DROP TABLE IF EXISTS `order_ticket`;
CREATE TABLE `order_ticket`  (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `uid` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '商户id',
  `merchantCode` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '商户系统编号',
  `merchantName` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '商户名称',
  `bizNo` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '业务流水编号',
  `bizName` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '业务名称',
  `bizBrief` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '业务摘要',
  `bizTime` datetime(0) NULL DEFAULT NULL COMMENT '业务日期',
  `orderDate` datetime(0) NULL DEFAULT NULL COMMENT '订票日期',
  `orderNo` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '对应订单流水号',
  `ticketPrices` float(11, 0) NOT NULL COMMENT '总票价',
  `payType` int(11) NOT NULL DEFAULT 0 COMMENT '支付类型： 0、云闪付 1、\r\n支付宝 2、微信 3 、其\r\n他',
  `mobile` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '手机号',
  `requestID` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '请求流水号',
  `orderTicketFlow` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '操作流水号',
  `updateTime` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '更新时间',
  `status` int(11) NULL DEFAULT NULL COMMENT '执行状态码',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 142 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
