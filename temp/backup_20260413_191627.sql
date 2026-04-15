-- MySQL dump 10.13  Distrib 8.0.37, for Win64 (x86_64)
--
-- Host: localhost    Database: LA_RESPUESTA
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `canal`
--

DROP TABLE IF EXISTS `canal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `canal` (
  `idCanal` int NOT NULL AUTO_INCREMENT,
  `idCategoria` int NOT NULL,
  `idOrdenCompra` int NOT NULL,
  `Descripcion` varchar(200) DEFAULT NULL,
  `Peso` float DEFAULT NULL,
  `fechaSacrificio` date NOT NULL,
  `fechaCaducidad` date DEFAULT NULL,
  `estatus` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`idCanal`),
  KEY `idCategoria` (`idCategoria`),
  KEY `idOrdenCompra` (`idOrdenCompra`),
  CONSTRAINT `canal_ibfk_1` FOREIGN KEY (`idCategoria`) REFERENCES `categoria` (`idCategoria`),
  CONSTRAINT `canal_ibfk_2` FOREIGN KEY (`idOrdenCompra`) REFERENCES `orden_compra` (`idOrdenCompra`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `canal`
--

LOCK TABLES `canal` WRITE;
/*!40000 ALTER TABLE `canal` DISABLE KEYS */;
INSERT INTO `canal` VALUES (1,2,1,'Canal de cerdo completa',160,'2026-04-13','2026-04-20','Disponible'),(2,1,5,'Canal de res completa',250,'2026-04-13','2026-04-20','Disponible'),(3,1,5,'Canal de res completa',250,'2026-04-13','2026-04-20','Disponible'),(4,3,6,'Pollo entero fresco',2,'2026-04-13','2026-04-20','Disponible'),(5,3,6,'Pollo entero fresco',2,'2026-04-13','2026-04-20','Disponible'),(6,4,7,'Canal de cordero',125,'2026-04-13','2026-04-20','Disponible');
/*!40000 ALTER TABLE `canal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `canal_corte`
--

DROP TABLE IF EXISTS `canal_corte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `canal_corte` (
  `idCanalCorte` int NOT NULL AUTO_INCREMENT,
  `idCorte` int NOT NULL,
  `idCanal` int NOT NULL,
  `CantidadEsperada` float DEFAULT NULL,
  `CantidadObtenida` float DEFAULT NULL,
  `Merma` float DEFAULT NULL,
  `estatus` varchar(20) NOT NULL,
  PRIMARY KEY (`idCanalCorte`),
  KEY `idCorte` (`idCorte`),
  KEY `idCanal` (`idCanal`),
  CONSTRAINT `canal_corte_ibfk_1` FOREIGN KEY (`idCorte`) REFERENCES `corte` (`idCorte`),
  CONSTRAINT `canal_corte_ibfk_2` FOREIGN KEY (`idCanal`) REFERENCES `canal` (`idCanal`)
) ENGINE=InnoDB AUTO_INCREMENT=229 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `canal_corte`
--

LOCK TABLES `canal_corte` WRITE;
/*!40000 ALTER TABLE `canal_corte` DISABLE KEYS */;
INSERT INTO `canal_corte` VALUES (1,46,1,14.4,13,1.4,'Consumido'),(2,47,1,6.4,NULL,NULL,'Disponible'),(3,48,1,4.8,NULL,NULL,'Disponible'),(4,49,1,4.8,NULL,NULL,'Disponible'),(5,50,1,1.6,NULL,NULL,'Disponible'),(6,51,1,1.6,NULL,NULL,'Disponible'),(7,52,1,1.6,NULL,NULL,'Disponible'),(8,53,1,1.6,NULL,NULL,'Disponible'),(9,54,1,10.4,NULL,NULL,'Disponible'),(10,55,1,7.2,7.125,0.075,'Consumido'),(11,56,1,3.2,NULL,NULL,'Disponible'),(12,57,1,1.6,NULL,NULL,'Disponible'),(13,58,1,1.6,NULL,NULL,'Disponible'),(14,59,1,1.6,NULL,NULL,'Disponible'),(15,60,1,1.6,NULL,NULL,'Disponible'),(16,61,1,7.2,NULL,NULL,'Disponible'),(17,62,1,6.4,NULL,NULL,'Disponible'),(18,63,1,4.8,NULL,NULL,'Disponible'),(19,64,1,1.6,NULL,NULL,'Disponible'),(20,65,1,1.6,NULL,NULL,'Disponible'),(21,66,1,6.4,NULL,NULL,'Disponible'),(22,67,1,3.2,NULL,NULL,'Disponible'),(23,68,1,3.2,NULL,NULL,'Disponible'),(24,69,1,1.6,NULL,NULL,'Disponible'),(25,70,1,1.6,NULL,NULL,'Disponible'),(26,71,1,0.8,NULL,NULL,'Disponible'),(27,72,1,11.2,NULL,NULL,'Disponible'),(28,73,1,4.8,NULL,NULL,'Disponible'),(29,74,1,4.8,NULL,NULL,'Disponible'),(30,75,1,3.2,NULL,NULL,'Disponible'),(31,76,1,1.6,NULL,NULL,'Disponible'),(32,77,1,1.6,NULL,NULL,'Disponible'),(33,78,1,0.8,NULL,NULL,'Disponible'),(34,79,1,0.32,NULL,NULL,'Disponible'),(35,80,1,0.64,NULL,NULL,'Disponible'),(36,81,1,0.64,NULL,NULL,'Disponible'),(37,82,1,3.2,NULL,NULL,'Disponible'),(38,83,1,1.6,NULL,NULL,'Disponible'),(39,84,1,1.6,NULL,NULL,'Disponible'),(40,85,1,0.8,NULL,NULL,'Disponible'),(41,86,1,0.8,NULL,NULL,'Disponible'),(42,87,1,1.6,NULL,NULL,'Disponible'),(43,88,1,1.6,NULL,NULL,'Disponible'),(44,89,1,1.6,NULL,NULL,'Disponible'),(45,90,1,0.8,NULL,NULL,'Disponible'),(46,91,1,3.2,NULL,NULL,'Disponible'),(47,92,1,1.6,NULL,NULL,'Disponible'),(48,93,1,1.6,NULL,NULL,'Disponible'),(49,95,1,3.2,NULL,NULL,'Disponible'),(50,96,1,1.6,NULL,NULL,'Disponible'),(51,97,1,1.6,NULL,NULL,'Disponible'),(52,1,2,16.25,NULL,NULL,'Disponible'),(53,2,2,7.5,NULL,NULL,'Disponible'),(54,3,2,10,NULL,NULL,'Disponible'),(55,4,2,7.5,NULL,NULL,'Disponible'),(56,5,2,3.75,NULL,NULL,'Disponible'),(57,6,2,2.5,NULL,NULL,'Disponible'),(58,7,2,5,NULL,NULL,'Disponible'),(59,8,2,12.5,NULL,NULL,'Disponible'),(60,9,2,8.75,NULL,NULL,'Disponible'),(61,10,2,8.75,NULL,NULL,'Disponible'),(62,11,2,3.75,NULL,NULL,'Disponible'),(63,12,2,3.75,3,0.75,'Consumido'),(64,13,2,6.25,NULL,NULL,'Disponible'),(65,14,2,2,NULL,NULL,'Disponible'),(66,15,2,1.75,NULL,NULL,'Disponible'),(67,16,2,7.5,NULL,NULL,'Disponible'),(68,17,2,5,NULL,NULL,'Disponible'),(69,18,2,6.25,NULL,NULL,'Disponible'),(70,19,2,5,NULL,NULL,'Disponible'),(71,20,2,2.5,NULL,NULL,'Disponible'),(72,21,2,6.25,NULL,NULL,'Disponible'),(73,22,2,3.75,NULL,NULL,'Disponible'),(74,23,2,1.75,NULL,NULL,'Disponible'),(75,24,2,16.25,NULL,NULL,'Disponible'),(76,25,2,12.5,NULL,NULL,'Disponible'),(77,26,2,5,NULL,NULL,'Disponible'),(78,27,2,7.5,NULL,NULL,'Disponible'),(79,28,2,3.75,NULL,NULL,'Disponible'),(80,29,2,5,NULL,NULL,'Disponible'),(81,30,2,3.75,NULL,NULL,'Disponible'),(82,32,2,7.5,7.2,0.3,'Consumido'),(83,33,2,5,NULL,NULL,'Disponible'),(84,34,2,5,NULL,NULL,'Disponible'),(85,35,2,2.5,NULL,NULL,'Disponible'),(86,36,2,6.25,NULL,NULL,'Disponible'),(87,37,2,8.75,NULL,NULL,'Disponible'),(88,38,2,2.5,NULL,NULL,'Disponible'),(89,40,2,5,NULL,NULL,'Disponible'),(90,41,2,2.5,NULL,NULL,'Disponible'),(91,42,2,1.25,NULL,NULL,'Disponible'),(92,43,2,3.75,NULL,NULL,'Disponible'),(93,44,2,2.5,NULL,NULL,'Disponible'),(94,45,2,1.25,NULL,NULL,'Disponible'),(95,1,3,16.25,NULL,NULL,'Disponible'),(96,2,3,7.5,NULL,NULL,'Disponible'),(97,3,3,10,NULL,NULL,'Disponible'),(98,4,3,7.5,NULL,NULL,'Disponible'),(99,5,3,3.75,NULL,NULL,'Disponible'),(100,6,3,2.5,NULL,NULL,'Disponible'),(101,7,3,5,NULL,NULL,'Disponible'),(102,8,3,12.5,NULL,NULL,'Disponible'),(103,9,3,8.75,NULL,NULL,'Disponible'),(104,10,3,8.75,NULL,NULL,'Disponible'),(105,11,3,3.75,NULL,NULL,'Disponible'),(106,12,3,3.75,NULL,NULL,'Disponible'),(107,13,3,6.25,NULL,NULL,'Disponible'),(108,14,3,2,1.95,0.05,'Consumido'),(109,15,3,1.75,NULL,NULL,'Disponible'),(110,16,3,7.5,NULL,NULL,'Disponible'),(111,17,3,5,NULL,NULL,'Disponible'),(112,18,3,6.25,NULL,NULL,'Disponible'),(113,19,3,5,NULL,NULL,'Disponible'),(114,20,3,2.5,NULL,NULL,'Disponible'),(115,21,3,6.25,NULL,NULL,'Disponible'),(116,22,3,3.75,NULL,NULL,'Disponible'),(117,23,3,1.75,NULL,NULL,'Disponible'),(118,24,3,16.25,16.2,0.05,'Consumido'),(119,25,3,12.5,NULL,NULL,'Disponible'),(120,26,3,5,NULL,NULL,'Disponible'),(121,27,3,7.5,NULL,NULL,'Disponible'),(122,28,3,3.75,NULL,NULL,'Disponible'),(123,29,3,5,NULL,NULL,'Disponible'),(124,30,3,3.75,NULL,NULL,'Disponible'),(125,32,3,7.5,7.2,0.3,'Consumido'),(126,33,3,5,NULL,NULL,'Disponible'),(127,34,3,5,NULL,NULL,'Disponible'),(128,35,3,2.5,NULL,NULL,'Disponible'),(129,36,3,6.25,NULL,NULL,'Disponible'),(130,37,3,8.75,NULL,NULL,'Disponible'),(131,38,3,2.5,NULL,NULL,'Disponible'),(132,40,3,5,NULL,NULL,'Disponible'),(133,41,3,2.5,NULL,NULL,'Disponible'),(134,42,3,1.25,NULL,NULL,'Disponible'),(135,43,3,3.75,NULL,NULL,'Disponible'),(136,44,3,2.5,NULL,NULL,'Disponible'),(137,45,3,1.25,NULL,NULL,'Disponible'),(138,98,4,0.36,0.31,0.05,'Consumido'),(139,99,4,0.12,NULL,NULL,'Disponible'),(140,100,4,0.08,NULL,NULL,'Disponible'),(141,101,4,0.04,NULL,NULL,'Disponible'),(142,102,4,0.04,NULL,NULL,'Disponible'),(143,103,4,0.28,NULL,NULL,'Disponible'),(144,104,4,0.2,NULL,NULL,'Disponible'),(145,105,4,0.12,NULL,NULL,'Disponible'),(146,106,4,0.06,NULL,NULL,'Disponible'),(147,107,4,0.04,NULL,NULL,'Disponible'),(148,108,4,0.12,NULL,NULL,'Disponible'),(149,109,4,0.04,NULL,NULL,'Disponible'),(150,110,4,0.04,NULL,NULL,'Disponible'),(151,111,4,0.04,NULL,NULL,'Disponible'),(152,112,4,0.12,NULL,NULL,'Disponible'),(153,113,4,0.04,NULL,NULL,'Disponible'),(154,114,4,0.02,NULL,NULL,'Disponible'),(155,115,4,0.04,NULL,NULL,'Disponible'),(156,116,4,0.04,NULL,NULL,'Disponible'),(157,117,4,0.02,NULL,NULL,'Disponible'),(158,118,4,0.04,NULL,NULL,'Disponible'),(159,119,4,0.01,NULL,NULL,'Disponible'),(160,120,4,0.02,NULL,NULL,'Disponible'),(161,121,4,0.04,NULL,NULL,'Disponible'),(162,122,4,0.03,NULL,NULL,'Disponible'),(163,98,5,0.36,NULL,NULL,'Disponible'),(164,99,5,0.12,NULL,NULL,'Disponible'),(165,100,5,0.08,NULL,NULL,'Disponible'),(166,101,5,0.04,NULL,NULL,'Disponible'),(167,102,5,0.04,NULL,NULL,'Disponible'),(168,103,5,0.28,NULL,NULL,'Disponible'),(169,104,5,0.2,NULL,NULL,'Disponible'),(170,105,5,0.12,NULL,NULL,'Disponible'),(171,106,5,0.06,NULL,NULL,'Disponible'),(172,107,5,0.04,NULL,NULL,'Disponible'),(173,108,5,0.12,NULL,NULL,'Disponible'),(174,109,5,0.04,NULL,NULL,'Disponible'),(175,110,5,0.04,NULL,NULL,'Disponible'),(176,111,5,0.04,NULL,NULL,'Disponible'),(177,112,5,0.12,NULL,NULL,'Disponible'),(178,113,5,0.04,NULL,NULL,'Disponible'),(179,114,5,0.02,NULL,NULL,'Disponible'),(180,115,5,0.04,NULL,NULL,'Disponible'),(181,116,5,0.04,NULL,NULL,'Disponible'),(182,117,5,0.02,NULL,NULL,'Disponible'),(183,118,5,0.04,NULL,NULL,'Disponible'),(184,119,5,0.01,NULL,NULL,'Disponible'),(185,120,5,0.02,NULL,NULL,'Disponible'),(186,121,5,0.04,NULL,NULL,'Disponible'),(187,122,5,0.03,NULL,NULL,'Disponible'),(188,123,6,16.875,NULL,NULL,'Disponible'),(189,124,6,5,NULL,NULL,'Disponible'),(190,125,6,3.75,NULL,NULL,'Disponible'),(191,126,6,2.5,NULL,NULL,'Disponible'),(192,127,6,2.5,NULL,NULL,'Disponible'),(193,128,6,1.25,NULL,NULL,'Disponible'),(194,129,6,2.5,NULL,NULL,'Disponible'),(195,130,6,6.25,NULL,NULL,'Disponible'),(196,131,6,5,NULL,NULL,'Disponible'),(197,132,6,2.5,NULL,NULL,'Disponible'),(198,133,6,2.5,NULL,NULL,'Disponible'),(199,134,6,3.75,NULL,NULL,'Disponible'),(200,135,6,7.5,NULL,NULL,'Disponible'),(201,136,6,5,NULL,NULL,'Disponible'),(202,137,6,3.75,NULL,NULL,'Disponible'),(203,138,6,2.5,NULL,NULL,'Disponible'),(204,139,6,2.5,NULL,NULL,'Disponible'),(205,140,6,9.375,NULL,NULL,'Disponible'),(206,141,6,3.75,NULL,NULL,'Disponible'),(207,142,6,2.5,NULL,NULL,'Disponible'),(208,143,6,2.5,NULL,NULL,'Disponible'),(209,144,6,3.75,NULL,NULL,'Disponible'),(210,145,6,3.75,NULL,NULL,'Disponible'),(211,146,6,3.75,NULL,NULL,'Disponible'),(212,147,6,2.5,NULL,NULL,'Disponible'),(213,148,6,1.25,NULL,NULL,'Disponible'),(214,149,6,2.5,NULL,NULL,'Disponible'),(215,150,6,1.25,NULL,NULL,'Disponible'),(216,151,6,1.25,NULL,NULL,'Disponible'),(217,152,6,0.625,NULL,NULL,'Disponible'),(218,153,6,0.375,NULL,NULL,'Disponible'),(219,154,6,0.625,NULL,NULL,'Disponible'),(220,155,6,1.25,NULL,NULL,'Disponible'),(221,156,6,0.625,NULL,NULL,'Disponible'),(222,157,6,1.25,NULL,NULL,'Disponible'),(223,158,6,0.25,NULL,NULL,'Disponible'),(224,159,6,1.25,NULL,NULL,'Disponible'),(225,160,6,0.625,NULL,NULL,'Disponible'),(226,161,6,0.625,NULL,NULL,'Disponible'),(227,162,6,2.5,NULL,NULL,'Disponible'),(228,163,6,1.25,NULL,NULL,'Disponible');
/*!40000 ALTER TABLE `canal_corte` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carrito`
--

DROP TABLE IF EXISTS `carrito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carrito` (
  `idCarrito` int NOT NULL AUTO_INCREMENT,
  `idUsuario` int DEFAULT NULL,
  `fechaCreacion` datetime DEFAULT NULL,
  PRIMARY KEY (`idCarrito`),
  UNIQUE KEY `idUsuario` (`idUsuario`),
  CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carrito`
--

LOCK TABLES `carrito` WRITE;
/*!40000 ALTER TABLE `carrito` DISABLE KEYS */;
INSERT INTO `carrito` VALUES (1,3,'2026-04-13 18:51:04');
/*!40000 ALTER TABLE `carrito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categoria`
--

DROP TABLE IF EXISTS `categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria` (
  `idCategoria` int NOT NULL AUTO_INCREMENT,
  `nombreCategoria` varchar(25) NOT NULL,
  PRIMARY KEY (`idCategoria`),
  UNIQUE KEY `nombreCategoria` (`nombreCategoria`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria`
--

LOCK TABLES `categoria` WRITE;
/*!40000 ALTER TABLE `categoria` DISABLE KEYS */;
INSERT INTO `categoria` VALUES (4,'BORREGO'),(2,'CERDO'),(5,'OTRO'),(3,'POLLO'),(1,'RES');
/*!40000 ALTER TABLE `categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conversor`
--

DROP TABLE IF EXISTS `conversor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conversor` (
  `idConversor` int NOT NULL AUTO_INCREMENT,
  `nombreConversor` varchar(25) NOT NULL,
  PRIMARY KEY (`idConversor`),
  UNIQUE KEY `nombreConversor` (`nombreConversor`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conversor`
--

LOCK TABLES `conversor` WRITE;
/*!40000 ALTER TABLE `conversor` DISABLE KEYS */;
INSERT INTO `conversor` VALUES (1,'Kilogramos'),(3,'Litros'),(2,'Piezas');
/*!40000 ALTER TABLE `conversor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `corte`
--

DROP TABLE IF EXISTS `corte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corte` (
  `idCorte` int NOT NULL AUTO_INCREMENT,
  `idCategoria` int NOT NULL,
  `idFoto` varchar(255) DEFAULT NULL,
  `nombreCorte` varchar(50) NOT NULL,
  `Porcentaje` float DEFAULT NULL,
  `precioPorKilo` float DEFAULT NULL,
  PRIMARY KEY (`idCorte`),
  KEY `idCategoria` (`idCategoria`),
  CONSTRAINT `corte_ibfk_1` FOREIGN KEY (`idCategoria`) REFERENCES `categoria` (`idCategoria`)
) ENGINE=InnoDB AUTO_INCREMENT=164 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `corte`
--

LOCK TABLES `corte` WRITE;
/*!40000 ALTER TABLE `corte` DISABLE KEYS */;
INSERT INTO `corte` VALUES (1,1,'C1','Diezmillo',0.065,250),(2,1,'C2','Aguja norteña',0.03,210),(3,1,'C3','Espaldilla',0.04,220),(4,1,'C4','Paleta',0.03,190),(5,1,'C5','Flat iron',0.015,320),(6,1,'C6','Filete de aguja',0.01,230),(7,1,'C7','Cuello',0.02,185),(8,1,'C8','Molida de chuck',0.05,180),(9,1,'C19','Recortes grasos',0.035,150),(10,1,'C10','Ribeye',0.035,500),(11,1,'C11','Cowboy steak',0.015,600),(12,1,'C12','Tomahawk',0.015,550),(13,1,'C13','Costilla cargada',0.025,650),(14,1,'C14','Costilla para BBQ',0.008,500),(15,1,'C15','Recortes rib',0.007,350),(16,1,'C16','T-bone',0.03,250),(17,1,'C17','Porterhouse',0.02,650),(18,1,'C18','New York strip',0.025,750),(19,1,'C19','Filete',0.02,500),(20,1,'C20','Chateaubriand',0.01,900),(21,1,'C21','Sirloin',0.025,245),(22,1,'C22','Top sirloin',0.015,310),(23,1,'C23','Tri-tip',0.007,350),(24,1,'C24','Bola',0.065,220),(25,1,'C25','Contra',0.05,210),(26,1,'C26','Cuete',0.02,220),(27,1,'C27','Tapa',0.03,235),(28,1,'C28','Culotte',0.015,350),(29,1,'C29','Milanesa',0.02,230),(30,1,'C30','Carne para deshebrar',0.015,220),(32,1,'C32','Arrachera',0.03,400),(33,1,'C33','Entraña',0.02,450),(34,1,'C34','Short ribs',0.02,500),(35,1,'C35','Falda deshebrada',0.01,200),(36,1,'C36','Recortes',0.025,80),(37,1,'C37','Vacío',0.035,300),(38,1,'C38','Bavette',0.01,450),(40,1,'C40','Brisket plano',0.02,245),(41,1,'C41','Brisket punta',0.01,250),(42,1,'C42','Pecho para cocido',0.005,220),(43,1,'C43','Chambarete delantero',0.015,160),(44,1,'C44','Chambarete trasero',0.01,160),(45,1,'C45','Osobuco',0.005,165),(46,2,'C46','Pierna de cerdo',0.09,120),(47,2,'C47','Pulpa de pierna',0.04,75),(48,2,'C48','Jamón fresco',0.03,160),(49,2,'C49','Jamón para curar',0.03,60),(50,2,'C50','Centro de jamón',0.01,145),(51,2,'C51','Punta de jamón',0.01,170),(52,2,'C52','Cuete de jamón',0.01,220),(53,2,'C53','Recortes de pierna',0.01,100),(54,2,'C54','Lomo entero',0.065,125),(55,2,'C55','Chuleta de lomo',0.045,155),(56,2,'C56','Chuleta ahumada',0.02,130),(57,2,'C57','Caña de lomo',0.01,145),(58,2,'C58','Medallón de lomo',0.01,140),(59,2,'C59','Lomo limpio',0.01,140),(60,2,'C60','Recortes de lomo',0.01,60),(61,2,'C61','Panceta',0.045,190),(62,2,'C62','Tocino',0.04,300),(63,2,'C63','Tocino ahumado',0.03,350),(64,2,'C64','Panceta en tiras',0.01,190),(65,2,'C65','Recortes de panceta',0.01,170),(66,2,'C66','Costilla de cerdo',0.04,170),(67,2,'C67','Costilla cargada',0.02,120),(68,2,'C68','Costilla baby back',0.02,190),(69,2,'C69','Costilla para BBQ',0.01,160),(70,2,'C70','Punta de costilla',0.01,90),(71,2,'C71','Recortes de costilla',0.005,110),(72,2,'C72','Paleta completa',0.07,40),(73,2,'C73','Pulpa de paleta',0.03,70),(74,2,'C74','Espaldilla de cerdo',0.03,110),(75,2,'C75','Bistec de paleta',0.02,110),(76,2,'C76','Recortes de paleta',0.01,60),(77,2,'C77','Cabeza de cerdo',0.01,40),(78,2,'C78','Cachete de cerdo',0.005,40),(79,2,'C79','Lengua de cerdo',0.002,65),(80,2,'C80','Oreja',0.004,75),(81,2,'C81','Morro',0.004,65),(82,2,'C82','Papada',0.02,75),(83,2,'C83','Papada para tocino',0.01,80),(84,2,'C84','Cuello',0.01,105),(85,2,'C85','Secreto ibérico',0.005,900),(86,2,'C86','Pluma',0.005,650),(87,2,'C87','Patas delanteras',0.01,45),(88,2,'C88','Patas traseras',0.01,45),(89,2,'C89','Manitas de cerdo',0.01,45),(90,2,'C90','Rabo',0.005,35),(91,2,'C91','Grasa dorsal',0.02,40),(92,2,'C92','Grasa abdominal',0.01,40),(93,2,'C93','Manteca',0.01,40),(95,2,'C95','Carne molida de cerdo',0.02,160),(96,2,'C96','Chicharrón',0.01,300),(97,2,'C97','Piel de cerdo',0.01,40),(98,3,'C98','Pechuga completa',0.18,117),(99,3,'C99','Pechuga deshuesada',0.06,136),(100,3,'C100','Filete de pechuga',0.04,120),(101,3,'C101','Pechuga con hueso',0.02,80),(102,3,'C102','Recortes de pechuga',0.02,67),(103,3,'C103','Muslo',0.14,55),(104,3,'C104','Pierna',0.1,50),(105,3,'C105','Pierna y muslo',0.06,54),(106,3,'C106','Muslo deshuesado',0.03,86),(107,3,'C107','Recortes de pierna',0.02,40),(108,3,'C108','Alas completas',0.06,31),(109,3,'C109','Alita',0.02,22),(110,3,'C110','Medio ala',0.02,21),(111,3,'C111','Punta de ala',0.02,37),(112,3,'C112','Carcasa',0.06,21),(113,3,'C113','Cuello',0.02,29),(114,3,'C114','Cabeza',0.01,18),(115,3,'C115','Patas de pollo',0.02,34),(116,3,'C116','Hígado',0.02,43),(117,3,'C117','Corazón',0.01,60),(118,3,'C118','Molleja',0.02,30),(119,3,'C119','Pulmones',0.005,10),(120,3,'C120','Grasa abdominal',0.01,10),(121,3,'C121','Piel de pollo',0.02,12),(122,3,'C122','Recortes generales',0.015,22),(123,4,'C123','Pierna de cordero',0.135,178),(124,4,'C124','Pierna deshuesada',0.04,240),(125,4,'C125','Centro de pierna',0.03,250),(126,4,'C126','Punta de pierna',0.02,160),(127,4,'C127','Cuete de pierna',0.02,180),(128,4,'C128','Bistec de pierna',0.01,230),(129,4,'C129','Recortes de pierna',0.02,160),(130,4,'C130','Lomo de cordero',0.05,340),(131,4,'C131','Chuleta de lomo',0.04,410),(132,4,'C132','Medallón de lomo',0.02,430),(133,4,'C133','Lomo limpio',0.02,460),(134,4,'C134','Recortes de lomo',0.03,170),(135,4,'C135','Costillar de cordero',0.06,330),(136,4,'C136','Rack de cordero',0.04,510),(137,4,'C137','Chuleta de costilla',0.03,400),(138,4,'C138','Punta de costilla',0.02,240),(139,4,'C139','Recortes de costilla',0.02,150),(140,4,'C140','Paleta de cordero',0.075,200),(141,4,'C141','Paleta deshuesada',0.03,230),(142,4,'C142','Pulpa de paleta',0.02,200),(143,4,'C143','Bistec de paleta',0.02,190),(144,4,'C144','Recortes de paleta',0.03,160),(145,4,'C145','Pecho de cordero',0.03,150),(146,4,'C146','Falda de cordero',0.03,170),(147,4,'C147','Costilla falda',0.02,190),(148,4,'C148','Recortes de falda',0.01,140),(149,4,'C149','Cuello de cordero',0.02,180),(150,4,'C150','Rodajas de cuello',0.01,200),(151,4,'C151','Cabeza de cordero',0.01,110),(152,4,'C152','Lengua de cordero',0.005,220),(153,4,'C153','Sesos',0.003,120),(154,4,'C154','Corazón',0.005,140),(155,4,'C155','Hígado',0.01,120),(156,4,'C156','Riñones',0.005,130),(157,4,'C157','Patas de cordero',0.01,90),(158,4,'C158','Rabo',0.002,50),(159,4,'C159','Grasa dorsal',0.01,100),(160,4,'C160','Grasa interna',0.005,90),(161,4,'C161','Sebo',0.005,50),(162,4,'C162','Huesos para caldo',0.02,60),(163,4,'C163','Carne molida de cordero',0.01,260);
/*!40000 ALTER TABLE `corte` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `corte_unitario`
--

DROP TABLE IF EXISTS `corte_unitario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corte_unitario` (
  `idCorteUnitario` int NOT NULL AUTO_INCREMENT,
  `idCorte` int NOT NULL,
  `idLote` int DEFAULT NULL,
  `idCarrito` int DEFAULT NULL,
  `idPedido` int DEFAULT NULL,
  `peso` float NOT NULL,
  `costo` float NOT NULL,
  `estatus` varchar(20) NOT NULL,
  PRIMARY KEY (`idCorteUnitario`),
  KEY `idCorte` (`idCorte`),
  KEY `idLote` (`idLote`),
  KEY `idCarrito` (`idCarrito`),
  KEY `idPedido` (`idPedido`),
  CONSTRAINT `corte_unitario_ibfk_1` FOREIGN KEY (`idCorte`) REFERENCES `corte` (`idCorte`),
  CONSTRAINT `corte_unitario_ibfk_2` FOREIGN KEY (`idLote`) REFERENCES `lote` (`idLote`),
  CONSTRAINT `corte_unitario_ibfk_3` FOREIGN KEY (`idCarrito`) REFERENCES `carrito` (`idCarrito`),
  CONSTRAINT `corte_unitario_ibfk_4` FOREIGN KEY (`idPedido`) REFERENCES `pedido` (`idPedido`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `corte_unitario`
--

LOCK TABLES `corte_unitario` WRITE;
/*!40000 ALTER TABLE `corte_unitario` DISABLE KEYS */;
INSERT INTO `corte_unitario` VALUES (1,32,6,NULL,1,2.87,1148,'Vendido'),(2,46,7,NULL,1,11.5,1380,'Vendido');
/*!40000 ALTER TABLE `corte_unitario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detallesticket`
--

DROP TABLE IF EXISTS `detallesticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detallesticket` (
  `idDetalle` int NOT NULL AUTO_INCREMENT,
  `idTicket` int NOT NULL,
  `idProducto` int NOT NULL,
  `cantidad` int NOT NULL,
  `subtotal` float NOT NULL,
  PRIMARY KEY (`idDetalle`),
  KEY `idTicket` (`idTicket`),
  KEY `idProducto` (`idProducto`),
  CONSTRAINT `detallesticket_ibfk_1` FOREIGN KEY (`idTicket`) REFERENCES `ticket` (`idTicket`),
  CONSTRAINT `detallesticket_ibfk_2` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`idProducto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detallesticket`
--

LOCK TABLES `detallesticket` WRITE;
/*!40000 ALTER TABLE `detallesticket` DISABLE KEYS */;
/*!40000 ALTER TABLE `detallesticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lote`
--

DROP TABLE IF EXISTS `lote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lote` (
  `idLote` int NOT NULL AUTO_INCREMENT,
  `idCanalCorte` int DEFAULT NULL,
  `idMateriaProveida` int DEFAULT NULL,
  `idOrdenCompra` int DEFAULT NULL,
  `numeroLote` varchar(25) NOT NULL,
  `cantidadDeUnidad` int DEFAULT NULL,
  `cantidadPorUnidad` float DEFAULT NULL,
  `totalMateria` float DEFAULT NULL,
  `precioPorUnidad` float DEFAULT NULL,
  `totalCosto` float DEFAULT NULL,
  `fechaCaducidad` date DEFAULT NULL,
  `estatus` enum('Disponible','Caducado','Agotado','EnEspera','Cancelado') NOT NULL,
  `idUsuario` int DEFAULT NULL,
  PRIMARY KEY (`idLote`),
  KEY `idCanalCorte` (`idCanalCorte`),
  KEY `idMateriaProveida` (`idMateriaProveida`),
  KEY `idOrdenCompra` (`idOrdenCompra`),
  KEY `idUsuario` (`idUsuario`),
  CONSTRAINT `lote_ibfk_1` FOREIGN KEY (`idCanalCorte`) REFERENCES `canal_corte` (`idCanalCorte`),
  CONSTRAINT `lote_ibfk_2` FOREIGN KEY (`idMateriaProveida`) REFERENCES `materia_proveida` (`idMateriaProveida`),
  CONSTRAINT `lote_ibfk_3` FOREIGN KEY (`idOrdenCompra`) REFERENCES `orden_compra` (`idOrdenCompra`),
  CONSTRAINT `lote_ibfk_4` FOREIGN KEY (`idUsuario`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lote`
--

LOCK TABLES `lote` WRITE;
/*!40000 ALTER TABLE `lote` DISABLE KEYS */;
INSERT INTO `lote` VALUES (1,NULL,2,2,'Abril1302',10,20,195.5,10,2000,'2026-05-31','Disponible',NULL),(2,10,NULL,NULL,'LP-Abr1301',0,0,3.125,0,0,NULL,'Disponible',1),(3,NULL,9,3,'Abril1303',10,10,97,0.5,50,'2027-04-30','Disponible',NULL),(4,NULL,10,4,'Abril1304',10,10,87,0.6,60,'2027-04-30','Disponible',NULL),(5,118,NULL,NULL,'LP-Abr1302',0,0,14.7,0,0,NULL,'Disponible',1),(6,82,NULL,NULL,'LP-Abr1303',0,0,0.33,0,0,NULL,'Disponible',1),(7,1,NULL,NULL,'LP-Abr1304',0,0,0,0,0,NULL,'Agotado',1),(8,63,NULL,NULL,'LP-Abr1305',0,0,3,0,0,NULL,'Disponible',1),(9,108,NULL,NULL,'LP-Abr1306',0,0,1.95,0,0,NULL,'Disponible',1),(10,138,NULL,NULL,'LP-Abr1307',0,0,0.31,0,0,NULL,'Disponible',1),(11,125,NULL,NULL,'LP-Abr1308',0,0,2.2,0,0,NULL,'Disponible',1);
/*!40000 ALTER TABLE `lote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materia_prima`
--

DROP TABLE IF EXISTS `materia_prima`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materia_prima` (
  `idMateriaPrima` int NOT NULL AUTO_INCREMENT,
  `nombreMateriaPrima` varchar(25) NOT NULL,
  `idCategoria` int DEFAULT NULL,
  `tipo` varchar(25) DEFAULT NULL,
  `idProducto` int DEFAULT NULL,
  PRIMARY KEY (`idMateriaPrima`),
  UNIQUE KEY `nombreMateriaPrima` (`nombreMateriaPrima`),
  KEY `idCategoria` (`idCategoria`),
  KEY `idProducto` (`idProducto`),
  CONSTRAINT `materia_prima_ibfk_1` FOREIGN KEY (`idCategoria`) REFERENCES `categoria` (`idCategoria`),
  CONSTRAINT `materia_prima_ibfk_2` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`idProducto`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materia_prima`
--

LOCK TABLES `materia_prima` WRITE;
/*!40000 ALTER TABLE `materia_prima` DISABLE KEYS */;
INSERT INTO `materia_prima` VALUES (37,'Canal de res completa',1,'Canal',NULL),(38,'Media canal de res',1,'Canal',NULL),(39,'Cuarto delantero de res',1,'Canal',NULL),(40,'Cuarto trasero de res',1,'Canal',NULL),(41,'Canal de cerdo completa',2,'Canal',NULL),(42,'Media canal de cerdo',2,'Canal',NULL),(43,'Pierna de cerdo',2,'Materia',NULL),(44,'Lomo de cerdo entero',2,'Materia',NULL),(45,'Pollo entero fresco',3,'Canal',NULL),(46,'Pollo entero congelado',3,'Canal',NULL),(47,'Pechuga de pollo entera',3,'Materia',NULL),(48,'Muslo con pierna de pollo',3,'Materia',NULL),(49,'Canal de borrego completa',4,'Canal',NULL),(50,'Media canal de borrego',4,'Canal',NULL),(51,'Pierna de borrego',4,'Materia',NULL),(52,'Costillar de borrego',4,'Producto',NULL),(53,'Salsa para marinar',5,'Materia',NULL),(54,'Charola de plastico',5,'Materia',NULL),(55,'Empaque para carne',5,'Materia',NULL),(56,'Canal de cordero',4,'Canal',NULL),(57,'Canal de pollo',3,'Canal',NULL);
/*!40000 ALTER TABLE `materia_prima` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materia_proveida`
--

DROP TABLE IF EXISTS `materia_proveida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materia_proveida` (
  `idMateriaProveida` int NOT NULL AUTO_INCREMENT,
  `nombreMateriaProveida` varchar(25) NOT NULL,
  `idProveedor` int NOT NULL,
  `idMateriaPrima` int NOT NULL,
  `idUnidadMedida` int NOT NULL,
  PRIMARY KEY (`idMateriaProveida`),
  UNIQUE KEY `nombreMateriaProveida` (`nombreMateriaProveida`),
  KEY `idProveedor` (`idProveedor`),
  KEY `idMateriaPrima` (`idMateriaPrima`),
  KEY `idUnidadMedida` (`idUnidadMedida`),
  CONSTRAINT `materia_proveida_ibfk_1` FOREIGN KEY (`idProveedor`) REFERENCES `proveedor` (`id`),
  CONSTRAINT `materia_proveida_ibfk_2` FOREIGN KEY (`idMateriaPrima`) REFERENCES `materia_prima` (`idMateriaPrima`),
  CONSTRAINT `materia_proveida_ibfk_3` FOREIGN KEY (`idUnidadMedida`) REFERENCES `unidad_medida` (`idUnidadMedida`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materia_proveida`
--

LOCK TABLES `materia_proveida` WRITE;
/*!40000 ALTER TABLE `materia_proveida` DISABLE KEYS */;
INSERT INTO `materia_proveida` VALUES (1,'Canal de res Bajío',10,37,1),(2,'Salsa para marinar FIC Le',9,53,10),(3,'Pollo entero Bajío',5,45,1),(4,'Canal de Cerdo Bajío',2,41,1),(8,'Res canal Empacadora',2,37,1),(9,'Charola Polimeros',11,54,9),(10,'Empaque polimeros',11,55,9),(11,'Canal de cordero Empacado',2,56,1);
/*!40000 ALTER TABLE `materia_proveida` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orden_compra`
--

DROP TABLE IF EXISTS `orden_compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orden_compra` (
  `idOrdenCompra` int NOT NULL AUTO_INCREMENT,
  `idProveedor` int NOT NULL,
  `numeroLote` varchar(20) DEFAULT NULL,
  `estatus` enum('EnCurso','Recibida','Cancelada') NOT NULL,
  `fechaDeOrden` date NOT NULL,
  `notas` varchar(500) DEFAULT NULL,
  `totalOrden` float NOT NULL,
  `PagoProveedor` varchar(20) NOT NULL,
  `metodoPago` varchar(20) DEFAULT NULL,
  `fechaPago` datetime DEFAULT NULL,
  `idUsuario` int DEFAULT NULL,
  `idUsuarioPago` int DEFAULT NULL,
  PRIMARY KEY (`idOrdenCompra`),
  UNIQUE KEY `numeroLote` (`numeroLote`),
  KEY `idProveedor` (`idProveedor`),
  KEY `idUsuario` (`idUsuario`),
  KEY `idUsuarioPago` (`idUsuarioPago`),
  CONSTRAINT `orden_compra_ibfk_1` FOREIGN KEY (`idProveedor`) REFERENCES `proveedor` (`id`),
  CONSTRAINT `orden_compra_ibfk_2` FOREIGN KEY (`idUsuario`) REFERENCES `user` (`id`),
  CONSTRAINT `orden_compra_ibfk_3` FOREIGN KEY (`idUsuarioPago`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orden_compra`
--

LOCK TABLES `orden_compra` WRITE;
/*!40000 ALTER TABLE `orden_compra` DISABLE KEYS */;
INSERT INTO `orden_compra` VALUES (1,2,'Abril1301','Recibida','2026-04-13',NULL,2400,'Pagado','Transferencia','2026-04-13 17:47:03',1,1),(2,9,'Abril1302','Recibida','2026-04-13',NULL,2000,'Pagado','Transferencia','2026-04-13 17:47:05',1,1),(3,11,'Abril1303','Recibida','2026-04-13',NULL,50,'Pagado','Transferencia','2026-04-13 17:47:07',1,1),(4,11,'Abril1304','Recibida','2026-04-13',NULL,60,'Pagado','Transferencia','2026-04-13 17:47:10',1,1),(5,2,'Abril1305','Recibida','2026-04-13',NULL,7500,'Pagado','Transferencia','2026-04-13 17:47:13',1,1),(6,5,'Abril1306','Recibida','2026-04-13',NULL,100,'Pagado','Transferencia','2026-04-13 17:49:02',1,1),(7,2,'Abril1307','Recibida','2026-04-13',NULL,3750,'Pendiente',NULL,NULL,1,NULL);
/*!40000 ALTER TABLE `orden_compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `idPedido` int NOT NULL AUTO_INCREMENT,
  `idUsuario` int DEFAULT NULL,
  `Total` float DEFAULT NULL,
  `Tipo` varchar(50) DEFAULT NULL,
  `Estatus` varchar(50) DEFAULT NULL,
  `Entrega` varchar(50) DEFAULT NULL,
  `Direccion` varchar(500) DEFAULT NULL,
  `Notas` varchar(500) DEFAULT NULL,
  `fechaCreacion` datetime NOT NULL,
  PRIMARY KEY (`idPedido`),
  KEY `idUsuario` (`idUsuario`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (1,3,2888,'Efectivo','Finalizado','Mostrador','En sucursal','Llego alredeor de las 3pm','2026-04-13 19:04:59');
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permisos_modulos`
--

DROP TABLE IF EXISTS `permisos_modulos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permisos_modulos` (
  `id_permiso` int NOT NULL AUTO_INCREMENT,
  `role_id` int NOT NULL,
  `modulo` varchar(50) NOT NULL,
  `l_lectura` tinyint(1) DEFAULT NULL,
  `a_alta` tinyint(1) DEFAULT NULL,
  `b_baja` tinyint(1) DEFAULT NULL,
  `m_modificacion` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id_permiso`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `permisos_modulos_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permisos_modulos`
--

LOCK TABLES `permisos_modulos` WRITE;
/*!40000 ALTER TABLE `permisos_modulos` DISABLE KEYS */;
/*!40000 ALTER TABLE `permisos_modulos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona`
--

DROP TABLE IF EXISTS `persona`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `persona` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido_paterno` varchar(100) NOT NULL,
  `apellido_materno` varchar(100) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `persona_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona`
--

LOCK TABLES `persona` WRITE;
/*!40000 ALTER TABLE `persona` DISABLE KEYS */;
INSERT INTO `persona` VALUES (1,'admin','admin','admin','4773845271','León, Gto',1),(2,'Haziel','Gutierrez','','4771135346','Pio XI #115, San Jerónimo II, León Gto',2),(3,'Emmanuel','Ortiz','Reyes','4773845271','Jose Antonio Torres #203 Col. Villa Insurgentes',3);
/*!40000 ALTER TABLE `persona` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `idProducto` int NOT NULL AUTO_INCREMENT,
  `idFoto` varchar(255) DEFAULT NULL,
  `NombreProducto` varchar(100) NOT NULL,
  `DescripcionProducto` varchar(500) DEFAULT NULL,
  `PrecioVentaProducto` float NOT NULL,
  `StockProducto` int NOT NULL,
  `idCategoria` int DEFAULT NULL,
  PRIMARY KEY (`idProducto`),
  UNIQUE KEY `NombreProducto` (`NombreProducto`),
  KEY `idCategoria` (`idCategoria`),
  CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`idCategoria`) REFERENCES `categoria` (`idCategoria`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,'2','Arrachera marinada','1 Kg de arrachera de res marinada',180,9,1),(2,'3','Carne molida','1 Kg de carne molida mixta',80,3,1),(3,'4','Chuleta marinada','1 Kg de chuleta marinada de cerdo',90,0,2);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto_unitario`
--

DROP TABLE IF EXISTS `producto_unitario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto_unitario` (
  `idProductoUnitario` int NOT NULL AUTO_INCREMENT,
  `idProducto` int NOT NULL,
  `idPedido` int DEFAULT NULL,
  `NumeroLote` varchar(100) NOT NULL,
  `FechaCaducidad` date DEFAULT NULL,
  `estatus` varchar(100) NOT NULL,
  `idCarrito` int DEFAULT NULL,
  `idOrdenCompra` int DEFAULT NULL,
  PRIMARY KEY (`idProductoUnitario`),
  KEY `idProducto` (`idProducto`),
  KEY `idPedido` (`idPedido`),
  KEY `idCarrito` (`idCarrito`),
  KEY `producto_unitario_ibfk_4` (`idOrdenCompra`),
  CONSTRAINT `producto_unitario_ibfk_1` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`idProducto`),
  CONSTRAINT `producto_unitario_ibfk_2` FOREIGN KEY (`idPedido`) REFERENCES `pedido` (`idPedido`),
  CONSTRAINT `producto_unitario_ibfk_3` FOREIGN KEY (`idCarrito`) REFERENCES `carrito` (`idCarrito`),
  CONSTRAINT `producto_unitario_ibfk_4` FOREIGN KEY (`idOrdenCompra`) REFERENCES `orden_compra` (`idOrdenCompra`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto_unitario`
--

LOCK TABLES `producto_unitario` WRITE;
/*!40000 ALTER TABLE `producto_unitario` DISABLE KEYS */;
INSERT INTO `producto_unitario` VALUES (1,1,NULL,'PP-Abr1301',NULL,'Disponible',NULL,NULL),(2,1,NULL,'PP-Abr1301',NULL,'Disponible',NULL,NULL),(3,1,NULL,'PP-Abr1301',NULL,'Disponible',NULL,NULL),(4,1,NULL,'PP-Abr1301',NULL,'Disponible',NULL,NULL),(5,2,NULL,'PP-Abr1302',NULL,'Disponible',NULL,NULL),(6,2,NULL,'PP-Abr1302',NULL,'Disponible',NULL,NULL),(7,2,NULL,'PP-Abr1302',NULL,'Disponible',NULL,NULL),(8,3,1,'PP-Abr1303',NULL,'Vendido',NULL,NULL),(9,3,1,'PP-Abr1303',NULL,'Vendido',NULL,NULL),(10,3,1,'PP-Abr1303',NULL,'Vendido',NULL,NULL),(11,3,1,'PP-Abr1303',NULL,'Vendido',NULL,NULL),(12,1,NULL,'PP-Abr1304',NULL,'Disponible',NULL,NULL),(13,1,NULL,'PP-Abr1304',NULL,'Disponible',NULL,NULL),(14,1,NULL,'PP-Abr1304',NULL,'Disponible',NULL,NULL),(15,1,NULL,'PP-Abr1304',NULL,'Disponible',NULL,NULL),(16,1,NULL,'PP-Abr1304',NULL,'Disponible',NULL,NULL);
/*!40000 ALTER TABLE `producto_unitario` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `actualizar_stock_after_insert` AFTER INSERT ON `producto_unitario` FOR EACH ROW BEGIN
    UPDATE producto
    SET StockProducto = (
        SELECT COUNT(*)
        FROM producto_unitario
        WHERE idProducto = NEW.idProducto
          AND estatus = 'Disponible'
    )
    WHERE idProducto = NEW.idProducto;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `actualizar_stock_after_update` AFTER UPDATE ON `producto_unitario` FOR EACH ROW BEGIN
    -- Recalcula el producto origen (por si cambió de idProducto)
    UPDATE producto
    SET StockProducto = (
        SELECT COUNT(*)
        FROM producto_unitario
        WHERE idProducto = OLD.idProducto
          AND estatus = 'Disponible'
    )
    WHERE idProducto = OLD.idProducto;

    -- Si la unidad fue reasignada a otro producto, actualiza ese también
    IF NEW.idProducto <> OLD.idProducto THEN
        UPDATE producto
        SET StockProducto = (
            SELECT COUNT(*)
            FROM producto_unitario
            WHERE idProducto = NEW.idProducto
              AND estatus = 'Disponible'
        )
        WHERE idProducto = NEW.idProducto;
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `proveedor`
--

DROP TABLE IF EXISTS `proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `rfc` varchar(13) NOT NULL,
  `estatus` enum('activo','inactivo') NOT NULL,
  `contacto` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `correo` varchar(120) DEFAULT NULL,
  `direccion` varchar(250) DEFAULT NULL,
  `condicion_pago` enum('contado','credito_8','credito_15','credito_30') NOT NULL,
  `dias_entrega` varchar(100) DEFAULT NULL,
  `notas` text,
  `fecha_registro` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rfc` (`rfc`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedor`
--

LOCK TABLES `proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor` DISABLE KEYS */;
INSERT INTO `proveedor` VALUES (2,'Empacadora de Carnes del Bajío','ECB010824KJ2','activo','Lic. Andrea Gómez','4772345678','ventas@ecbajio.mx','Parque Industrial León, Gto.','credito_30','Martes y Jueves','Distribución de carne de res en canal y cortes','2026-04-10 11:47:04'),(3,'Rastro Porcícola Guanajuato','RPG950612LM3','activo','Carlos Hernández','4621456789','ventas@rastroporcino.mx','Irapuato, Guanajuato','credito_15','Lunes a Viernes','Especialistas en canal de cerdo','2026-04-10 11:47:04'),(4,'Procesadora Porcina del Centro','PPC030921TR4','activo','María López','4773456789','contacto@ppcentro.mx','Silao, Guanajuato','credito_8','Martes, Jueves, Sábado','Venta de carne de cerdo fresca y congelada','2026-04-10 11:47:04'),(5,'Avícola Bajío S.A. de C.V.','ABA070515DF5','activo','Raúl Sánchez','4774567890','ventas@avicolabajio.mx','León, Guanajuato','contado','Diario','Suministro de pollo fresco entero y en piezas','2026-04-10 11:47:04'),(6,'Distribuidora Avícola Los Altos','DAL110223GH6','activo','Luis Ramírez','4741122334','pedidos@avicolalosaltos.mx','Lagos de Moreno, Jalisco','credito_8','Lunes a Sábado','Proveedor regional de pollo','2026-04-10 11:47:04'),(7,'Rastro Ovino del Bajío','ROB980731JK7','activo','Pedro Castillo','4775678901','contacto@ovinosbajio.mx','San Francisco del Rincón, Gto.','credito_15','Miércoles y Viernes','Venta de canal de borrego','2026-04-10 11:47:04'),(8,'Ganadera Ovina Guanajuato','GOG050912PL8','activo','Fernando Torres','4776789012','ventas@ganaderaovina.mx','Dolores Hidalgo, Gto.','credito_30','Martes y Jueves','Proveedor de borrego en pie y canal','2026-04-10 11:47:04'),(9,'Frigorífico Industrial del Centro','FIC020101MN9','activo','Alejandro Ruiz','4777890123','contacto@ficentro.mx','León, Guanajuato','credito_30','Lunes a Viernes','Manejan res, cerdo y pollo','2026-04-10 11:47:04'),(10,'Distribuidora Cárnica Integral Bajío','DCI140404QR1','activo','Sofía Navarro','4778901234','ventas@dcibajio.mx','Silao, Guanajuato','credito_15','Lunes, Miércoles, Viernes','Proveedor multi-especie','2026-04-10 11:47:04'),(11,'Polimeros y derivados S.A. de C.V.','POLIMEROSASID','activo','Juan Perez','4776128593','polimerosventas@hotmail.com','Calle San Julian #512, Parque industrial IV, Celaya, Gto','contado','Lunes',NULL,'2026-04-13 17:30:19');
/*!40000 ALTER TABLE `proveedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receta`
--

DROP TABLE IF EXISTS `receta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receta` (
  `idReceta` int NOT NULL AUTO_INCREMENT,
  `nombreReceta` varchar(100) NOT NULL,
  `idProducto` int NOT NULL,
  `idFoto` varchar(255) DEFAULT NULL,
  `descripcion` varchar(500) DEFAULT NULL,
  `tipo` varchar(20) NOT NULL,
  PRIMARY KEY (`idReceta`),
  UNIQUE KEY `nombreReceta` (`nombreReceta`),
  KEY `idProducto` (`idProducto`),
  CONSTRAINT `receta_ibfk_1` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`idProducto`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta`
--

LOCK TABLES `receta` WRITE;
/*!40000 ALTER TABLE `receta` DISABLE KEYS */;
INSERT INTO `receta` VALUES (1,'Arrachera marinada',1,'2',NULL,'MateriaPrima'),(2,'Carne molida',2,'3','1kg de carne molida de res, va en charola','MateriaPrima'),(3,'Chuleta marinada',3,'4','1kg de chuleta marinada de chuleta de lomo de cerdo, va en empaque','MateriaPrima');
/*!40000 ALTER TABLE `receta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receta_materia_prima`
--

DROP TABLE IF EXISTS `receta_materia_prima`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receta_materia_prima` (
  `idRecetaMateriaPrima` int NOT NULL AUTO_INCREMENT,
  `idReceta` int NOT NULL,
  `idMateriaPrima` int DEFAULT NULL,
  `idCorte` int DEFAULT NULL,
  `cantidadUsada` float NOT NULL,
  PRIMARY KEY (`idRecetaMateriaPrima`),
  KEY `idReceta` (`idReceta`),
  KEY `idMateriaPrima` (`idMateriaPrima`),
  KEY `idCorte` (`idCorte`),
  CONSTRAINT `receta_materia_prima_ibfk_1` FOREIGN KEY (`idReceta`) REFERENCES `receta` (`idReceta`),
  CONSTRAINT `receta_materia_prima_ibfk_2` FOREIGN KEY (`idMateriaPrima`) REFERENCES `materia_prima` (`idMateriaPrima`),
  CONSTRAINT `receta_materia_prima_ibfk_3` FOREIGN KEY (`idCorte`) REFERENCES `corte` (`idCorte`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta_materia_prima`
--

LOCK TABLES `receta_materia_prima` WRITE;
/*!40000 ALTER TABLE `receta_materia_prima` DISABLE KEYS */;
INSERT INTO `receta_materia_prima` VALUES (1,1,53,NULL,0.5),(2,1,55,NULL,1),(3,1,NULL,32,1),(10,3,55,NULL,1),(11,3,NULL,55,1),(12,2,54,NULL,1),(13,2,NULL,24,0.5),(14,2,NULL,46,0.5);
/*!40000 ALTER TABLE `receta_materia_prima` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `retiro`
--

DROP TABLE IF EXISTS `retiro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `retiro` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `origen` varchar(20) NOT NULL,
  `monto` float NOT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  `usuario` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `retiro`
--

LOCK TABLES `retiro` WRITE;
/*!40000 ALTER TABLE `retiro` DISABLE KEYS */;
INSERT INTO `retiro` VALUES (1,'2026-04-13 17:44:40','Ingreso','Efectivo',7500,'Apertura de caja','LaRESpuestaAdmin@gmail.com'),(2,'2026-04-13 17:44:58','Ingreso','Transferencia',100000,'Capital inicial','LaRESpuestaAdmin@gmail.com');
/*!40000 ALTER TABLE `retiro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'admin','Administrator'),(2,'Gerente','Administrador general del sistema'),(3,'Cajero','Cobrador de mostrador'),(4,'Repartidor','Entregas a domicilio'),(5,'Cliente','Ventas en linea'),(6,'end-user','End user');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solicitud_produccion`
--

DROP TABLE IF EXISTS `solicitud_produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solicitud_produccion` (
  `idSolicitud` int NOT NULL AUTO_INCREMENT,
  `tipoReceta` varchar(20) NOT NULL,
  `idReceta` int DEFAULT NULL,
  `idCorte` int DEFAULT NULL,
  `cantidadProducir` int NOT NULL,
  `fechaSolicitud` datetime NOT NULL,
  `fechaCompletada` datetime DEFAULT NULL,
  `estatus` varchar(20) NOT NULL,
  `idUsuario` int DEFAULT NULL,
  `notas` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`idSolicitud`),
  KEY `idReceta` (`idReceta`),
  KEY `idCorte` (`idCorte`),
  KEY `idUsuario` (`idUsuario`),
  CONSTRAINT `solicitud_produccion_ibfk_1` FOREIGN KEY (`idReceta`) REFERENCES `receta` (`idReceta`),
  CONSTRAINT `solicitud_produccion_ibfk_2` FOREIGN KEY (`idCorte`) REFERENCES `corte` (`idCorte`),
  CONSTRAINT `solicitud_produccion_ibfk_3` FOREIGN KEY (`idUsuario`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitud_produccion`
--

LOCK TABLES `solicitud_produccion` WRITE;
/*!40000 ALTER TABLE `solicitud_produccion` DISABLE KEYS */;
INSERT INTO `solicitud_produccion` VALUES (1,'Corte',NULL,55,1,'2026-04-13 17:12:46','2026-04-13 17:13:16','Completada',1,'Se necesita extraer toda la chuleta posible'),(2,'Corte',NULL,24,1,'2026-04-13 17:55:43','2026-04-13 17:57:05','Completada',1,'Todo en fa'),(3,'Corte',NULL,46,1,'2026-04-13 17:56:11','2026-04-13 17:57:24','Completada',1,'Se ocupa para carne molida'),(4,'Corte',NULL,32,1,'2026-04-13 17:56:38','2026-04-13 17:57:14','Completada',1,'Para marinar'),(5,'Personalizada',1,NULL,4,'2026-04-13 17:58:45','2026-04-13 18:05:00','Completada',1,NULL),(6,'Personalizada',2,NULL,3,'2026-04-13 18:02:37','2026-04-13 18:05:10','Completada',1,NULL),(7,'Personalizada',3,NULL,4,'2026-04-13 18:02:53','2026-04-13 18:05:14','Completada',1,NULL),(8,'Corte',NULL,12,1,'2026-04-13 18:50:34','2026-04-13 18:50:51','Completada',1,NULL),(9,'Corte',NULL,14,1,'2026-04-13 19:08:45','2026-04-13 19:09:29','Completada',1,'Se necesita en 30 mins'),(10,'Corte',NULL,98,1,'2026-04-13 19:10:25','2026-04-13 19:11:22','Completada',1,NULL),(11,'Corte',NULL,32,1,'2026-04-13 19:14:30','2026-04-13 19:14:35','Completada',1,'La necesito ya'),(12,'Personalizada',1,NULL,5,'2026-04-13 19:14:57','2026-04-13 19:15:17','Completada',1,NULL);
/*!40000 ALTER TABLE `solicitud_produccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solicitud_produccion_detalle`
--

DROP TABLE IF EXISTS `solicitud_produccion_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solicitud_produccion_detalle` (
  `idDetalle` int NOT NULL AUTO_INCREMENT,
  `idSolicitud` int NOT NULL,
  `idMateriaPrima` int DEFAULT NULL,
  `idLote` int DEFAULT NULL,
  `idCanalCorte` int DEFAULT NULL,
  `idLoteProducido` int DEFAULT NULL,
  `cantidadConsumida` float NOT NULL,
  PRIMARY KEY (`idDetalle`),
  KEY `idSolicitud` (`idSolicitud`),
  KEY `idMateriaPrima` (`idMateriaPrima`),
  KEY `idLote` (`idLote`),
  KEY `idCanalCorte` (`idCanalCorte`),
  KEY `idLoteProducido` (`idLoteProducido`),
  CONSTRAINT `solicitud_produccion_detalle_ibfk_1` FOREIGN KEY (`idSolicitud`) REFERENCES `solicitud_produccion` (`idSolicitud`),
  CONSTRAINT `solicitud_produccion_detalle_ibfk_2` FOREIGN KEY (`idMateriaPrima`) REFERENCES `materia_prima` (`idMateriaPrima`),
  CONSTRAINT `solicitud_produccion_detalle_ibfk_3` FOREIGN KEY (`idLote`) REFERENCES `lote` (`idLote`),
  CONSTRAINT `solicitud_produccion_detalle_ibfk_4` FOREIGN KEY (`idCanalCorte`) REFERENCES `canal_corte` (`idCanalCorte`),
  CONSTRAINT `solicitud_produccion_detalle_ibfk_5` FOREIGN KEY (`idLoteProducido`) REFERENCES `lote` (`idLote`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitud_produccion_detalle`
--

LOCK TABLES `solicitud_produccion_detalle` WRITE;
/*!40000 ALTER TABLE `solicitud_produccion_detalle` DISABLE KEYS */;
INSERT INTO `solicitud_produccion_detalle` VALUES (1,1,NULL,NULL,10,2,7.125),(2,2,NULL,NULL,118,5,16.2),(3,3,NULL,NULL,1,7,13),(4,4,NULL,NULL,82,6,7.2),(5,5,53,1,NULL,NULL,2),(6,5,55,4,NULL,NULL,4),(7,5,NULL,6,NULL,NULL,4),(8,6,54,3,NULL,NULL,3),(9,6,NULL,5,NULL,NULL,1.5),(10,6,NULL,7,NULL,NULL,1.5),(11,7,55,4,NULL,NULL,4),(12,7,NULL,2,NULL,NULL,4),(13,8,NULL,NULL,63,8,3),(14,9,NULL,NULL,108,9,1.95),(15,10,NULL,NULL,138,10,0.31),(16,11,NULL,NULL,125,11,7.2),(17,12,53,1,NULL,NULL,2.5),(18,12,55,4,NULL,NULL,5),(19,12,NULL,11,NULL,NULL,5);
/*!40000 ALTER TABLE `solicitud_produccion_detalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket` (
  `idTicket` int NOT NULL AUTO_INCREMENT,
  `folioTicket` varchar(50) NOT NULL,
  `fechaCompra` datetime NOT NULL,
  `totalCompra` float NOT NULL,
  PRIMARY KEY (`idTicket`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
/*!40000 ALTER TABLE `ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unidad_medida`
--

DROP TABLE IF EXISTS `unidad_medida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unidad_medida` (
  `idUnidadMedida` int NOT NULL AUTO_INCREMENT,
  `nombreUnidadMedida` varchar(25) NOT NULL,
  `idConversor` int DEFAULT NULL,
  PRIMARY KEY (`idUnidadMedida`),
  UNIQUE KEY `nombreUnidadMedida` (`nombreUnidadMedida`),
  KEY `idConversor` (`idConversor`),
  CONSTRAINT `unidad_medida_ibfk_1` FOREIGN KEY (`idConversor`) REFERENCES `conversor` (`idConversor`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidad_medida`
--

LOCK TABLES `unidad_medida` WRITE;
/*!40000 ALTER TABLE `unidad_medida` DISABLE KEYS */;
INSERT INTO `unidad_medida` VALUES (1,'Canal entera',1),(2,'Media canal',1),(3,'Kilogramo',1),(4,'Tonelada',1),(5,'Paquete',1),(6,'Bolsa',1),(7,'Bulto',1),(8,'Pieza',2),(9,'Caja',2),(10,'Litro',3);
/*!40000 ALTER TABLE `unidad_medida` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `fs_uniquifier` varchar(255) NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `confirmed_at` datetime DEFAULT NULL,
  `intentos_fallidos` int NOT NULL,
  `bloqueado_hasta` datetime DEFAULT NULL,
  `ultima_sesion` datetime DEFAULT NULL,
  `ultima_ip` varchar(45) DEFAULT NULL,
  `session_token` varchar(255) DEFAULT NULL,
  `session_expiration` datetime DEFAULT NULL,
  `autenticacion_doble_factor` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `fs_uniquifier` (`fs_uniquifier`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','LaRESpuestaAdmin@gmail.com','$pbkdf2-sha512$25000$sTYGwPi/F8L4X2uNMcbYmw$XuCzSVLTcDxkyzMlBr2u1fpW5FsD.DtINLHe3mvqBMeBG9KenJyQQ3VKOHOR7UvGf9hf0HvCJTbq1LWIEYQJIA','c690016303274aa3a8a4008fe65b7a86',1,NULL,0,NULL,'2026-04-13 15:53:24','127.0.0.1','cc1a3ec3-b848-4705-b495-5f9eae043c07','2026-04-20 19:16:27',NULL),(2,'Haziel Gutierrez','hazielgtz@hotmail.com','$pbkdf2-sha512$25000$17r3/l9LKUUIgbC2llJq7Q$qNev7Prt.TnYBPmyBuVCpln3LgcfhzOAoOyJIgMo40Lx0qY1p/E3F6IQGJdIUb4ejiFMPIRQ//o.o/c58/vPiQ','4f0ce74b45b64733935db140a1b5492a',1,NULL,0,NULL,'2026-04-13 17:18:55','127.0.0.1','71dbe023-dac6-4c90-8dcf-62cab05f3514','2026-04-20 18:11:46',NULL),(3,'Emmanuel Ortiz Reyes','emmanuelortizreyes3@gmail.com','$pbkdf2-sha512$25000$sva.l1IqJQQgJARAyPm/9w$k.MQQHDITfyr7Hm2.ZHuBsvRNdWQMla56vz6JaxoSBlixgdh8QA1mfukjO2hvX6G7vPZI2475RCsE1.0oJwDxQ','f79fc78bdb45420c9adf8b9e55a517e9',1,NULL,0,NULL,'2026-04-13 18:11:46','127.0.0.1','2ad35d27-840f-47d6-895e-158b7578f387','2026-04-20 19:11:33',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_roles`
--

DROP TABLE IF EXISTS `users_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_roles` (
  `userId` int DEFAULT NULL,
  `roleId` int DEFAULT NULL,
  KEY `userId` (`userId`),
  KEY `roleId` (`roleId`),
  CONSTRAINT `users_roles_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `user` (`id`),
  CONSTRAINT `users_roles_ibfk_2` FOREIGN KEY (`roleId`) REFERENCES `role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_roles`
--

LOCK TABLES `users_roles` WRITE;
/*!40000 ALTER TABLE `users_roles` DISABLE KEYS */;
INSERT INTO `users_roles` VALUES (1,1),(2,5),(3,3);
/*!40000 ALTER TABLE `users_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vista_resumen_pedido`
--

DROP TABLE IF EXISTS `vista_resumen_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vista_resumen_pedido` (
  `idPedido` int NOT NULL,
  `idProducto` int NOT NULL,
  `NombreProducto` varchar(255) DEFAULT NULL,
  `PrecioVentaProducto` float DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `subtotal` float DEFAULT NULL,
  PRIMARY KEY (`idPedido`,`idProducto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vista_resumen_pedido`
--

LOCK TABLES `vista_resumen_pedido` WRITE;
/*!40000 ALTER TABLE `vista_resumen_pedido` DISABLE KEYS */;
/*!40000 ALTER TABLE `vista_resumen_pedido` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-13 19:16:28
