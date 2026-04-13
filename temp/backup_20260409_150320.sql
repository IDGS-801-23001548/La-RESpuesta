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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `canal`
--

LOCK TABLES `canal` WRITE;
/*!40000 ALTER TABLE `canal` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `canal_corte`
--

LOCK TABLES `canal_corte` WRITE;
/*!40000 ALTER TABLE `canal_corte` DISABLE KEYS */;
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
INSERT INTO `corte` VALUES (1,1,NULL,'Diezmillo',0.065),(2,1,NULL,'Aguja norteña',0.03),(3,1,NULL,'Espaldilla',0.04),(4,1,NULL,'Paleta',0.03),(5,1,NULL,'Flat iron',0.015),(6,1,NULL,'Filete de aguja',0.01),(7,1,NULL,'Cuello',0.02),(8,1,NULL,'Molida de chuck',0.05),(9,1,NULL,'Recortes grasos',0.035),(10,1,NULL,'Ribeye',0.035),(11,1,NULL,'Cowboy steak',0.015),(12,1,NULL,'Tomahawk',0.015),(13,1,NULL,'Costilla cargada',0.025),(14,1,NULL,'Costilla para BBQ',0.008),(15,1,NULL,'Recortes rib',0.007),(16,1,NULL,'T-bone',0.03),(17,1,NULL,'Porterhouse',0.02),(18,1,NULL,'New York strip',0.025),(19,1,NULL,'Filete',0.02),(20,1,NULL,'Chateaubriand',0.01),(21,1,NULL,'Sirloin',0.025),(22,1,NULL,'Top sirloin',0.015),(23,1,NULL,'Tri-tip',0.007),(24,1,NULL,'Bola',0.065),(25,1,NULL,'Contra',0.05),(26,1,NULL,'Cuete',0.02),(27,1,NULL,'Tapa',0.03),(28,1,NULL,'Culotte',0.015),(29,1,NULL,'Milanesa',0.02),(30,1,NULL,'Carne para deshebrar',0.015),(31,1,NULL,'Recortes',0.01),(32,1,NULL,'Arrachera',0.03),(33,1,NULL,'Entraña',0.02),(34,1,NULL,'Short ribs',0.02),(35,1,NULL,'Falda deshebrada',0.01),(36,1,NULL,'Recortes',0.023),(37,1,NULL,'Vacío',0.035),(38,1,NULL,'Bavette',0.01),(39,1,NULL,'Recortes',0.01),(40,1,NULL,'Brisket plano',0.02),(41,1,NULL,'Brisket punta',0.01),(42,1,NULL,'Pecho para cocido',0.005),(43,1,NULL,'Chambarete delantero',0.015),(44,1,NULL,'Chambarete trasero',0.01),(45,1,NULL,'Osobuco',0.005),(46,2,NULL,'Pierna de cerdo',9),(47,2,NULL,'Pulpa de pierna',4),(48,2,NULL,'Jamón fresco',3),(49,2,NULL,'Jamón para curar',3),(50,2,NULL,'Centro de jamón',1),(51,2,NULL,'Punta de jamón',1),(52,2,NULL,'Cuete de jamón',1),(53,2,NULL,'Recortes de pierna',1),(54,2,NULL,'Lomo entero',6.5),(55,2,NULL,'Chuleta de lomo',4.5),(56,2,NULL,'Chuleta ahumada',2),(57,2,NULL,'Caña de lomo',1),(58,2,NULL,'Medallón de lomo',1),(59,2,NULL,'Lomo limpio',1),(60,2,NULL,'Recortes de lomo',1),(61,2,NULL,'Panceta',4.5),(62,2,NULL,'Tocino',4),(63,2,NULL,'Tocino ahumado',3),(64,2,NULL,'Panceta en tiras',1),(65,2,NULL,'Recortes de panceta',1),(66,2,NULL,'Costilla de cerdo',4),(67,2,NULL,'Costilla cargada',2),(68,2,NULL,'Costilla baby back',2),(69,2,NULL,'Costilla para BBQ',1),(70,2,NULL,'Punta de costilla',1),(71,2,NULL,'Recortes de costilla',0.5),(72,2,NULL,'Paleta completa',7),(73,2,NULL,'Pulpa de paleta',3),(74,2,NULL,'Espaldilla de cerdo',3),(75,2,NULL,'Bistec de paleta',2),(76,2,NULL,'Recortes de paleta',1),(77,2,NULL,'Cabeza de cerdo',1),(78,2,NULL,'Cachete de cerdo',0.5),(79,2,NULL,'Lengua de cerdo',0.2),(80,2,NULL,'Oreja',0.4),(81,2,NULL,'Morro',0.4),(82,2,NULL,'Papada',2),(83,2,NULL,'Papada para tocino',1),(84,2,NULL,'Cuello',1),(85,2,NULL,'Secreto ibérico',0.5),(86,2,NULL,'Pluma',0.5),(87,2,NULL,'Patas delanteras',1),(88,2,NULL,'Patas traseras',1),(89,2,NULL,'Manitas de cerdo',1),(90,2,NULL,'Rabo',0.5),(91,2,NULL,'Grasa dorsal',2),(92,2,NULL,'Grasa abdominal',1),(93,2,NULL,'Manteca',1),(94,2,NULL,'Recortes generales',1),(95,2,NULL,'Carne molida de cerdo',2),(96,2,NULL,'Chicharrón',1),(97,2,NULL,'Piel de cerdo',1),(98,3,NULL,'Pechuga completa',18),(99,3,NULL,'Pechuga deshuesada',6),(100,3,NULL,'Filete de pechuga',4),(101,3,NULL,'Pechuga con hueso',2),(102,3,NULL,'Recortes de pechuga',2),(103,3,NULL,'Muslo',14),(104,3,NULL,'Pierna',10),(105,3,NULL,'Pierna y muslo',6),(106,3,NULL,'Muslo deshuesado',3),(107,3,NULL,'Recortes de pierna',2),(108,3,NULL,'Alas completas',6),(109,3,NULL,'Alita',2),(110,3,NULL,'Medio ala',2),(111,3,NULL,'Punta de ala',2),(112,3,NULL,'Carcasa',6),(113,3,NULL,'Cuello',2),(114,3,NULL,'Cabeza',1),(115,3,NULL,'Patas de pollo',2),(116,3,NULL,'Hígado',2),(117,3,NULL,'Corazón',1),(118,3,NULL,'Molleja',2),(119,3,NULL,'Pulmones',0.5),(120,3,NULL,'Grasa abdominal',1),(121,3,NULL,'Piel de pollo',2),(122,3,NULL,'Recortes generales',1.5),(123,4,NULL,'Pierna de cordero',13.5),(124,4,NULL,'Pierna deshuesada',4),(125,4,NULL,'Centro de pierna',3),(126,4,NULL,'Punta de pierna',2),(127,4,NULL,'Cuete de pierna',2),(128,4,NULL,'Bistec de pierna',1),(129,4,NULL,'Recortes de pierna',2),(130,4,NULL,'Lomo de cordero',5),(131,4,NULL,'Chuleta de lomo',4),(132,4,NULL,'Medallón de lomo',2),(133,4,NULL,'Lomo limpio',2),(134,4,NULL,'Recortes de lomo',3),(135,4,NULL,'Costillar de cordero',6),(136,4,NULL,'Rack de cordero',4),(137,4,NULL,'Chuleta de costilla',3),(138,4,NULL,'Punta de costilla',2),(139,4,NULL,'Recortes de costilla',2),(140,4,NULL,'Paleta de cordero',7.5),(141,4,NULL,'Paleta deshuesada',3),(142,4,NULL,'Pulpa de paleta',2),(143,4,NULL,'Bistec de paleta',2),(144,4,NULL,'Recortes de paleta',3),(145,4,NULL,'Pecho de cordero',3),(146,4,NULL,'Falda de cordero',3),(147,4,NULL,'Costilla falda',2),(148,4,NULL,'Recortes de falda',1),(149,4,NULL,'Cuello de cordero',2),(150,4,NULL,'Rodajas de cuello',1),(151,4,NULL,'Cabeza de cordero',1),(152,4,NULL,'Lengua de cordero',0.5),(153,4,NULL,'Sesos',0.3),(154,4,NULL,'Corazón',0.5),(155,4,NULL,'Hígado',1),(156,4,NULL,'Riñones',0.5),(157,4,NULL,'Patas de cordero',1),(158,4,NULL,'Rabo',0.2),(159,4,NULL,'Grasa dorsal',1),(160,4,NULL,'Grasa interna',0.5),(161,4,NULL,'Sebo',0.5),(162,4,NULL,'Huesos para caldo',2),(163,4,NULL,'Carne molida de cordero',1);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lote`
--

LOCK TABLES `lote` WRITE;
/*!40000 ALTER TABLE `lote` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materia_prima`
--

LOCK TABLES `materia_prima` WRITE;
/*!40000 ALTER TABLE `materia_prima` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materia_proveida`
--

LOCK TABLES `materia_proveida` WRITE;
/*!40000 ALTER TABLE `materia_proveida` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orden_compra`
--

LOCK TABLES `orden_compra` WRITE;
/*!40000 ALTER TABLE `orden_compra` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona`
--

LOCK TABLES `persona` WRITE;
/*!40000 ALTER TABLE `persona` DISABLE KEYS */;
INSERT INTO `persona` VALUES (1,'admin','admin','admin','9999999999','León, Gto',1),(2,'Emiliano','Mendoza','Maldonado','4779189172','León, Gto',2),(3,'Emmanuel','Ortiz','Reyes','4773845271','León, Gto',3);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedor`
--

LOCK TABLES `proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta`
--

LOCK TABLES `receta` WRITE;
/*!40000 ALTER TABLE `receta` DISABLE KEYS */;
/*!40000 ALTER TABLE `receta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receta_corte`
--

DROP TABLE IF EXISTS `receta_corte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receta_corte` (
  `idRecetaCorte` int NOT NULL AUTO_INCREMENT,
  `idCorte` int NOT NULL,
  `nombreReceta` varchar(100) NOT NULL,
  `descripcion` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`idRecetaCorte`),
  UNIQUE KEY `idCorte` (`idCorte`),
  UNIQUE KEY `nombreReceta` (`nombreReceta`),
  CONSTRAINT `receta_corte_ibfk_1` FOREIGN KEY (`idCorte`) REFERENCES `corte` (`idCorte`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta_corte`
--

LOCK TABLES `receta_corte` WRITE;
/*!40000 ALTER TABLE `receta_corte` DISABLE KEYS */;
/*!40000 ALTER TABLE `receta_corte` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receta_corte_materia_prima`
--

DROP TABLE IF EXISTS `receta_corte_materia_prima`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receta_corte_materia_prima` (
  `idRecetaCorteMateriaPrima` int NOT NULL AUTO_INCREMENT,
  `idRecetaCorte` int NOT NULL,
  `idMateriaPrima` int NOT NULL,
  `cantidadUsada` float NOT NULL,
  PRIMARY KEY (`idRecetaCorteMateriaPrima`),
  KEY `idRecetaCorte` (`idRecetaCorte`),
  KEY `idMateriaPrima` (`idMateriaPrima`),
  CONSTRAINT `receta_corte_materia_prima_ibfk_1` FOREIGN KEY (`idRecetaCorte`) REFERENCES `receta_corte` (`idRecetaCorte`),
  CONSTRAINT `receta_corte_materia_prima_ibfk_2` FOREIGN KEY (`idMateriaPrima`) REFERENCES `materia_prima` (`idMateriaPrima`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta_corte_materia_prima`
--

LOCK TABLES `receta_corte_materia_prima` WRITE;
/*!40000 ALTER TABLE `receta_corte_materia_prima` DISABLE KEYS */;
/*!40000 ALTER TABLE `receta_corte_materia_prima` ENABLE KEYS */;
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
  `idMateriaPrima` int NOT NULL,
  `cantidadUsada` float NOT NULL,
  PRIMARY KEY (`idRecetaMateriaPrima`),
  KEY `idReceta` (`idReceta`),
  KEY `idMateriaPrima` (`idMateriaPrima`),
  CONSTRAINT `receta_materia_prima_ibfk_1` FOREIGN KEY (`idReceta`) REFERENCES `receta` (`idReceta`),
  CONSTRAINT `receta_materia_prima_ibfk_2` FOREIGN KEY (`idMateriaPrima`) REFERENCES `materia_prima` (`idMateriaPrima`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta_materia_prima`
--

LOCK TABLES `receta_materia_prima` WRITE;
/*!40000 ALTER TABLE `receta_materia_prima` DISABLE KEYS */;
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
  `idRecetaCorte` int DEFAULT NULL,
  `cantidadProducir` int NOT NULL,
  `fechaSolicitud` datetime NOT NULL,
  `fechaCompletada` datetime DEFAULT NULL,
  `estatus` varchar(20) NOT NULL,
  `idUsuario` int DEFAULT NULL,
  `notas` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`idSolicitud`),
  KEY `idReceta` (`idReceta`),
  KEY `idRecetaCorte` (`idRecetaCorte`),
  KEY `idUsuario` (`idUsuario`),
  CONSTRAINT `solicitud_produccion_ibfk_1` FOREIGN KEY (`idReceta`) REFERENCES `receta` (`idReceta`),
  CONSTRAINT `solicitud_produccion_ibfk_2` FOREIGN KEY (`idRecetaCorte`) REFERENCES `receta_corte` (`idRecetaCorte`),
  CONSTRAINT `solicitud_produccion_ibfk_3` FOREIGN KEY (`idUsuario`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitud_produccion`
--

LOCK TABLES `solicitud_produccion` WRITE;
/*!40000 ALTER TABLE `solicitud_produccion` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitud_produccion_detalle`
--

LOCK TABLES `solicitud_produccion_detalle` WRITE;
/*!40000 ALTER TABLE `solicitud_produccion_detalle` DISABLE KEYS */;
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
INSERT INTO `user` VALUES (1,'admin','admin@example.com','$pbkdf2-sha512$25000$hFDK2Vtrzfnf./9/732vFQ$5FcO1Z9K9gQXb6k.h1yMnx7xECwr4F6gjwPJhSD6zYRLeiw7fwZCEdUmp03qL/egpzhLVFboFY3zE9F1TB1M5Q','35c8fa13c2544e62bceb28c02ae83dc3',1,NULL,0,NULL,'2026-04-09 14:55:09','127.0.0.1','5996543c-037e-4432-a743-d6b1718e9a77','2026-04-16 15:03:21'),(2,'emiliano','emiliano@example.com','$pbkdf2-sha512$25000$hFDK2Vtrzfnf./9/732vFQ$5FcO1Z9K9gQXb6k.h1yMnx7xECwr4F6gjwPJhSD6zYRLeiw7fwZCEdUmp03qL/egpzhLVFboFY3zE9F1TB1M5Q','2ab9377076d94f71abcd0682071bb7bd',1,NULL,0,NULL,NULL,NULL,NULL,NULL),(3,'Emmanuel','emmanuel@example.com','$pbkdf2-sha512$25000$hFDK2Vtrzfnf./9/732vFQ$5FcO1Z9K9gQXb6k.h1yMnx7xECwr4F6gjwPJhSD6zYRLeiw7fwZCEdUmp03qL/egpzhLVFboFY3zE9F1TB1M5Q','3366c0e180434648b1fd603f2a4e6a37',1,NULL,0,NULL,NULL,NULL,NULL,NULL);
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
INSERT INTO `users_roles` VALUES (1,1),(2,1),(3,1);
/*!40000 ALTER TABLE `users_roles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-09 15:03:20
