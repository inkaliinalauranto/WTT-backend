-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `db` DEFAULT CHARACTER SET utf8 ;
USE `db` ;

-- -----------------------------------------------------
-- Table `db`.`organizations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db`.`organizations` (
  `organization_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`organization_id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`auth_roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db`.`auth_roles` (
  `role_id` INT NOT NULL AUTO_INCREMENT,
  `role_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE INDEX `role_name_UNIQUE` (`role_name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db`.`users` (
  `username` VARCHAR(16) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(32) NOT NULL,
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `organization_id` INT NOT NULL,
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `deleted_at` TIMESTAMP NULL,
  `access_jtl` VARCHAR(45) NOT NULL,
  `role_id` INT NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  INDEX `fk_user_organization_idx` (`organization_id` ASC),
  PRIMARY KEY (`user_id`),
  INDEX `fk_users_auth_roles1_idx` (`role_id` ASC),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  CONSTRAINT `fk_user_organization`
    FOREIGN KEY (`organization_id`)
    REFERENCES `db`.`organizations` (`organization_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_auth_roles1`
    FOREIGN KEY (`role_id`)
    REFERENCES `db`.`auth_roles` (`role_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `db`.`shift_types`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db`.`shift_types` (
  `shift_type_id` INT NOT NULL,
  `type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`shift_type_id`),
  UNIQUE INDEX `type_UNIQUE` (`type` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`shift_statuses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db`.`shift_statuses` (
  `status_id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`status_id`),
  UNIQUE INDEX `type_UNIQUE` (`type` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`shifts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db`.`shifts` (
  `shift_id` INT NOT NULL AUTO_INCREMENT,
  `start_time` TIMESTAMP NOT NULL,
  `end_time` TIMESTAMP NULL,
  `user_id` INT NOT NULL,
  `shift_type_id` INT NOT NULL,
  `shift_status_id` INT NOT NULL,
  `description` VARCHAR(255) NULL,
  PRIMARY KEY (`shift_id`),
  INDEX `fk_shifts_users1_idx` (`user_id` ASC),
  INDEX `fk_shifts_shift_types1_idx` (`shift_type_id` ASC),
  INDEX `fk_shifts_shift_statuses1_idx` (`shift_status_id` ASC),
  CONSTRAINT `fk_shifts_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `db`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_shifts_shift_types1`
    FOREIGN KEY (`shift_type_id`)
    REFERENCES `db`.`shift_types` (`shift_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_shifts_shift_statuses1`
    FOREIGN KEY (`shift_status_id`)
    REFERENCES `db`.`shift_statuses` (`status_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`breaks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db`.`breaks` (
  `break_id` INT NOT NULL AUTO_INCREMENT,
  `start_time` TIMESTAMP NULL,
  `end_time` TIMESTAMP NULL,
  `description` VARCHAR(255) NULL,
  `shift_id` INT NOT NULL,
  PRIMARY KEY (`break_id`),
  INDEX `fk_breaks_shifts1_idx` (`shift_id` ASC),
  CONSTRAINT `fk_breaks_shifts1`
    FOREIGN KEY (`shift_id`)
    REFERENCES `db`.`shifts` (`shift_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`notifications`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db`.`notifications` (
  `notification_id` INT NOT NULL AUTO_INCREMENT,
  `message` VARCHAR(255) NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`notification_id`),
  INDEX `fk_notifications_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_notifications_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `db`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `db`.`test`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db`.`test` (
  `id` INT NOT NULL,
  `name` VARCHAR(255) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`user_relationships`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db`.`user_relationships` (
  `relationship_id` INT NOT NULL AUTO_INCREMENT,
  `manager_id` INT NOT NULL,
  `worker_id` INT NOT NULL,
  `relationship_type` ENUM('MANAGER', 'VIEWER') NOT NULL,
  PRIMARY KEY (`relationship_id`),
  INDEX `fk_user_relationships_users1_idx` (`manager_id` ASC),
  INDEX `fk_user_relationships_users2_idx` (`worker_id` ASC),
  UNIQUE INDEX `unique_manager_worker_idx` (`manager_id` ASC, `worker_id` ASC),
  CONSTRAINT `fk_user_relationships_users1`
    FOREIGN KEY (`manager_id`)
    REFERENCES `db`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_relationships_users2`
    FOREIGN KEY (`worker_id`)
    REFERENCES `db`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
