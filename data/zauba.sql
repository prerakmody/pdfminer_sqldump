-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: localhost    Database: zauba
-- ------------------------------------------------------
-- Server version	5.7.20-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `zauba_mca`
--

DROP TABLE IF EXISTS `zauba_mca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zauba_mca` (
  `srn` varchar(16) DEFAULT NULL,
  `service_request_date` date DEFAULT NULL,
  `payment_made_into` varchar(128) DEFAULT NULL,
  `name` varchar(128) DEFAULT NULL,
  `address` varchar(512) DEFAULT NULL,
  `service_type` varchar(128) DEFAULT NULL,
  `service_description` varchar(512) DEFAULT NULL,
  `fee_type` varchar(32) DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `total` float DEFAULT NULL,
  `payment_mode` varchar(128) DEFAULT NULL,
  `received_payment_rupees` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zauba_mca`
--

LOCK TABLES `zauba_mca` WRITE;
/*!40000 ALTER TABLE `zauba_mca` DISABLE KEYS */;
INSERT INTO `zauba_mca` VALUES ('U16571275','2017-08-03','ICICI BANK','Zauba Technologies and Data Services Privat','No 1/10, II Floor, Near Gate No 9 APMC Yard, Yeshwanthpur Bangalore , Karnataka India - 00560022 ','Fee for inspection of Public documents','Inspection of Public documents of KEYSTONE  REALTORS PRIVATE LIMITED ( U45200MH1995PTC094208  )','Normal',100,100,'Credit Card/Prepaid Card - ICICI Bank','One Hundred Only\r'),('U16572745','2017-08-03','ICICI BANK','Zauba Technologies and Data Services Privat','No 1/10, II Floor, Near Gate No 9 APMC Yard, Yeshwanthpur Bangalore , Karnataka India - 00560022 ','Fee for inspection of Public documents','Inspection of Public documents of LANDMARK  CRAFTS PRIVATE LIMITED  ( U74999DL2007PTC163299  )','Normal',100,100,'Credit Card/Prepaid Card - ICICI Bank','One Hundred Only\r'),('U16573131','2017-08-03','ICICI BANK','Zauba Technologies and Data Services Privat','No 1/10, II Floor, Near Gate No 9 APMC Yard, Yeshwanthpur Bangalore , Karnataka India - 00560022 ','Fee for inspection of Public documents','Inspection of Public documents of WESNIA INFO  SOLUTIONS PRIVATE LIMITED ( U72200KA2006PTC039676  )','Normal',100,100,'Credit Card/Prepaid Card - ICICI Bank','One Hundred Only\r'),('U22212252','2017-12-28','HDFC BANK','PRERAK MODY','51, Gaurav Apts, Sayani Road, Prabhadevi Mumbai , Maharashtra\nIN - 00400025\n','Fee for inspection of Public documents','Inspection of Public documents of VICARA  INFOTECH PRIVATE LIMITED ( U72200DL2010PTC201590  )','Normal',100,100,'Internet Banking - HDFC Bank','One Hundred Only\r');
/*!40000 ALTER TABLE `zauba_mca` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-12-30 16:19:19
