-- Creates a trigger to reset valid_email when the email has been changed

DELIMITER $$
CREATE TRIGGER reset_email_validation BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email != OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END;
DELIMITER ;