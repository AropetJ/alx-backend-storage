-- An SQL script that creates a stored procedure AddBonus
-- that adds a new correction for a student.
DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER $$
CREATE PROCEDURE AddBonus (user_id INT, project_name VARCHAR(255), score FLOAT)
BEGIN
    DECLARE count INT DEFAULT 0;
    DECLARE student_id INT DEFAULT 0;

    SELECT COUNT(id)
        INTO count
        FROM projects
        WHERE name = project_name;
    IF count = 0 THEN
        INSERT INTO projects(name)
            VALUES(project_name);
    END IF;
    SELECT id
        INTO student_id
        FROM projects
        WHERE name = project_name;
    INSERT INTO corrections(user_id, student_id, score)
        VALUES (user_id, student_id, score);
END $$
DELIMITER ;
