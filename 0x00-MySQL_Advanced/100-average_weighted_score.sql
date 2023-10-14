-- creates a stored procedure ComputeAverageWeightedScoreForUser 
-- that computes and store the average weighted score for a student

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE total_weight INT DEFAULT 0;
    DECLARE total_weighted_score INT DEFAULT 0;

    SELECT SUM(p.weight)
    INTO total_weight
    FROM corrections c
    INNER JOIN projects p
    ON c.project_id = p.id
    WHERE c.user_id = user_id;

    SELECT SUM(c.score * p.weight)
    INTO total_weighted_score
    FROM corrections c
    INNER JOIN projects p
    ON c.project_id = p.id
    WHERE c.user_id = user_id;

    UPDATE users
    SET users.average_score = IF(total_weight = 0, 0, total_weighted_score / total_weight);

END;
//
DELIMITER ;
