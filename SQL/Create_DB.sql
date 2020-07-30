CREATE DATABASE  IF NOT EXISTS `ping_management` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ping_management`;
-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: ping_management
-- ------------------------------------------------------
-- Server version	8.0.20
--
-- Table structure for table `comps`
--

DROP TABLE IF EXISTS `comps`;
CREATE TABLE `comps` (
  `id` int NOT NULL AUTO_INCREMENT,
  `compName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `compName_UNIQUE` (`compName`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `pings`
--

DROP TABLE IF EXISTS `pings`;
CREATE TABLE `pings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `compName` varchar(45) DEFAULT NULL,
  `ping` int DEFAULT NULL,
  `timeOfResponce` datetime DEFAULT NULL,
  `status` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1158 DEFAULT CHARSET=utf8mb4;