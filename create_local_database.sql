-- Tee wtt-niminen tietokanta paikallisessa phpMyAdminissa,
-- valitse luotu tietokanta ja suorita SQL-välilehdellä seuraava
-- kysely:

-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema wtt
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema wtt
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `wtt` DEFAULT CHARACTER SET utf8 ;
USE `wtt` ;

-- -----------------------------------------------------
-- Table `wtt`.`roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wtt`.`roles` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `role_name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `wtt`.`organizations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wtt`.`organizations` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `wtt`.`teams`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wtt`.`teams` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `organization_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC),
  INDEX `fk_team_organizations1_idx` (`organization_id` ASC),
  CONSTRAINT `fk_team_organizations1`
    FOREIGN KEY (`organization_id`)
    REFERENCES `wtt`.`organizations` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `wtt`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wtt`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `access_jti` VARCHAR(512) NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted_at` TIMESTAMP NULL,
  `role_id` INT NOT NULL,
  `team_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_users_auth_roles1_idx` (`role_id` ASC),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  INDEX `fk_users_team1_idx` (`team_id` ASC),
  CONSTRAINT `fk_users_auth_roles1`
    FOREIGN KEY (`role_id`)
    REFERENCES `wtt`.`roles` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_users_team1`
    FOREIGN KEY (`team_id`)
    REFERENCES `wtt`.`teams` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `wtt`.`shift_types`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wtt`.`shift_types` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `type_UNIQUE` (`type` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `wtt`.`shifts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wtt`.`shifts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `start_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `end_time` TIMESTAMP NULL,
  `user_id` INT NOT NULL,
  `shift_type_id` INT NOT NULL,
  `description` VARCHAR(255) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_shifts_users1_idx` (`user_id` ASC),
  INDEX `fk_shifts_shift_types1_idx` (`shift_type_id` ASC),
  CONSTRAINT `fk_shifts_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `wtt`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_shifts_shift_types1`
    FOREIGN KEY (`shift_type_id`)
    REFERENCES `wtt`.`shift_types` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
