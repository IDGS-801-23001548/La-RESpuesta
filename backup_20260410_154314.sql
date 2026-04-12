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
INSERT INTO `canal` VALUES (1,1,1,'Canal de res completa',234,'2026-04-10','Disponible'),(2,3,3,'Pollo entero fresco',2,'2026-04-10','Disponible'),(3,2,4,'Canal de cerdo completa',84,'2026-04-10','Disponible');
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
) ENGINE=InnoDB AUTO_INCREMENT=123 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `canal_corte`
--

LOCK TABLES `canal_corte` WRITE;
/*!40000 ALTER TABLE `canal_corte` DISABLE KEYS */;
INSERT INTO `canal_corte` VALUES (1,1,1,15.21,NULL,NULL,'Disponible'),(2,2,1,7.02,6.8,0.22,'Consumido'),(3,3,1,9.36,NULL,NULL,'Disponible'),(4,4,1,7.02,NULL,NULL,'Disponible'),(5,5,1,3.51,NULL,NULL,'Disponible'),(6,6,1,2.34,NULL,NULL,'Disponible'),(7,7,1,4.68,NULL,NULL,'Disponible'),(8,8,1,11.7,NULL,NULL,'Disponible'),(9,9,1,8.19,NULL,NULL,'Disponible'),(10,10,1,8.19,NULL,NULL,'Disponible'),(11,11,1,3.51,NULL,NULL,'Disponible'),(12,12,1,3.51,NULL,NULL,'Disponible'),(13,13,1,5.85,NULL,NULL,'Disponible'),(14,14,1,1.872,NULL,NULL,'Disponible'),(15,15,1,1.638,NULL,NULL,'Disponible'),(16,16,1,7.02,NULL,NULL,'Disponible'),(17,17,1,4.68,NULL,NULL,'Disponible'),(18,18,1,5.85,NULL,NULL,'Disponible'),(19,19,1,4.68,4,0.68,'Consumido'),(20,20,1,2.34,NULL,NULL,'Disponible'),(21,21,1,5.85,NULL,NULL,'Disponible'),(22,22,1,3.51,NULL,NULL,'Disponible'),(23,23,1,1.638,NULL,NULL,'Disponible'),(24,24,1,15.21,14.224,0.986,'Consumido'),(25,25,1,11.7,NULL,NULL,'Disponible'),(26,26,1,4.68,NULL,NULL,'Disponible'),(27,27,1,7.02,NULL,NULL,'Disponible'),(28,28,1,3.51,NULL,NULL,'Disponible'),(29,29,1,4.68,NULL,NULL,'Disponible'),(30,30,1,3.51,NULL,NULL,'Disponible'),(31,31,1,2.34,NULL,NULL,'Disponible'),(32,32,1,7.02,NULL,NULL,'Disponible'),(33,33,1,4.68,NULL,NULL,'Disponible'),(34,34,1,4.68,NULL,NULL,'Disponible'),(35,35,1,2.34,NULL,NULL,'Disponible'),(36,36,1,5.382,NULL,NULL,'Disponible'),(37,37,1,8.19,NULL,NULL,'Disponible'),(38,38,1,2.34,NULL,NULL,'Disponible'),(39,39,1,2.34,NULL,NULL,'Disponible'),(40,40,1,4.68,NULL,NULL,'Disponible'),(41,41,1,2.34,NULL,NULL,'Disponible'),(42,42,1,1.17,NULL,NULL,'Disponible'),(43,43,1,3.51,NULL,NULL,'Disponible'),(44,44,1,2.34,NULL,NULL,'Disponible'),(45,45,1,1.17,NULL,NULL,'Disponible'),(46,98,2,0.36,0.32,0.04,'Consumido'),(47,99,2,0.12,NULL,NULL,'Disponible'),(48,100,2,0.08,NULL,NULL,'Disponible'),(49,101,2,0.04,NULL,NULL,'Disponible'),(50,102,2,0.04,NULL,NULL,'Disponible'),(51,103,2,0.28,NULL,NULL,'Disponible'),(52,104,2,0.2,NULL,NULL,'Disponible'),(53,105,2,0.12,NULL,NULL,'Disponible'),(54,106,2,0.06,NULL,NULL,'Disponible'),(55,107,2,0.04,NULL,NULL,'Disponible'),(56,108,2,0.12,NULL,NULL,'Disponible'),(57,109,2,0.04,NULL,NULL,'Disponible'),(58,110,2,0.04,NULL,NULL,'Disponible'),(59,111,2,0.04,NULL,NULL,'Disponible'),(60,112,2,0.12,NULL,NULL,'Disponible'),(61,113,2,0.04,NULL,NULL,'Disponible'),(62,114,2,0.02,NULL,NULL,'Disponible'),(63,115,2,0.04,NULL,NULL,'Disponible'),(64,116,2,0.04,NULL,NULL,'Disponible'),(65,117,2,0.02,NULL,NULL,'Disponible'),(66,118,2,0.04,NULL,NULL,'Disponible'),(67,119,2,0.01,NULL,NULL,'Disponible'),(68,120,2,0.02,NULL,NULL,'Disponible'),(69,121,2,0.04,NULL,NULL,'Disponible'),(70,122,2,0.03,NULL,NULL,'Disponible'),(71,46,3,7.56,NULL,NULL,'Disponible'),(72,47,3,3.36,NULL,NULL,'Disponible'),(73,48,3,2.52,NULL,NULL,'Disponible'),(74,49,3,2.52,NULL,NULL,'Disponible'),(75,50,3,0.84,NULL,NULL,'Disponible'),(76,51,3,0.84,NULL,NULL,'Disponible'),(77,52,3,0.84,NULL,NULL,'Disponible'),(78,53,3,0.84,NULL,NULL,'Disponible'),(79,54,3,5.46,NULL,NULL,'Disponible'),(80,55,3,3.78,NULL,NULL,'Disponible'),(81,56,3,1.68,NULL,NULL,'Disponible'),(82,57,3,0.84,NULL,NULL,'Disponible'),(83,58,3,0.84,NULL,NULL,'Disponible'),(84,59,3,0.84,NULL,NULL,'Disponible'),(85,60,3,0.84,NULL,NULL,'Disponible'),(86,61,3,3.78,NULL,NULL,'Disponible'),(87,62,3,3.36,NULL,NULL,'Disponible'),(88,63,3,2.52,NULL,NULL,'Disponible'),(89,64,3,0.84,NULL,NULL,'Disponible'),(90,65,3,0.84,NULL,NULL,'Disponible'),(91,66,3,3.36,NULL,NULL,'Disponible'),(92,67,3,1.68,NULL,NULL,'Disponible'),(93,68,3,1.68,NULL,NULL,'Disponible'),(94,69,3,0.84,NULL,NULL,'Disponible'),(95,70,3,0.84,NULL,NULL,'Disponible'),(96,71,3,0.42,NULL,NULL,'Disponible'),(97,72,3,5.88,NULL,NULL,'Disponible'),(98,73,3,2.52,2.345,0.175,'Consumido'),(99,74,3,2.52,NULL,NULL,'Disponible'),(100,75,3,1.68,NULL,NULL,'Disponible'),(101,76,3,0.84,NULL,NULL,'Disponible'),(102,77,3,0.84,NULL,NULL,'Disponible'),(103,78,3,0.42,NULL,NULL,'Disponible'),(104,79,3,0.168,NULL,NULL,'Disponible'),(105,80,3,0.336,NULL,NULL,'Disponible'),(106,81,3,0.336,NULL,NULL,'Disponible'),(107,82,3,1.68,NULL,NULL,'Disponible'),(108,83,3,0.84,NULL,NULL,'Disponible'),(109,84,3,0.84,NULL,NULL,'Disponible'),(110,85,3,0.42,NULL,NULL,'Disponible'),(111,86,3,0.42,NULL,NULL,'Disponible'),(112,87,3,0.84,NULL,NULL,'Disponible'),(113,88,3,0.84,NULL,NULL,'Disponible'),(114,89,3,0.84,NULL,NULL,'Disponible'),(115,90,3,0.42,NULL,NULL,'Disponible'),(116,91,3,1.68,NULL,NULL,'Disponible'),(117,92,3,0.84,NULL,NULL,'Disponible'),(118,93,3,0.84,NULL,NULL,'Disponible'),(119,94,3,0.84,NULL,NULL,'Disponible'),(120,95,3,1.68,NULL,NULL,'Disponible'),(121,96,3,0.84,NULL,NULL,'Disponible'),(122,97,3,0.84,NULL,NULL,'Disponible');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
INSERT INTO `corte` VALUES (1,1,NULL,'Diezmillo',0.065),(2,1,NULL,'Aguja norteña',0.03),(3,1,NULL,'Espaldilla',0.04),(4,1,NULL,'Paleta',0.03),(5,1,NULL,'Flat iron',0.015),(6,1,NULL,'Filete de aguja',0.01),(7,1,NULL,'Cuello',0.02),(8,1,NULL,'Molida de chuck',0.05),(9,1,NULL,'Recortes grasos',0.035),(10,1,NULL,'Ribeye',0.035),(11,1,NULL,'Cowboy steak',0.015),(12,1,NULL,'Tomahawk',0.015),(13,1,NULL,'Costilla cargada',0.025),(14,1,NULL,'Costilla para BBQ',0.008),(15,1,NULL,'Recortes rib',0.007),(16,1,NULL,'T-bone',0.03),(17,1,NULL,'Porterhouse',0.02),(18,1,NULL,'New York strip',0.025),(19,1,NULL,'Filete',0.02),(20,1,NULL,'Chateaubriand',0.01),(21,1,NULL,'Sirloin',0.025),(22,1,NULL,'Top sirloin',0.015),(23,1,NULL,'Tri-tip',0.007),(24,1,NULL,'Bola',0.065),(25,1,NULL,'Contra',0.05),(26,1,NULL,'Cuete',0.02),(27,1,NULL,'Tapa',0.03),(28,1,NULL,'Culotte',0.015),(29,1,NULL,'Milanesa',0.02),(30,1,NULL,'Carne para deshebrar',0.015),(31,1,NULL,'Recortes',0.01),(32,1,NULL,'Arrachera',0.03),(33,1,NULL,'Entraña',0.02),(34,1,NULL,'Short ribs',0.02),(35,1,NULL,'Falda deshebrada',0.01),(36,1,NULL,'Recortes',0.023),(37,1,NULL,'Vacío',0.035),(38,1,NULL,'Bavette',0.01),(39,1,NULL,'Recortes',0.01),(40,1,NULL,'Brisket plano',0.02),(41,1,NULL,'Brisket punta',0.01),(42,1,NULL,'Pecho para cocido',0.005),(43,1,NULL,'Chambarete delantero',0.015),(44,1,NULL,'Chambarete trasero',0.01),(45,1,NULL,'Osobuco',0.005),(46,2,NULL,'Pierna de cerdo',0.09),(47,2,NULL,'Pulpa de pierna',0.04),(48,2,NULL,'Jamón fresco',0.03),(49,2,NULL,'Jamón para curar',0.03),(50,2,NULL,'Centro de jamón',0.01),(51,2,NULL,'Punta de jamón',0.01),(52,2,NULL,'Cuete de jamón',0.01),(53,2,NULL,'Recortes de pierna',0.01),(54,2,NULL,'Lomo entero',0.065),(55,2,NULL,'Chuleta de lomo',0.045),(56,2,NULL,'Chuleta ahumada',0.02),(57,2,NULL,'Caña de lomo',0.01),(58,2,NULL,'Medallón de lomo',0.01),(59,2,NULL,'Lomo limpio',0.01),(60,2,NULL,'Recortes de lomo',0.01),(61,2,NULL,'Panceta',0.045),(62,2,NULL,'Tocino',0.04),(63,2,NULL,'Tocino ahumado',0.03),(64,2,NULL,'Panceta en tiras',0.01),(65,2,NULL,'Recortes de panceta',0.01),(66,2,NULL,'Costilla de cerdo',0.04),(67,2,NULL,'Costilla cargada',0.02),(68,2,NULL,'Costilla baby back',0.02),(69,2,NULL,'Costilla para BBQ',0.01),(70,2,NULL,'Punta de costilla',0.01),(71,2,NULL,'Recortes de costilla',0.005),(72,2,NULL,'Paleta completa',0.07),(73,2,NULL,'Pulpa de paleta',0.03),(74,2,NULL,'Espaldilla de cerdo',0.03),(75,2,NULL,'Bistec de paleta',0.02),(76,2,NULL,'Recortes de paleta',0.01),(77,2,NULL,'Cabeza de cerdo',0.01),(78,2,NULL,'Cachete de cerdo',0.005),(79,2,NULL,'Lengua de cerdo',0.002),(80,2,NULL,'Oreja',0.004),(81,2,NULL,'Morro',0.004),(82,2,NULL,'Papada',0.02),(83,2,NULL,'Papada para tocino',0.01),(84,2,NULL,'Cuello',0.01),(85,2,NULL,'Secreto ibérico',0.005),(86,2,NULL,'Pluma',0.005),(87,2,NULL,'Patas delanteras',0.01),(88,2,NULL,'Patas traseras',0.01),(89,2,NULL,'Manitas de cerdo',0.01),(90,2,NULL,'Rabo',0.005),(91,2,NULL,'Grasa dorsal',0.02),(92,2,NULL,'Grasa abdominal',0.01),(93,2,NULL,'Manteca',0.01),(94,2,NULL,'Recortes generales',0.01),(95,2,NULL,'Carne molida de cerdo',0.02),(96,2,NULL,'Chicharrón',0.01),(97,2,NULL,'Piel de cerdo',0.01),(98,3,NULL,'Pechuga completa',0.18),(99,3,NULL,'Pechuga deshuesada',0.06),(100,3,NULL,'Filete de pechuga',0.04),(101,3,NULL,'Pechuga con hueso',0.02),(102,3,NULL,'Recortes de pechuga',0.02),(103,3,NULL,'Muslo',0.14),(104,3,NULL,'Pierna',0.1),(105,3,NULL,'Pierna y muslo',0.06),(106,3,NULL,'Muslo deshuesado',0.03),(107,3,NULL,'Recortes de pierna',0.02),(108,3,NULL,'Alas completas',0.06),(109,3,NULL,'Alita',0.02),(110,3,NULL,'Medio ala',0.02),(111,3,NULL,'Punta de ala',0.02),(112,3,NULL,'Carcasa',0.06),(113,3,NULL,'Cuello',0.02),(114,3,NULL,'Cabeza',0.01),(115,3,NULL,'Patas de pollo',0.02),(116,3,NULL,'Hígado',0.02),(117,3,NULL,'Corazón',0.01),(118,3,NULL,'Molleja',0.02),(119,3,NULL,'Pulmones',0.005),(120,3,NULL,'Grasa abdominal',0.01),(121,3,NULL,'Piel de pollo',0.02),(122,3,NULL,'Recortes generales',0.015),(123,4,NULL,'Pierna de cordero',0.135),(124,4,NULL,'Pierna deshuesada',0.04),(125,4,NULL,'Centro de pierna',0.03),(126,4,NULL,'Punta de pierna',0.02),(127,4,NULL,'Cuete de pierna',0.02),(128,4,NULL,'Bistec de pierna',0.01),(129,4,NULL,'Recortes de pierna',0.02),(130,4,NULL,'Lomo de cordero',0.05),(131,4,NULL,'Chuleta de lomo',0.04),(132,4,NULL,'Medallón de lomo',0.02),(133,4,NULL,'Lomo limpio',0.02),(134,4,NULL,'Recortes de lomo',0.03),(135,4,NULL,'Costillar de cordero',0.06),(136,4,NULL,'Rack de cordero',0.04),(137,4,NULL,'Chuleta de costilla',0.03),(138,4,NULL,'Punta de costilla',0.02),(139,4,NULL,'Recortes de costilla',0.02),(140,4,NULL,'Paleta de cordero',0.075),(141,4,NULL,'Paleta deshuesada',0.03),(142,4,NULL,'Pulpa de paleta',0.02),(143,4,NULL,'Bistec de paleta',0.02),(144,4,NULL,'Recortes de paleta',0.03),(145,4,NULL,'Pecho de cordero',0.03),(146,4,NULL,'Falda de cordero',0.03),(147,4,NULL,'Costilla falda',0.02),(148,4,NULL,'Recortes de falda',0.01),(149,4,NULL,'Cuello de cordero',0.02),(150,4,NULL,'Rodajas de cuello',0.01),(151,4,NULL,'Cabeza de cordero',0.01),(152,4,NULL,'Lengua de cordero',0.005),(153,4,NULL,'Sesos',0.003),(154,4,NULL,'Corazón',0.005),(155,4,NULL,'Hígado',0.01),(156,4,NULL,'Riñones',0.005),(157,4,NULL,'Patas de cordero',0.01),(158,4,NULL,'Rabo',0.002),(159,4,NULL,'Grasa dorsal',0.01),(160,4,NULL,'Grasa interna',0.005),(161,4,NULL,'Sebo',0.005),(162,4,NULL,'Huesos para caldo',0.02),(163,4,NULL,'Carne molida de cordero',0.01);
/*!40000 ALTER TABLE `corte` ENABLE KEYS */;
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
  PRIMARY KEY (`idLote`),
  KEY `idCanalCorte` (`idCanalCorte`),
  KEY `idMateriaProveida` (`idMateriaProveida`),
  KEY `idOrdenCompra` (`idOrdenCompra`),
  CONSTRAINT `lote_ibfk_1` FOREIGN KEY (`idCanalCorte`) REFERENCES `canal_corte` (`idCanalCorte`),
  CONSTRAINT `lote_ibfk_2` FOREIGN KEY (`idMateriaProveida`) REFERENCES `materia_proveida` (`idMateriaProveida`),
  CONSTRAINT `lote_ibfk_3` FOREIGN KEY (`idOrdenCompra`) REFERENCES `orden_compra` (`idOrdenCompra`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lote`
--

LOCK TABLES `lote` WRITE;
/*!40000 ALTER TABLE `lote` DISABLE KEYS */;
INSERT INTO `lote` VALUES (1,2,NULL,NULL,'LP-Abr1001',1,6.8,6.8,0,0,NULL,'Disponible'),(2,19,NULL,NULL,'LP-Abr1002',1,4,4,0,0,NULL,'Disponible'),(3,NULL,2,2,'Abril1002',20,1,20,32,640,'2026-06-24','Disponible'),(4,46,NULL,NULL,'LP-Abr1003',1,0.32,0.32,0,0,NULL,'Disponible'),(5,24,NULL,NULL,'LP-Abr1004',1,14.224,14.224,0,0,NULL,'Disponible'),(6,98,NULL,NULL,'LP-Abr1005',1,2.345,2.345,0,0,NULL,'Disponible');
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
  `nombreMateriaPrima` varchar(60) DEFAULT NULL,
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
  PRIMARY KEY (`idOrdenCompra`),
  UNIQUE KEY `numeroLote` (`numeroLote`),
  KEY `idProveedor` (`idProveedor`),
  CONSTRAINT `orden_compra_ibfk_1` FOREIGN KEY (`idProveedor`) REFERENCES `proveedor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orden_compra`
--

LOCK TABLES `orden_compra` WRITE;
/*!40000 ALTER TABLE `orden_compra` DISABLE KEYS */;
INSERT INTO `orden_compra` VALUES (1,10,'Abril1001','Recibida','2026-04-10',NULL,2034,'Pendiente',NULL,NULL),(2,9,'Abril1002','Recibida','2026-04-10',NULL,640,'Pendiente',NULL,NULL),(3,5,'Abril1003','Recibida','2026-04-10',NULL,55,'Pendiente',NULL,NULL),(4,2,'Abril1004','Recibida','2026-04-10',NULL,4158,'Pendiente',NULL,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona`
--

LOCK TABLES `persona` WRITE;
/*!40000 ALTER TABLE `persona` DISABLE KEYS */;
INSERT INTO `persona` VALUES (1,'admin','admin','admin','4773845271','León, Gto',1);
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
INSERT INTO `producto` VALUES (1,'10','Aguja Norteña marinada','Aguja norteña cortada y marinada con la salsa de congelados del bajío',1,130,0,1),(2,'11','Carne molida de Mixta','Molida de res con cerdo para hamburguesa, picadillo, etc.',1,90,0,1);
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
INSERT INTO `receta` VALUES (1,'Aguja Norteña marinada',1,'10','Aguja norteña marinada con salsa para marinar FIC Le','MateriaPrima'),(2,'Carne molida de Mixta',2,'11','Molida de res y cerdo','MateriaPrima');
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
  KEY `fk_rmp_corte` (`idCorte`),
  CONSTRAINT `fk_rmp_corte` FOREIGN KEY (`idCorte`) REFERENCES `corte` (`idCorte`),
  CONSTRAINT `receta_materia_prima_ibfk_1` FOREIGN KEY (`idReceta`) REFERENCES `receta` (`idReceta`),
  CONSTRAINT `receta_materia_prima_ibfk_2` FOREIGN KEY (`idMateriaPrima`) REFERENCES `materia_prima` (`idMateriaPrima`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta_materia_prima`
--

LOCK TABLES `receta_materia_prima` WRITE;
/*!40000 ALTER TABLE `receta_materia_prima` DISABLE KEYS */;
INSERT INTO `receta_materia_prima` VALUES (1,1,53,NULL,0.5),(2,1,NULL,2,1),(3,2,NULL,24,0.5),(4,2,NULL,73,0.5);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `retiro`
--

LOCK TABLES `retiro` WRITE;
/*!40000 ALTER TABLE `retiro` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitud_produccion`
--

LOCK TABLES `solicitud_produccion` WRITE;
/*!40000 ALTER TABLE `solicitud_produccion` DISABLE KEYS */;
INSERT INTO `solicitud_produccion` VALUES (1,'Corte',NULL,2,1,'2026-04-10 12:30:17','2026-04-10 12:30:17','Completada',1,NULL),(2,'Corte',NULL,19,1,'2026-04-10 12:35:21','2026-04-10 12:35:21','Completada',1,NULL),(3,'Corte',NULL,98,1,'2026-04-10 14:33:28','2026-04-10 14:34:02','Completada',1,'Falta pechuga de pollo'),(4,'Corte',NULL,24,1,'2026-04-10 15:15:34','2026-04-10 15:15:55','Completada',1,NULL),(5,'Corte',NULL,73,1,'2026-04-10 15:20:10','2026-04-10 15:20:34','Completada',1,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitud_produccion_detalle`
--

LOCK TABLES `solicitud_produccion_detalle` WRITE;
/*!40000 ALTER TABLE `solicitud_produccion_detalle` DISABLE KEYS */;
INSERT INTO `solicitud_produccion_detalle` VALUES (1,1,NULL,NULL,2,1,6.8),(2,2,NULL,NULL,19,2,4),(3,3,NULL,NULL,46,4,0.32),(4,4,NULL,NULL,24,5,14.224),(5,5,NULL,NULL,98,6,2.345);
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','emmanuelortizreyes3@gmail.com','$pbkdf2-sha512$25000$SEnJOUeotdZ6T.ndGwNgzA$K/vnlKNd.t8LZzK./ijSmNf.CLcQpH71yC2B.5XTbB6OxZWzlKF6JMoXWz8Uo3SwLJy263t0eDqgtIBBJw15XQ','6342a26a50764f5ca4188ae8057f4677',1,NULL,0,NULL,'2026-04-10 11:49:08','127.0.0.1','a4e4a5ec-17ec-4215-a7b7-2cf360505bd6','2026-04-17 15:43:14',NULL);
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
INSERT INTO `users_roles` VALUES (1,1);
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

-- Dump completed on 2026-04-10 15:43:14
