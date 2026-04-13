-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: LA_RESPUESTA
-- ------------------------------------------------------
-- Server version	8.0.45

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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `canal`
--

LOCK TABLES `canal` WRITE;
/*!40000 ALTER TABLE `canal` DISABLE KEYS */;
INSERT INTO `canal` VALUES (1,1,2,'Canal de res completa',250,'2026-04-12','2026-04-19','Disponible'),(2,2,3,'Canal de cerdo completa',90,'2026-04-12','2026-04-19','Disponible'),(3,1,4,'Canal de res completa',250,'2026-04-12','2026-04-19','Disponible');
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
) ENGINE=InnoDB AUTO_INCREMENT=143 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `canal_corte`
--

LOCK TABLES `canal_corte` WRITE;
/*!40000 ALTER TABLE `canal_corte` DISABLE KEYS */;
INSERT INTO `canal_corte` VALUES (1,1,1,16.25,NULL,NULL,'Disponible'),(2,2,1,7.5,7.234,0.266,'Consumido'),(3,3,1,10,NULL,NULL,'Disponible'),(4,4,1,7.5,NULL,NULL,'Disponible'),(5,5,1,3.75,NULL,NULL,'Disponible'),(6,6,1,2.5,2.25,0.25,'Consumido'),(7,7,1,5,NULL,NULL,'Disponible'),(8,8,1,12.5,NULL,NULL,'Disponible'),(9,9,1,8.75,NULL,NULL,'Disponible'),(10,10,1,8.75,NULL,NULL,'Disponible'),(11,11,1,3.75,NULL,NULL,'Disponible'),(12,12,1,3.75,NULL,NULL,'Disponible'),(13,13,1,6.25,NULL,NULL,'Disponible'),(14,14,1,2,NULL,NULL,'Disponible'),(15,15,1,1.75,NULL,NULL,'Disponible'),(16,16,1,7.5,NULL,NULL,'Disponible'),(17,17,1,5,NULL,NULL,'Disponible'),(18,18,1,6.25,NULL,NULL,'Disponible'),(19,19,1,5,NULL,NULL,'Disponible'),(20,20,1,2.5,NULL,NULL,'Disponible'),(21,21,1,6.25,NULL,NULL,'Disponible'),(22,22,1,3.75,NULL,NULL,'Disponible'),(23,23,1,1.75,NULL,NULL,'Disponible'),(24,24,1,16.25,NULL,NULL,'Disponible'),(25,25,1,12.5,NULL,NULL,'Disponible'),(26,26,1,5,NULL,NULL,'Disponible'),(27,27,1,7.5,NULL,NULL,'Disponible'),(28,28,1,3.75,NULL,NULL,'Disponible'),(29,29,1,5,NULL,NULL,'Disponible'),(30,30,1,3.75,NULL,NULL,'Disponible'),(31,31,1,2.5,NULL,NULL,'Disponible'),(32,32,1,7.5,NULL,NULL,'Disponible'),(33,33,1,5,NULL,NULL,'Disponible'),(34,34,1,5,NULL,NULL,'Disponible'),(35,35,1,2.5,NULL,NULL,'Disponible'),(36,36,1,5.75,NULL,NULL,'Disponible'),(37,37,1,8.75,NULL,NULL,'Disponible'),(38,38,1,2.5,NULL,NULL,'Disponible'),(39,39,1,2.5,NULL,NULL,'Disponible'),(40,40,1,5,NULL,NULL,'Disponible'),(41,41,1,2.5,NULL,NULL,'Disponible'),(42,42,1,1.25,NULL,NULL,'Disponible'),(43,43,1,3.75,NULL,NULL,'Disponible'),(44,44,1,2.5,NULL,NULL,'Disponible'),(45,45,1,1.25,NULL,NULL,'Disponible'),(46,46,2,8.1,NULL,NULL,'Disponible'),(47,47,2,3.6,NULL,NULL,'Disponible'),(48,48,2,2.7,NULL,NULL,'Disponible'),(49,49,2,2.7,NULL,NULL,'Disponible'),(50,50,2,0.9,NULL,NULL,'Disponible'),(51,51,2,0.9,NULL,NULL,'Disponible'),(52,52,2,0.9,NULL,NULL,'Disponible'),(53,53,2,0.9,NULL,NULL,'Disponible'),(54,54,2,5.85,NULL,NULL,'Disponible'),(55,55,2,4.05,NULL,NULL,'Disponible'),(56,56,2,1.8,NULL,NULL,'Disponible'),(57,57,2,0.9,NULL,NULL,'Disponible'),(58,58,2,0.9,NULL,NULL,'Disponible'),(59,59,2,0.9,NULL,NULL,'Disponible'),(60,60,2,0.9,NULL,NULL,'Disponible'),(61,61,2,4.05,NULL,NULL,'Disponible'),(62,62,2,3.6,NULL,NULL,'Disponible'),(63,63,2,2.7,NULL,NULL,'Disponible'),(64,64,2,0.9,NULL,NULL,'Disponible'),(65,65,2,0.9,NULL,NULL,'Disponible'),(66,66,2,3.6,NULL,NULL,'Disponible'),(67,67,2,1.8,NULL,NULL,'Disponible'),(68,68,2,1.8,NULL,NULL,'Disponible'),(69,69,2,0.9,NULL,NULL,'Disponible'),(70,70,2,0.9,NULL,NULL,'Disponible'),(71,71,2,0.45,NULL,NULL,'Disponible'),(72,72,2,6.3,NULL,NULL,'Disponible'),(73,73,2,2.7,NULL,NULL,'Disponible'),(74,74,2,2.7,NULL,NULL,'Disponible'),(75,75,2,1.8,NULL,NULL,'Disponible'),(76,76,2,0.9,NULL,NULL,'Disponible'),(77,77,2,0.9,NULL,NULL,'Disponible'),(78,78,2,0.45,NULL,NULL,'Disponible'),(79,79,2,0.18,NULL,NULL,'Disponible'),(80,80,2,0.36,NULL,NULL,'Disponible'),(81,81,2,0.36,NULL,NULL,'Disponible'),(82,82,2,1.8,NULL,NULL,'Disponible'),(83,83,2,0.9,NULL,NULL,'Disponible'),(84,84,2,0.9,NULL,NULL,'Disponible'),(85,85,2,0.45,NULL,NULL,'Disponible'),(86,86,2,0.45,NULL,NULL,'Disponible'),(87,87,2,0.9,NULL,NULL,'Disponible'),(88,88,2,0.9,NULL,NULL,'Disponible'),(89,89,2,0.9,NULL,NULL,'Disponible'),(90,90,2,0.45,NULL,NULL,'Disponible'),(91,91,2,1.8,NULL,NULL,'Disponible'),(92,92,2,0.9,NULL,NULL,'Disponible'),(93,93,2,0.9,NULL,NULL,'Disponible'),(94,94,2,0.9,NULL,NULL,'Disponible'),(95,95,2,1.8,NULL,NULL,'Disponible'),(96,96,2,0.9,NULL,NULL,'Disponible'),(97,97,2,0.9,NULL,NULL,'Disponible'),(98,1,3,16.25,NULL,NULL,'Disponible'),(99,2,3,7.5,7.221,0.279,'Consumido'),(100,3,3,10,NULL,NULL,'Disponible'),(101,4,3,7.5,NULL,NULL,'Disponible'),(102,5,3,3.75,NULL,NULL,'Disponible'),(103,6,3,2.5,2.349,0.151,'Consumido'),(104,7,3,5,NULL,NULL,'Disponible'),(105,8,3,12.5,NULL,NULL,'Disponible'),(106,9,3,8.75,NULL,NULL,'Disponible'),(107,10,3,8.75,NULL,NULL,'Disponible'),(108,11,3,3.75,NULL,NULL,'Disponible'),(109,12,3,3.75,NULL,NULL,'Disponible'),(110,13,3,6.25,NULL,NULL,'Disponible'),(111,14,3,2,NULL,NULL,'Disponible'),(112,15,3,1.75,NULL,NULL,'Disponible'),(113,16,3,7.5,NULL,NULL,'Disponible'),(114,17,3,5,NULL,NULL,'Disponible'),(115,18,3,6.25,NULL,NULL,'Disponible'),(116,19,3,5,NULL,NULL,'Disponible'),(117,20,3,2.5,NULL,NULL,'Disponible'),(118,21,3,6.25,NULL,NULL,'Disponible'),(119,22,3,3.75,NULL,NULL,'Disponible'),(120,23,3,1.75,NULL,NULL,'Disponible'),(121,24,3,16.25,NULL,NULL,'Disponible'),(122,25,3,12.5,NULL,NULL,'Disponible'),(123,26,3,5,NULL,NULL,'Disponible'),(124,27,3,7.5,NULL,NULL,'Disponible'),(125,28,3,3.75,NULL,NULL,'Disponible'),(126,29,3,5,NULL,NULL,'Disponible'),(127,30,3,3.75,NULL,NULL,'Disponible'),(128,31,3,2.5,NULL,NULL,'Disponible'),(129,32,3,7.5,NULL,NULL,'Disponible'),(130,33,3,5,NULL,NULL,'Disponible'),(131,34,3,5,NULL,NULL,'Disponible'),(132,35,3,2.5,NULL,NULL,'Disponible'),(133,36,3,5.75,NULL,NULL,'Disponible'),(134,37,3,8.75,NULL,NULL,'Disponible'),(135,38,3,2.5,NULL,NULL,'Disponible'),(136,39,3,2.5,NULL,NULL,'Disponible'),(137,40,3,5,NULL,NULL,'Disponible'),(138,41,3,2.5,NULL,NULL,'Disponible'),(139,42,3,1.25,NULL,NULL,'Disponible'),(140,43,3,3.75,NULL,NULL,'Disponible'),(141,44,3,2.5,NULL,NULL,'Disponible'),(142,45,3,1.25,NULL,NULL,'Disponible');
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carrito`
--

LOCK TABLES `carrito` WRITE;
/*!40000 ALTER TABLE `carrito` DISABLE KEYS */;
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
INSERT INTO `corte` VALUES (1,1,'','Diezmillo',0.065,0),(2,1,'','Aguja norteña',0.03,0),(3,1,'','Espaldilla',0.04,0),(4,1,'','Paleta',0.03,0),(5,1,'','Flat iron',0.015,0),(6,1,'','Filete de aguja',0.01,0),(7,1,'','Cuello',0.02,0),(8,1,'','Molida de chuck',0.05,0),(9,1,'','Recortes grasos',0.035,0),(10,1,'','Ribeye',0.035,0),(11,1,'','Cowboy steak',0.015,0),(12,1,'','Tomahawk',0.015,0),(13,1,'','Costilla cargada',0.025,0),(14,1,'','Costilla para BBQ',0.008,0),(15,1,'','Recortes rib',0.007,0),(16,1,'','T-bone',0.03,0),(17,1,'','Porterhouse',0.02,0),(18,1,'','New York strip',0.025,0),(19,1,'','Filete',0.02,0),(20,1,'','Chateaubriand',0.01,0),(21,1,'','Sirloin',0.025,0),(22,1,'','Top sirloin',0.015,0),(23,1,'','Tri-tip',0.007,0),(24,1,'','Bola',0.065,0),(25,1,'','Contra',0.05,0),(26,1,'','Cuete',0.02,0),(27,1,'','Tapa',0.03,0),(28,1,'','Culotte',0.015,0),(29,1,'','Milanesa',0.02,0),(30,1,'','Carne para deshebrar',0.015,0),(31,1,'','Recortes',0.01,0),(32,1,'','Arrachera',0.03,0),(33,1,'','Entraña',0.02,0),(34,1,'','Short ribs',0.02,0),(35,1,'','Falda deshebrada',0.01,0),(36,1,'','Recortes',0.023,0),(37,1,'','Vacío',0.035,0),(38,1,'','Bavette',0.01,0),(39,1,'','Recortes',0.01,0),(40,1,'','Brisket plano',0.02,0),(41,1,'','Brisket punta',0.01,0),(42,1,'','Pecho para cocido',0.005,0),(43,1,'','Chambarete delantero',0.015,0),(44,1,'','Chambarete trasero',0.01,0),(45,1,'','Osobuco',0.005,0),(46,2,'','Pierna de cerdo',0.09,0),(47,2,'','Pulpa de pierna',0.04,0),(48,2,'','Jamón fresco',0.03,0),(49,2,'','Jamón para curar',0.03,0),(50,2,'','Centro de jamón',0.01,0),(51,2,'','Punta de jamón',0.01,0),(52,2,'','Cuete de jamón',0.01,0),(53,2,'','Recortes de pierna',0.01,0),(54,2,'','Lomo entero',0.065,0),(55,2,'','Chuleta de lomo',0.045,0),(56,2,'','Chuleta ahumada',0.02,0),(57,2,'','Caña de lomo',0.01,0),(58,2,'','Medallón de lomo',0.01,0),(59,2,'','Lomo limpio',0.01,0),(60,2,'','Recortes de lomo',0.01,0),(61,2,'','Panceta',0.045,0),(62,2,'','Tocino',0.04,0),(63,2,'','Tocino ahumado',0.03,0),(64,2,'','Panceta en tiras',0.01,0),(65,2,'','Recortes de panceta',0.01,0),(66,2,'','Costilla de cerdo',0.04,0),(67,2,'','Costilla cargada',0.02,0),(68,2,'','Costilla baby back',0.02,0),(69,2,'','Costilla para BBQ',0.01,0),(70,2,'','Punta de costilla',0.01,0),(71,2,'','Recortes de costilla',0.005,0),(72,2,'','Paleta completa',0.07,0),(73,2,'','Pulpa de paleta',0.03,0),(74,2,'','Espaldilla de cerdo',0.03,0),(75,2,'','Bistec de paleta',0.02,0),(76,2,'','Recortes de paleta',0.01,0),(77,2,'','Cabeza de cerdo',0.01,0),(78,2,'','Cachete de cerdo',0.005,0),(79,2,'','Lengua de cerdo',0.002,0),(80,2,'','Oreja',0.004,0),(81,2,'','Morro',0.004,0),(82,2,'','Papada',0.02,0),(83,2,'','Papada para tocino',0.01,0),(84,2,'','Cuello',0.01,0),(85,2,'','Secreto ibérico',0.005,0),(86,2,'','Pluma',0.005,0),(87,2,'','Patas delanteras',0.01,0),(88,2,'','Patas traseras',0.01,0),(89,2,'','Manitas de cerdo',0.01,0),(90,2,'','Rabo',0.005,0),(91,2,'','Grasa dorsal',0.02,0),(92,2,'','Grasa abdominal',0.01,0),(93,2,'','Manteca',0.01,0),(94,2,'','Recortes generales',0.01,0),(95,2,'','Carne molida de cerdo',0.02,0),(96,2,'','Chicharrón',0.01,0),(97,2,'','Piel de cerdo',0.01,0),(98,3,'','Pechuga completa',0.18,0),(99,3,'','Pechuga deshuesada',0.06,0),(100,3,'','Filete de pechuga',0.04,0),(101,3,'','Pechuga con hueso',0.02,0),(102,3,'','Recortes de pechuga',0.02,0),(103,3,'','Muslo',0.14,0),(104,3,'','Pierna',0.1,0),(105,3,'','Pierna y muslo',0.06,0),(106,3,'','Muslo deshuesado',0.03,0),(107,3,'','Recortes de pierna',0.02,0),(108,3,'','Alas completas',0.06,0),(109,3,'','Alita',0.02,0),(110,3,'','Medio ala',0.02,0),(111,3,'','Punta de ala',0.02,0),(112,3,'','Carcasa',0.06,0),(113,3,'','Cuello',0.02,0),(114,3,'','Cabeza',0.01,0),(115,3,'','Patas de pollo',0.02,0),(116,3,'','Hígado',0.02,0),(117,3,'','Corazón',0.01,0),(118,3,'','Molleja',0.02,0),(119,3,'','Pulmones',0.005,0),(120,3,'','Grasa abdominal',0.01,0),(121,3,'','Piel de pollo',0.02,0),(122,3,'','Recortes generales',0.015,0),(123,4,'','Pierna de cordero',0.135,0),(124,4,'','Pierna deshuesada',0.04,0),(125,4,'','Centro de pierna',0.03,0),(126,4,'','Punta de pierna',0.02,0),(127,4,'','Cuete de pierna',0.02,0),(128,4,'','Bistec de pierna',0.01,0),(129,4,'','Recortes de pierna',0.02,0),(130,4,'','Lomo de cordero',0.05,0),(131,4,'','Chuleta de lomo',0.04,0),(132,4,'','Medallón de lomo',0.02,0),(133,4,'','Lomo limpio',0.02,0),(134,4,'','Recortes de lomo',0.03,0),(135,4,'','Costillar de cordero',0.06,0),(136,4,'','Rack de cordero',0.04,0),(137,4,'','Chuleta de costilla',0.03,0),(138,4,'','Punta de costilla',0.02,0),(139,4,'','Recortes de costilla',0.02,0),(140,4,'','Paleta de cordero',0.075,0),(141,4,'','Paleta deshuesada',0.03,0),(142,4,'','Pulpa de paleta',0.02,0),(143,4,'','Bistec de paleta',0.02,0),(144,4,'','Recortes de paleta',0.03,0),(145,4,'','Pecho de cordero',0.03,0),(146,4,'','Falda de cordero',0.03,0),(147,4,'','Costilla falda',0.02,0),(148,4,'','Recortes de falda',0.01,0),(149,4,'','Cuello de cordero',0.02,0),(150,4,'','Rodajas de cuello',0.01,0),(151,4,'','Cabeza de cordero',0.01,0),(152,4,'','Lengua de cordero',0.005,0),(153,4,'','Sesos',0.003,0),(154,4,'','Corazón',0.005,0),(155,4,'','Hígado',0.01,0),(156,4,'','Riñones',0.005,0),(157,4,'','Patas de cordero',0.01,0),(158,4,'','Rabo',0.002,0),(159,4,'','Grasa dorsal',0.01,0),(160,4,'','Grasa interna',0.005,0),(161,4,'','Sebo',0.005,0),(162,4,'','Huesos para caldo',0.02,0),(163,4,'','Carne molida de cordero',0.01,0);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `corte_unitario`
--

LOCK TABLES `corte_unitario` WRITE;
/*!40000 ALTER TABLE `corte_unitario` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lote`
--

LOCK TABLES `lote` WRITE;
/*!40000 ALTER TABLE `lote` DISABLE KEYS */;
INSERT INTO `lote` VALUES (1,NULL,2,1,'Abril1201',5,15,70.5,46,3450,'2026-06-12','Disponible',NULL),(2,2,NULL,NULL,'LP-Abr1201',1,7.234,0.234,0,0,'2026-04-19','Disponible',1),(3,6,NULL,NULL,'LP-Abr1202',1,2.25,2.25,0,0,'2026-04-19','Disponible',2),(4,99,NULL,NULL,'LP-Abr1203',1,7.221,5.221,0,0,'2026-04-19','Disponible',1),(5,NULL,NULL,NULL,'LP-Abr1204',1,1.5,1.5,0,0,'2026-04-19','Disponible',1),(6,NULL,NULL,NULL,'LP-Abr1205',1,1.5,1.5,0,0,'2026-04-19','Disponible',1),(7,103,NULL,NULL,'LP-Abr1206',1,2.349,2.349,0,0,'2026-04-19','Disponible',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materia_prima`
--

LOCK TABLES `materia_prima` WRITE;
/*!40000 ALTER TABLE `materia_prima` DISABLE KEYS */;
INSERT INTO `materia_prima` VALUES (37,'Canal de res completa',1,'Canal',NULL),(38,'Media canal de res',1,'Canal',NULL),(39,'Cuarto delantero de res',1,'Canal',NULL),(40,'Cuarto trasero de res',1,'Canal',NULL),(41,'Canal de cerdo completa',2,'Canal',NULL),(42,'Media canal de cerdo',2,'Canal',NULL),(43,'Pierna de cerdo',2,'Materia',NULL),(44,'Lomo de cerdo entero',2,'Materia',NULL),(45,'Pollo entero fresco',3,'Canal',NULL),(46,'Pollo entero congelado',3,'Canal',NULL),(47,'Pechuga de pollo entera',3,'Materia',NULL),(48,'Muslo con pierna de pollo',3,'Materia',NULL),(49,'Canal de borrego completa',4,'Canal',NULL),(50,'Media canal de borrego',4,'Canal',NULL),(51,'Pierna de borrego',4,'Materia',NULL),(52,'Costillar de borrego',4,'Producto',NULL),(53,'Salsa para marinar',5,'Materia',NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materia_proveida`
--

LOCK TABLES `materia_proveida` WRITE;
/*!40000 ALTER TABLE `materia_proveida` DISABLE KEYS */;
INSERT INTO `materia_proveida` VALUES (1,'Canal de res Bajío',10,37,1),(2,'Salsa para marinar FIC Le',9,53,10),(3,'Pollo entero Bajío',5,45,1),(4,'Canal de Cerdo Bajío',2,41,1),(8,'Res canal Empacadora',2,37,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orden_compra`
--

LOCK TABLES `orden_compra` WRITE;
/*!40000 ALTER TABLE `orden_compra` DISABLE KEYS */;
INSERT INTO `orden_compra` VALUES (1,9,'Abril1201','Recibida','2026-04-12',NULL,3450,'Pagado','Transferencia','2026-04-12 19:58:53',1,1),(2,2,'Abril1202','Recibida','2026-04-12',NULL,24500,'Pagado','Transferencia','2026-04-12 19:58:58',1,1),(3,2,'Abril1203','Recibida','2026-04-13',NULL,4005,'Pagado','Efectivo','2026-04-12 19:59:00',1,1),(4,2,'Abril1204','Recibida','2026-04-13',NULL,22500,'Pagado','Transferencia','2026-04-12 19:59:02',1,1);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona`
--

LOCK TABLES `persona` WRITE;
/*!40000 ALTER TABLE `persona` DISABLE KEYS */;
INSERT INTO `persona` VALUES (1,'Emmanuel','Ortiz','Reyes','4773845271','León, Gto',1),(2,'Emiliano','Mendoza','Maldonado','4776541234','direccion',2);
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
  `PrecioCompraProducto` float NOT NULL,
  `PrecioVentaProducto` float NOT NULL,
  `StockProducto` int NOT NULL,
  `idCategoria` int DEFAULT NULL,
  PRIMARY KEY (`idProducto`),
  UNIQUE KEY `NombreProducto` (`NombreProducto`),
  KEY `idCategoria` (`idCategoria`),
  CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`idCategoria`) REFERENCES `categoria` (`idCategoria`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,'10','Aguja Norteña marinada','Aguja norteña cortada y marinada con la salsa de congelados del bajío',1,130,17,1),(2,'11','Carne molida de Mixta','Molida de res con cerdo para hamburguesa, picadillo, etc.',1,90,2,1);
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
  `idOrdenCompra` int NOT NULL,
  PRIMARY KEY (`idProductoUnitario`),
  KEY `idProducto` (`idProducto`),
  KEY `idPedido` (`idPedido`),
  KEY `idCarrito` (`idCarrito`),
  KEY `idOrdenCompra` (`idOrdenCompra`),
  CONSTRAINT `producto_unitario_ibfk_1` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`idProducto`),
  CONSTRAINT `producto_unitario_ibfk_2` FOREIGN KEY (`idPedido`) REFERENCES `pedido` (`idPedido`),
  CONSTRAINT `producto_unitario_ibfk_3` FOREIGN KEY (`idCarrito`) REFERENCES `carrito` (`idCarrito`),
  CONSTRAINT `producto_unitario_ibfk_4` FOREIGN KEY (`idOrdenCompra`) REFERENCES `orden_compra` (`idOrdenCompra`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto_unitario`
--

LOCK TABLES `producto_unitario` WRITE;
/*!40000 ALTER TABLE `producto_unitario` DISABLE KEYS */;
/*!40000 ALTER TABLE `producto_unitario` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedor`
--

LOCK TABLES `proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor` DISABLE KEYS */;
INSERT INTO `proveedor` VALUES (1,'Rastro Frigorífico de León','RFL920315AB1','activo','Ing. José Martínez','4771234567','contacto@rastroleon.com','Blvd. Timoteo Lozano, León, Gto.','credito_15','Lunes, Miércoles, Viernes','Proveedor principal de canal de res','2026-04-10 11:47:04'),(2,'Empacadora de Carnes del Bajío','ECB010824KJ2','activo','Lic. Andrea Gómez','4772345678','ventas@ecbajio.mx','Parque Industrial León, Gto.','credito_30','Martes y Jueves','Distribución de carne de res en canal y cortes','2026-04-10 11:47:04'),(3,'Rastro Porcícola Guanajuato','RPG950612LM3','activo','Carlos Hernández','4621456789','ventas@rastroporcino.mx','Irapuato, Guanajuato','credito_15','Lunes a Viernes','Especialistas en canal de cerdo','2026-04-10 11:47:04'),(4,'Procesadora Porcina del Centro','PPC030921TR4','activo','María López','4773456789','contacto@ppcentro.mx','Silao, Guanajuato','credito_8','Martes, Jueves, Sábado','Venta de carne de cerdo fresca y congelada','2026-04-10 11:47:04'),(5,'Avícola Bajío S.A. de C.V.','ABA070515DF5','activo','Raúl Sánchez','4774567890','ventas@avicolabajio.mx','León, Guanajuato','contado','Diario','Suministro de pollo fresco entero y en piezas','2026-04-10 11:47:04'),(6,'Distribuidora Avícola Los Altos','DAL110223GH6','activo','Luis Ramírez','4741122334','pedidos@avicolalosaltos.mx','Lagos de Moreno, Jalisco','credito_8','Lunes a Sábado','Proveedor regional de pollo','2026-04-10 11:47:04'),(7,'Rastro Ovino del Bajío','ROB980731JK7','activo','Pedro Castillo','4775678901','contacto@ovinosbajio.mx','San Francisco del Rincón, Gto.','credito_15','Miércoles y Viernes','Venta de canal de borrego','2026-04-10 11:47:04'),(8,'Ganadera Ovina Guanajuato','GOG050912PL8','activo','Fernando Torres','4776789012','ventas@ganaderaovina.mx','Dolores Hidalgo, Gto.','credito_30','Martes y Jueves','Proveedor de borrego en pie y canal','2026-04-10 11:47:04'),(9,'Frigorífico Industrial del Centro','FIC020101MN9','activo','Alejandro Ruiz','4777890123','contacto@ficentro.mx','León, Guanajuato','credito_30','Lunes a Viernes','Manejan res, cerdo y pollo','2026-04-10 11:47:04'),(10,'Distribuidora Cárnica Integral Bajío','DCI140404QR1','activo','Sofía Navarro','4778901234','ventas@dcibajio.mx','Silao, Guanajuato','credito_15','Lunes, Miércoles, Viernes','Proveedor multi-especie','2026-04-10 11:47:04');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta`
--

LOCK TABLES `receta` WRITE;
/*!40000 ALTER TABLE `receta` DISABLE KEYS */;
INSERT INTO `receta` VALUES (1,'Aguja Norteña marinada',1,'10','Aguja norteña de res marinada con salsa FICL','MateriaPrima'),(2,'Carne molida de Mixta',2,'11','Carne molida con 50% Res y 50% Cerdo','MateriaPrima');
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta_materia_prima`
--

LOCK TABLES `receta_materia_prima` WRITE;
/*!40000 ALTER TABLE `receta_materia_prima` DISABLE KEYS */;
INSERT INTO `receta_materia_prima` VALUES (1,1,53,NULL,0.5),(2,1,NULL,2,1),(3,2,NULL,24,0.5),(4,2,NULL,72,0.5);
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `retiro`
--

LOCK TABLES `retiro` WRITE;
/*!40000 ALTER TABLE `retiro` DISABLE KEYS */;
INSERT INTO `retiro` VALUES (1,'2026-04-12 19:59:25','Ingreso','Efectivo',15679,'Corte de caja','emmanuelortizreyes3@gmail.com'),(2,'2026-04-12 19:59:55','Ingreso','Transferencia',20000,'Ingreso externo para compras de material','emmanuelortizreyes3@gmail.com'),(3,'2026-04-12 20:00:14','Ingreso','Efectivo',200000,'corte de casja','emmanuelortizreyes3@gmail.com'),(4,'2026-04-12 20:00:33','Ingreso','Transferencia',150000,'Deposito mensual','emmanuelortizreyes3@gmail.com');
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitud_produccion`
--

LOCK TABLES `solicitud_produccion` WRITE;
/*!40000 ALTER TABLE `solicitud_produccion` DISABLE KEYS */;
INSERT INTO `solicitud_produccion` VALUES (1,'Corte',NULL,2,1,'2026-04-12 15:10:41','2026-04-12 15:10:58','Completada',1,NULL),(2,'Personalizada',1,NULL,5,'2026-04-12 15:11:38','2026-04-12 15:12:03','Completada',1,NULL),(3,'Personalizada',1,NULL,2,'2026-04-12 15:16:10','2026-04-12 15:16:41','Completada',2,NULL),(4,'Corte',NULL,6,1,'2026-04-12 15:21:50','2026-04-12 15:22:13','Completada',1,NULL),(5,'Corte',NULL,2,1,'2026-04-12 20:08:13','2026-04-12 20:08:23','Completada',1,NULL),(6,'Personalizada',1,NULL,1,'2026-04-12 20:08:41','2026-04-12 20:08:46','Completada',1,NULL),(7,'Personalizada',1,NULL,1,'2026-04-12 20:09:05','2026-04-12 20:11:45','Completada',1,NULL),(8,'Corte',NULL,6,1,'2026-04-12 20:11:55','2026-04-12 20:12:06','Completada',1,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitud_produccion_detalle`
--

LOCK TABLES `solicitud_produccion_detalle` WRITE;
/*!40000 ALTER TABLE `solicitud_produccion_detalle` DISABLE KEYS */;
INSERT INTO `solicitud_produccion_detalle` VALUES (1,1,NULL,NULL,2,2,7.234),(2,2,53,1,NULL,NULL,2.5),(3,2,NULL,2,NULL,NULL,5),(4,3,53,1,NULL,NULL,1),(5,3,NULL,2,NULL,NULL,2),(6,4,NULL,NULL,6,3,2.25),(7,5,NULL,NULL,99,4,7.221),(8,6,53,1,NULL,5,0.5),(9,6,NULL,4,NULL,5,1),(10,7,53,1,NULL,6,0.5),(11,7,NULL,4,NULL,6,1),(12,8,NULL,NULL,103,7,2.349);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Emmanuel Ortiz Reyes','emmanuelortizreyes3@gmail.com','$pbkdf2-sha512$25000$lpIy5tw7h9A657zX2ruXUg$FLJzebSVJOnvHCd21ufikAlJvTuISK2JW/D3soHImEdpO8vBSoGhXrbg/741oBx74JiE/ojw3ISYKdaMIpV5RA','c9a0e91a6e3149eca6c1dd978056d626',1,NULL,0,NULL,'2026-04-12 20:16:20','127.0.0.1','e49ad047-a82b-4d44-981f-304cbf6ee4cd','2026-04-19 20:17:28',NULL),(2,'Emiliano Mendoza Maldonado','LaRESpuestaAdmin@gmail.com','$pbkdf2-sha512$25000$/p8T4rz3vhcCAIAwxjjHGA$CiQADPETxg.URykmVnVNspvP5oX.o24.pgSHj8Z6Zx2lpg5zeH3FWIrZUcc1eQ.JCWl5XE.K.ifpOey2rTvrFA','ba80e921f9bf41bc9b85dc8486bbf48d',1,NULL,0,NULL,'2026-04-12 15:15:48','127.0.0.1','c5b2f101-59c0-4985-ab48-1e8e969ae187','2026-04-19 20:16:39',NULL);
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
INSERT INTO `users_roles` VALUES (1,1),(2,1);
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

-- Dump completed on 2026-04-12 20:17:28
