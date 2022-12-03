CREATE DATABASE IF NOT EXISTS `hotel_system`; 
USE `hotel_system`;

DROP TABLE IF EXISTS `hotel`;
CREATE TABLE `hotel` (
  `hotelID` int NOT NULL auto_increment,
  `hotel_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`hotelID`)
);

DROP TABLE IF EXISTS `room`;
CREATE TABLE `room` (
  `room_num` INT NOT NULL DEFAULT 1,
  `price` FLOAT DEFAULT NULL,
  `room_type` ENUM('single', 'double'),
  PRIMARY KEY (`room_num`, `hotelID`),
  FOREIGN KEY (`hotelID`) REFERENCES `hotel`(`hotelID`)
) ;

DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer` (
  `Email_address` varchar(20) DEFAULT ' ',
  `password` varchar (100) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`Email_address`)
);

DROP TABLE IF EXISTS `reservation`;
CREATE TABLE `reservation` (
  `invoice` INT NOT NULL auto_increment,
  `Email_address` varchar(50) DEFAULT NULL,
  `check_in` DATE NOT NULL,
  PRIMARY KEY (`invoice`),
  FOREIGN KEY (`Email_address`) REFERENCES `customer`(`Email_address`)
);
