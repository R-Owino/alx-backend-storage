-- Create a trigger that decreases item quantity after adding a new order

DROP TRIGGER IF EXISTS decrease_item_quantity_after_order;

DELIMITER //
CREATE TRIGGER decrease_item_quantity_after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Decrease the quantity in the items table
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;
//
DELIMITER ;
