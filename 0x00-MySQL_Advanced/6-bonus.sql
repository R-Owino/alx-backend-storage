-- Creates a stored procedure that adds a new correction for a student

DROP PROCEDURE IF EXISTS AddBonus;

DELIMITER //
CREATE PROCEDURE AddBonus(
    IN p_user_id INT,
    IN p_project_name VARCHAR(255),
    IN p_score INT
)
BEGIN
    DECLARE v_project_id INT;

    -- Check if the project already exists; if not, create it
    SELECT id INTO v_project_id
    FROM projects
    WHERE name = p_project_name;

    IF v_project_id IS NULL THEN
        -- Project doesn't exist, so create a new one
        INSERT INTO projects (name) VALUES (p_project_name);
        SET v_project_id = LAST_INSERT_ID();
    END IF;

    -- Add the correction for the student
    INSERT INTO corrections (user_id, project_id, score) VALUES (p_user_id, v_project_id, p_score);
END;
//
DELIMITER ;
