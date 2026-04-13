
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


-- Procedure para crear un pedido en una venta de mostrador
DELIMITER $$

CREATE PROCEDURE crear_pedido_mostrador(
    IN p_idUsuario INT,
    IN p_tipo VARCHAR(50)
)
BEGIN
    INSERT INTO pedido (
        idUsuario,
        Total,
        Tipo,
        Estatus,
        Entrega,
        Direccion,
        Notas,
        fechaCreacion
    )
    VALUES (
        p_idUsuario,
        0, -- inicia en 0, luego puedes actualizarlo
        p_tipo,
        'Finalizado',
        'Mostrador',
        '',
        'Venta generada en sucursal',
        NOW()
    );

    -- Retornar el ID generado
    SELECT LAST_INSERT_ID() AS idPedido;
END$$

DELIMITER ;



-- Procedure para asignar productos unitarios a un pedido y actualizar su estatus
DELIMITER $$

CREATE PROCEDURE asignar_productos_a_pedido(
    IN p_idPedido INT,
    IN p_idProducto INT,
    IN p_cantidad INT
)
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE v_idProductoUnitario INT;

    -- Cursor para obtener productos disponibles ordenados por caducidad
    DECLARE cur_productos CURSOR FOR
        SELECT idProductoUnitario
        FROM producto_unitario
        WHERE idProducto = p_idProducto
          AND estatus = 'Disponible'
        ORDER BY FechaCaducidad ASC;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur_productos;

    read_loop: LOOP
        FETCH cur_productos INTO v_idProductoUnitario;

        IF done = 1 OR p_cantidad <= 0 THEN
            LEAVE read_loop;
        END IF;

        -- Actualizar el producto unitario
        UPDATE producto_unitario
        SET idPedido = p_idPedido,
            estatus = 'Vendido'
        WHERE idProductoUnitario = v_idProductoUnitario;

        -- Reducir contador
        SET p_cantidad = p_cantidad - 1;

    END LOOP;

    CLOSE cur_productos;

END$$

DELIMITER ;