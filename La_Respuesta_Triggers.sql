
INSERT INTO categoria (nombreCategoria) VALUES("Res"),("Pollo"),("Cerdo"),("Borrego"),("Otro");


DELIMITER $$

-- ─────────────────────────────────────────────────────────────
--  TRIGGER: actualizar_stock_after_insert
--  Dispara cuando se inserta una nueva unidad en producto_unitario
-- ─────────────────────────────────────────────────────────────
CREATE TRIGGER actualizar_stock_after_insert
AFTER INSERT ON producto_unitario
FOR EACH ROW
BEGIN
    UPDATE producto
    SET StockProducto = (
        SELECT COUNT(*)
        FROM producto_unitario
        WHERE idProducto = NEW.idProducto
          AND estatus = 'Disponible'
    )
    WHERE idProducto = NEW.idProducto;
END$$


-- ─────────────────────────────────────────────────────────────
--  TRIGGER: actualizar_stock_after_update
--  Dispara cuando se actualiza una unidad (cambio de estatus,
--  reasignación de producto, etc.)
-- ─────────────────────────────────────────────────────────────
CREATE TRIGGER actualizar_stock_after_update
AFTER UPDATE ON producto_unitario
FOR EACH ROW
BEGIN
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
END$$


-- Conversores
INSERT INTO conversor (idConversor, nombreConversor) VALUES
  (1, 'Kilogramos'),
  (2, 'Piezas'),
  (3, 'Litros');

-- Unidades de medida
INSERT INTO unidad_medida (nombreUnidadMedida, idConversor) VALUES
  ('Canal entera', 1),   
  ('Media canal',1),  
  ('Kilogramo',1),   
  ('Tonelada',1),   
  ('Paquete',1),  
  ('Bolsa',1),   
  ('Bulto',1),   
  ('Pieza',2),  
  ('Caja',2),   
  ('Litro',3);  


INSERT INTO Categoria (nombreCategoria) VALUES ('RES'), ('CERDO'), ('POLLO'), ('BORREGO'), ('OTRO');
