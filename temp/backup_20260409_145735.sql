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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria`
--

LOCK TABLES `categoria` WRITE;
/*!40000 ALTER TABLE `categoria` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conversor`
--

LOCK TABLES `conversor` WRITE;
/*!40000 ALTER TABLE `conversor` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `corte`
--

LOCK TABLES `corte` WRITE;
/*!40000 ALTER TABLE `corte` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidad_medida`
--

LOCK TABLES `unidad_medida` WRITE;
/*!40000 ALTER TABLE `unidad_medida` DISABLE KEYS */;
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
INSERT INTO `user` VALUES (1,'admin','admin@example.com','$pbkdf2-sha512$25000$hFDK2Vtrzfnf./9/732vFQ$5FcO1Z9K9gQXb6k.h1yMnx7xECwr4F6gjwPJhSD6zYRLeiw7fwZCEdUmp03qL/egpzhLVFboFY3zE9F1TB1M5Q','35c8fa13c2544e62bceb28c02ae83dc3',1,NULL,0,NULL,'2026-04-09 14:55:09','127.0.0.1','5996543c-037e-4432-a743-d6b1718e9a77','2026-04-16 14:57:35'),(2,'emiliano','emiliano@example.com','$pbkdf2-sha512$25000$hFDK2Vtrzfnf./9/732vFQ$5FcO1Z9K9gQXb6k.h1yMnx7xECwr4F6gjwPJhSD6zYRLeiw7fwZCEdUmp03qL/egpzhLVFboFY3zE9F1TB1M5Q','2ab9377076d94f71abcd0682071bb7bd',1,NULL,0,NULL,NULL,NULL,NULL,NULL),(3,'Emmanuel','emmanuel@example.com','$pbkdf2-sha512$25000$hFDK2Vtrzfnf./9/732vFQ$5FcO1Z9K9gQXb6k.h1yMnx7xECwr4F6gjwPJhSD6zYRLeiw7fwZCEdUmp03qL/egpzhLVFboFY3zE9F1TB1M5Q','3366c0e180434648b1fd603f2a4e6a37',1,NULL,0,NULL,NULL,NULL,NULL,NULL);
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

-- Dump completed on 2026-04-09 14:57:35
