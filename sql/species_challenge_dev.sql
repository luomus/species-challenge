-- MariaDB dump 10.19  Distrib 10.5.23-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: species_challenge_dev
-- ------------------------------------------------------
-- Server version	10.5.23-MariaDB-1:10.5.23+maria~ubu2004

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `species_challenge_dev`
--


USE `species_challenge_rahti`;

--
-- Table structure for table `challenges`
--

DROP TABLE IF EXISTS `challenges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `challenges` (
  `challenge_id` int(11) NOT NULL AUTO_INCREMENT,
  `taxon` varchar(16) NOT NULL,
  `autocomplete` varchar(256) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `type` varchar(16) NOT NULL,
  `title` varchar(255) NOT NULL,
  `status` varchar(8) NOT NULL,
  `description` varchar(2048) DEFAULT NULL,
  `meta_created_by` varchar(16) NOT NULL,
  `meta_created_at` datetime NOT NULL,
  `meta_edited_by` varchar(16) NOT NULL,
  `meta_edited_at` datetime NOT NULL,
  PRIMARY KEY (`challenge_id`),
  KEY `status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `challenges`
--

LOCK TABLES `challenges` WRITE;
/*!40000 ALTER TABLE `challenges` DISABLE KEYS */;
INSERT INTO `challenges` VALUES (1,'MX.37601_2024',NULL,2024,'challenge100','Hyönteiset 2024','draft',NULL,'MA.3','2024-01-28 10:39:59','MA.3','2024-01-28 10:39:59'),(2,'MX.37601_2024','',2024,'challenge100','Sienet 2024','draft','Kuka havaitsee vuoden aikana eniten lajeja omalla kotikunnassaan? Perinteinen kuntahaaste on avoin kilpailu kaikille alueen asukkaille.\r\n\r\nLiikkumistavaksi suositellaan ekovaihtoehtoja, mutta kaikki liikkumistavat ovat kuitenkin sallittuja. Lorem ipsum dolor sit amet. Liikkumistavaksi suositellaan ekovaihtoehtoja, mutta kaikki liikkumistavat ovat kuitenkin sallittuja. Lorem ipsum dolor sit amet.','MA.3','2024-01-28 10:39:59','MA.3','2024-02-09 08:07:10'),(3,'MX.37601_2024','',2023,'challenge100','Sienet 2023','draft','','MA.3','2024-01-28 10:41:49','MA.3','2024-02-09 08:06:58'),(4,'MX.37601_2024','MVL.343,MVL.23',2024,'challenge100','Kasvit 2024','open','<img src=\'/static/images/icon_plantae_100.png\'>\r\n\r\nHavaitse 100 kasvilajia vuodessa!\r\n<p>\r\n<a href=\"https://pinkka.laji.fi/pinkat/#/\">Lue lisää haasteen lajeista Pinkasta</a>.','MA.3','2024-01-28 10:42:23','MA.3','2024-02-08 20:02:52'),(5,'MX.37601_2024','MVL.343,MVL.23',2024,'challenge100','Sienihaaste 2024 Playwright','open','<img src=\'/static/images/icon_fungi_100.png\'>\r\n\r\nHavaitse 100 sienilajia vuodessa!','MA.3','2024-01-28 22:32:58','MA.3','2024-02-09 08:21:14'),(6,'MX.37601_2024','',2024,'challenge100','100 hyönteislajia 2024','open','<img src=\'/static/images/icon_insecta_100.png\'>\r\n\r\nHavaitse 100 hyönteislajia vuodessa!','MA.3','2024-01-28 22:33:44','MA.3','2024-02-08 20:03:51'),(7,'MX.37601_2024',NULL,2000,'challenge100','Testi','draft','Testi','MA.3','2024-01-30 14:58:59','MA.3','2024-01-30 14:58:59'),(8,'MX.37601_2024',NULL,2000,'challenge100','Testi','draft','Testi','MA.3','2024-01-30 14:59:56','MA.3','2024-01-30 14:59:56'),(9,'MX.37601_2024',NULL,2000,'challenge100','Testi','draft','Testi','MA.3','2024-01-30 15:02:14','MA.3','2024-01-30 15:02:14'),(10,'MX.37601_2024',NULL,2001,'challenge100','simplified Chinese 汉语 traditional Chinese 漢語','draft','simplified Chinese: 汉语; traditional Chinese: 漢語;','MA.3','2024-01-30 15:11:19','MA.3','2024-01-30 15:14:52'),(11,'MX.37601_2024',NULL,2024,'challenge100','Temp','draft','Temp','MA.3','2024-01-30 15:49:13','MA.3','2024-01-30 15:49:13');
/*!40000 ALTER TABLE `challenges` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `participations`
--

DROP TABLE IF EXISTS `participations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `participations` (
  `participation_id` int(11) NOT NULL AUTO_INCREMENT,
  `challenge_id` int(11) NOT NULL,
  `name` varchar(128) NOT NULL,
  `place` varchar(128) DEFAULT NULL,
  `taxa_count` int(11) DEFAULT NULL,
  `taxa_json` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`taxa_json`)),
  `meta_created_by` varchar(16) NOT NULL,
  `meta_created_at` datetime NOT NULL,
  `meta_edited_by` varchar(16) NOT NULL,
  `meta_edited_at` datetime NOT NULL,
  `trashed` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`participation_id`),
  KEY `challenge_id` (`challenge_id`),
  KEY `meta_created_by` (`meta_created_by`),
  KEY `taxa_count` (`taxa_count`),
  FULLTEXT KEY `taxa_json_fulltext` (`taxa_json`),
  CONSTRAINT `participations_ibfk_1` FOREIGN KEY (`challenge_id`) REFERENCES `challenges` (`challenge_id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `participations`
--

LOCK TABLES `participations` WRITE;
/*!40000 ALTER TABLE `participations` DISABLE KEYS */;
INSERT INTO `participations` VALUES (1,2,'Testaaja 2','Helsinki 2',0,'{}','MA.3','2024-01-28 10:47:46','MA.3','2024-01-31 12:53:43',1),(2,2,'Teppo Testaaja','Vantaa',0,NULL,'MA.3','2024-01-28 10:51:00','MA.3','2024-01-28 10:51:03',0),(3,2,'Ulla Uusmäki-Vanhalaakso','Outokumpu, kummun takana',0,NULL,'MA.3','2024-01-28 13:53:50','MA.3','2024-01-28 13:54:36',0),(4,2,'Untamo Ikämies-Akana','Akaa-Loimaa',0,NULL,'MA.3','2024-01-28 13:54:52','MA.3','2024-01-28 15:18:24',0),(5,4,'Nimi Merkkinen','Nimismiehenkylä',38,'{\"MX.43922\": \"2024-02-01\", \"MX.43502\": \"2024-02-05\", \"MX.43901\": \"2024-02-05\", \"MX.43956\": \"2024-02-05\", \"MX.44366\": \"2024-02-06\", \"MX.37691\": \"2024-01-30\", \"MX.37717\": \"2024-01-17\", \"MX.37719\": \"2024-01-25\", \"MX.37763\": \"2024-01-01\", \"MX.37771\": \"2024-01-30\", \"MX.37752\": \"2024-01-30\", \"MX.37826\": \"2024-01-30\", \"MX.37812\": \"2024-01-10\", \"MX.37819\": \"2024-01-30\", \"MX.39201\": \"2024-01-30\", \"MX.39235\": \"2024-01-30\", \"MX.39761\": \"2024-02-02\", \"MX.39871\": \"2024-02-06\", \"MX.39887\": \"2024-01-30\", \"MX.39917\": \"2024-01-11\", \"MX.38364\": \"2024-02-06\", \"MX.38279\": \"2024-01-02\", \"MX.38598\": \"2024-01-13\", \"MX.39052\": \"2024-01-20\", \"MX.39038\": \"2024-01-11\", \"MX.39465\": \"2024-01-18\", \"MX.39673\": \"2024-01-30\", \"MX.4994055\": \"2024-01-03\", \"MX.37747\": \"2024-01-30\", \"MX.40138\": \"2024-01-30\", \"MX.4973227\": \"2024-01-17\", \"MX.39967\": \"2024-01-30\", \"MX.38301\": \"2024-01-30\", \"MX.40632\": \"2024-01-11\", \"MX.38843\": \"2024-01-25\", \"MX.40643\": \"2024-02-05\", \"MX.39687\": \"2024-02-06\", \"MX.40028\": \"2024-02-08\"}','MA.3','2024-01-28 15:19:17','MA.3','2024-02-08 19:44:08',0),(6,4,'André D\'Artágnan','Ääkkölä ääkkölärules',33,'{\"MX.43668\": \"2024-02-02\", \"MX.43901\": \"2024-02-07\", \"MX.43933\": \"2024-02-01\", \"MX.37691\": \"2024-01-11\", \"MX.37721\": \"2024-01-02\", \"MX.37717\": \"2024-01-27\", \"MX.37719\": \"2024-01-28\", \"MX.37763\": \"2024-01-10\", \"MX.37771\": \"2024-01-18\", \"MX.37752\": \"2024-01-30\", \"MX.39201\": \"2024-01-30\", \"MX.39827\": \"2024-01-25\", \"MX.39703\": \"2024-02-02\", \"MX.39711\": \"2024-02-02\", \"MX.38364\": \"2024-02-02\", \"MX.38387\": \"2024-02-02\", \"MX.38795\": \"2024-01-01\", \"MX.38869\": \"2024-02-02\", \"MX.38834\": \"2024-02-02\", \"MX.38863\": \"2024-02-02\", \"MX.38939\": \"2024-02-01\", \"MX.38797\": \"2024-02-02\", \"MX.38802\": \"2024-02-02\", \"MX.37984\": \"2024-02-02\", \"MX.39122\": \"2024-02-02\", \"MX.38750\": \"2024-02-02\", \"MX.4994055\": \"2024-01-18\", \"MX.40138\": \"2024-01-30\", \"MX.40150\": \"2024-01-30\", \"MX.4973227\": \"2024-01-17\", \"MX.4984037\": \"2024-02-02\", \"MX.39750\": \"2024-01-10\", \"MX.38820\": \"2024-02-02\"}','MA.3','2024-01-28 15:29:01','MA.3','2024-02-07 10:33:45',0),(7,5,'Nollanen','Peräkyläntaka',3,'{\"MX.43922\": \"2024-02-09\", \"MX.37812\": \"2024-02-09\", \"MX.37819\": \"2024-02-09\"}','MA.3','2024-01-29 21:13:01','MA.3','2024-02-09 09:24:59',0),(8,4,'Meikäläinen','Meikäläisenkylä',9,'{\"MX.37721\": \"2024-01-11\", \"MX.37719\": \"2024-01-16\", \"MX.39201\": \"2024-01-31\", \"MX.39761\": \"2024-01-01\", \"MX.39823\": \"2024-01-31\", \"MX.39328\": \"2024-01-31\", \"MX.38048\": \"2024-01-10\", \"MX.39889\": \"2024-01-30\", \"MX.38004\": \"2024-02-08\"}','MA.3','2024-01-30 15:48:29','MA.3','2024-02-09 08:20:48',0),(9,4,'Teppo Testaaja','Testipaikka',7,'{\"MX.43922\": \"2024-01-01\", \"MX.43956\": \"2024-02-06\", \"MX.39976\": \"2024-02-01\", \"MX.39890\": \"2024-01-17\", \"MX.38048\": \"2024-01-17\", \"MX.38263\": \"2024-01-06\", \"MX.39158\": \"2024-01-06\"}','MA.315','2024-02-05 12:02:33','MA.315','2024-02-06 07:20:10',0),(10,5,'Playwright','Näyttämö',0,'{}','MA.315','2024-02-05 12:24:29','MA.315','2024-02-05 12:24:52',1),(11,5,'Playwright','Näyttämö',1,'{\"MX.43922\": \"2024-01-01\"}','MA.315','2024-02-05 12:25:08','MA.315','2024-02-05 12:28:25',1),(12,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-05 12:28:35','MA.315','2024-02-05 12:29:29',1),(13,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-05 12:31:39','MA.315','2024-02-05 12:31:42',1),(14,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-05 12:32:56','MA.315','2024-02-05 12:32:57',1),(15,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-05 12:44:45','MA.315','2024-02-05 12:44:46',1),(16,4,'sadsa','asdsa',0,'{}','MA.315','2024-02-05 15:13:26','MA.315','2024-02-05 15:13:31',1),(17,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-05 18:49:14','MA.315','2024-02-05 18:49:14',1),(18,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-05 20:49:17','MA.315','2024-02-05 20:49:17',1),(19,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-05 21:45:11','MA.315','2024-02-05 21:45:11',1),(20,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-05 21:59:20','MA.315','2024-02-05 21:59:21',1),(21,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-06 16:18:39','MA.315','2024-02-06 16:18:39',1),(22,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-06 18:30:15','MA.315','2024-02-06 18:30:16',1),(23,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-06 21:40:55','MA.315','2024-02-06 21:40:56',1),(24,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-06 21:41:38','MA.315','2024-02-06 21:41:39',1),(25,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-06 21:43:23','MA.315','2024-02-06 21:43:24',1),(26,4,'Testi','Testi',0,'{}','MA.3','2024-02-07 10:42:44','MA.3','2024-02-07 10:47:15',1),(27,4,'Testi','Testipaikka',8,'{\"MX.43922\": \"2024-02-07\", \"MX.43901\": \"2024-01-17\", \"MX.44366\": \"2024-02-07\", \"MX.37691\": \"2024-02-07\", \"MX.37721\": \"2024-02-07\", \"MX.37763\": \"2024-02-07\", \"MX.37771\": \"2024-02-07\", \"MX.39687\": \"2024-02-07\"}','MA.3','2024-02-07 11:06:59','MA.3','2024-02-07 11:08:16',1),(28,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-07 12:05:49','MA.315','2024-02-07 12:05:50',1),(29,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-07 13:48:36','MA.315','2024-02-07 13:48:36',1),(30,6,'Testi','Temp',0,'{}','MA.3','2024-02-07 17:19:52','MA.3','2024-02-07 17:20:06',1),(31,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-08 07:02:44','MA.315','2024-02-08 07:02:44',1),(32,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-09 08:14:36','MA.315','2024-02-09 08:14:36',1),(33,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-09 08:15:26','MA.315','2024-02-09 08:15:28',1),(34,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-09 08:16:27','MA.315','2024-02-09 08:16:28',1),(35,5,'Testi Äläpoista','Playwright-paikka',2,'{\"MX.43922\": \"2024-02-09\", \"MX.39687\": \"2024-02-09\"}','MA.3','2024-02-09 08:23:23','MA.3','2024-02-09 08:24:19',0),(36,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-09 08:44:33','MA.315','2024-02-09 08:44:33',1),(37,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-09 08:45:12','MA.315','2024-02-09 08:45:12',1),(38,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-09 08:47:54','MA.315','2024-02-09 08:47:55',1),(39,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-09 09:00:12','MA.315','2024-02-09 09:00:12',1),(40,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-09 09:01:17','MA.315','2024-02-09 09:01:18',1),(41,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-09 09:01:57','MA.315','2024-02-09 09:01:58',1),(42,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-09 09:07:29','MA.315','2024-02-09 09:07:29',1),(43,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-09 09:10:32','MA.315','2024-02-09 09:10:32',1),(44,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-09 09:10:59','MA.315','2024-02-09 09:11:00',1),(45,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-09 09:13:53','MA.315','2024-02-09 09:13:54',1),(46,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-01-02\"}','MA.315','2024-02-09 09:14:24','MA.315','2024-02-09 09:14:25',1),(47,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-02-09\"}','MA.315','2024-02-09 09:16:55','MA.315','2024-02-09 09:16:55',1),(48,5,'Playwright','Näyttämö',1,'{\"MX.43502\": \"2024-02-09\"}','MA.315','2024-02-09 09:21:26','MA.315','2024-02-09 09:21:27',1);
/*!40000 ALTER TABLE `participations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-01  9:45:56
