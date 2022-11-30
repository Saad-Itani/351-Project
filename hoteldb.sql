CREATE DATABASE IF NOT EXISTS `HOTELDB`; 
USE `HOTELDB`;

-- Table structure for table `hotel`
--

DROP TABLE IF EXISTS `hotel`;
CREATE TABLE `hotel` (
  `hotelID` int NOT NULL auto_increment,
  `hotel_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`hotelID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- -- /*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `HotelPhoneNumbers`
--
DROP TABLE IF EXISTS `HotelPhoneNumbers`;
CREATE TABLE `HotelPhoneNumbers` (
  `hotelID` int NOT NULL DEFAULT 1,
  `phone_no` varchar(30) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`hotelID`, `phone_no`),
  FOREIGN KEY (`hotelID`) REFERENCES `hotel`(`hotelID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- -- /*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `myroom`;
CREATE TABLE `myroom` (
  `room_num` INT NOT NULL DEFAULT 1,
  `hotelID` INT NOT NULL DEFAULT 1,
  `price` FLOAT DEFAULT NULL,
  `capacity` INT DEFAULT NULL,
  `floor_no` INT NOT NULL DEFAULT 1,
  `description` varchar(250) DEFAULT NULL,
  `room_type` ENUM('standard','double','deluxe','suite'),
  PRIMARY KEY (`room_num`, `hotelID`),
  FOREIGN KEY (`hotelID`) REFERENCES `hotel`(`hotelID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer` (
  `CID` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT ' ',
  `password` varchar (100) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `PHONE_NUM` int DEFAULT NULL,
  PRIMARY KEY (`CID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Table structure for table `reservation`
--
DROP TABLE IF EXISTS `reservation`;
-- -- /*!40101 SET @saved_cs_client     = @@character_set_client */;
-- -- /*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reservation` (
  `invoiceNo` INT NOT NULL auto_increment,
  `CID` INT NOT NULL DEFAULT 1,
  `totalAmt` FLOAT DEFAULT NULL,
  `resDate` DATE NOT NULL DEFAULT '2008-7-04',
  PRIMARY KEY (`invoiceNO`),
  FOREIGN KEY (`CID`) REFERENCES `customer`(`CID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Table structure for table `reserves`
--
DROP TABLE IF EXISTS `reserves`;
-- -- /*!40101 SET @saved_cs_client     = @@character_set_client */;
-- -- /*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reserves` (
  `invoiceNo` INT NOT NULL DEFAULT 1,
  `room_num` INT NOT NULL DEFAULT 1,
  `hotelID` INT NOT NULL DEFAULT 1,
  `noOfDays` INT DEFAULT NULL,
  `inDate` DATE NOT NULL DEFAULT '2008-7-04',
  `outDate` DATE NOT NULL DEFAULT '2008-7-04',
  PRIMARY KEY (`invoiceNo`,`room_num`,`hotelID`),
  FOREIGN KEY (`invoiceNo`) REFERENCES `reservation`(`invoiceNo`),
  FOREIGN KEY (`room_num`,`hotelID`) REFERENCES `myroom`(`room_num`,`hotelID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Table structure for table `review`
--
DROP TABLE IF EXISTS `review`;
CREATE TABLE `review` (
  `reviewID` int NOT NULL auto_increment,
  `CID` int NOT NULL DEFAULT 1,
  `rating` int DEFAULT NULL,
  `title` varchar (100) DEFAULT NULL,
  `textcomment` varchar(1028) DEFAULT NULL,
  `review_type` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`reviewID`),
  FOREIGN KEY (`CID`) REFERENCES `customer`(`CID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Table structure for table `room_review`
--
DROP TABLE IF EXISTS `room_review`;
CREATE TABLE `room_review` (
  `reviewID` int NOT NULL DEFAULT 1,
  `room_num` int DEFAULT NULL,
  `hotelID` int DEFAULT NULL,
  PRIMARY KEY (`reviewID`),
  FOREIGN KEY (`reviewID`) REFERENCES `review`(`reviewID`),
  FOREIGN KEY (`room_num`,`hotelID`) REFERENCES `myroom`(`room_num`,`hotelID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- /*!40101 SET character_set_client = @saved_cs_client */;


DROP TABLE IF EXISTS `includes`;
CREATE TABLE `includes` (
  `invoiceNo` INT NOT NULL DEFAULT 1,
  `hotelID` INT NOT NULL DEFAULT 1,
  `bType` varchar(20) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`invoiceNo`,`bType`,`hotelID`),
  FOREIGN KEY (`invoiceNo`) REFERENCES `reservation`(`invoiceNo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `contains`;
CREATE TABLE `contains` (
  `invoiceNo` INT NOT NULL DEFAULT 1,
  `num_of_services` INT NOT NULL DEFAULT 1,
  `hotelID` INT NOT NULL DEFAULT 1,
  PRIMARY KEY (`invoiceNo`,`sType`,`hotelID`),
  FOREIGN KEY (`invoiceNo`) REFERENCES `reservation`(`invoiceNo`),
  FOREIGN KEY (`sType`,`hotelID`) REFERENCES `services`(`sType`,`hotelID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



--
-- Table structure for table creditcard
--
DROP TABLE IF EXISTS `creditcard`;
-- /*!40101 SET @saved_cs_client     = @@character_set_client */;
-- /*!40101 SET character_set_client = utf8 */;
CREATE TABLE `creditcard` (
  `CNumber` INT NOT NULL DEFAULT 1,
  `CID` INT NOT NULL DEFAULT 1,
  `InvoiceNo` INT NOT NULL DEFAULT 1,
  `Name` varchar(30) DEFAULT NULL,
  `ExpDate` DATE DEFAULT NULL,
  `Type` varchar (20) DEFAULT NULL,
  `SecCode` INT NOT NULL DEFAULT 1,
  `BillingAddr` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`CNumber`, `CID`, `InvoiceNo`),
  FOREIGN KEY (`CID`) REFERENCES `customer`(`CID`),
  FOREIGN KEY (`InvoiceNo`) REFERENCES `reservation`(`invoiceNo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- /*!40101 SET character_set_client = @saved_cs_client */;

select * from hoteldb
