-- creates a stored procedure ComputeAverageWeightedScoreForUser 
-- that computes and store the average weighted score for all students

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    ALTER TABLE users
    ADD total_weight INT NOT NULL;

    ALTER TABLE users
    ADD total_weighted_score INT NOT NULL;

    UPDATE users
    SET total_weight = (
        SELECT SUM(p.weight)
        FROM corrections c
        INNER JOIN projects p
        ON c.project_id = p.id
        WHERE c.user_id = users.id
    );

    UPDATE users
    SET total_weighted_score = (
        SELECT SUM(c.score * p.weight)
        FROM corrections c
        INNER JOIN projects p
        ON c.project_id = p.id
        WHERE c.user_id = users.id
    );

    UPDATE users
    SET average_score = IF(total_weight = 0, 0, total_weighted_score / total_weight);

    ALTER TABLE users
    DROP COLUMN total_weight;

    ALTER TABLE users
    DROP COLUMN total_weighted_score;
END;
//
DELIMITER ;
