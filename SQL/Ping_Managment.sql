-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
CREATE DATABASE  IF NOT EXISTS `ping_management`;
USE `ping_management`;

-- Tables

-- Table structure for table `comps`
DROP TABLE IF EXISTS `comps`;

CREATE TABLE `comps` (
  `id` int NOT NULL AUTO_INCREMENT,
  `compName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `compName_UNIQUE` (`compName`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4;

-- Table structure for table `pings`
DROP TABLE IF EXISTS `pings`;
CREATE TABLE `pings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `compName` varchar(45) DEFAULT NULL,
  `ping` int DEFAULT NULL,
  `timeOfResponce` datetime DEFAULT NULL,
  `status` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6829 DEFAULT CHARSET=utf8mb4;

-- Stored Procedures 
DELIMITER ;;
DROP PROCEDURE IF EXISTS `add`;;

CREATE DEFINER=`root`@`localhost` PROCEDURE `add`(
IN comp_name VARCHAR(45),
IN pingVal INT,
IN timeStem datetime
)
BEGIN

	DECLARE isAppear INT;
    START transaction;
	select Count(compName) into isAppear from ping_management.comps where compName = comp_name ;

		IF isAppear = 0 THEN 
			INSERT INTO ping_management.comps (compName)  VALUES (comp_name ); 
		END IF;
		INSERT INTO ping_management.pings (compName, ping, timeOfResponce)  VALUES (comp_name, pingVal, timeStem);
		
	 commit;

END ;;

DROP PROCEDURE IF EXISTS `delete`;

CREATE DEFINER=`root`@`localhost` PROCEDURE `delete`(
IN comp_name NVARCHAR(45),
OUT row_effected INT
)
BEGIN
SET SQL_SAFE_UPDATES=0;
START transaction;
DELETE FROM ping_management.pings WHERE compName = comp_name;
DELETE FROM ping_management.comps WHERE compName = comp_name;
SET row_effected =  ROW_COUNT();
COMMIT;
END ;;
DELIMITER ;