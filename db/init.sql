CREATE SCHEMA cv_builder;
USE cv_builder;

CREATE TABLE `Students` (
  `Student_id` int UNIQUE PRIMARY KEY NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Phone` varchar(255) UNIQUE NOT NULL,
  `Email` varchar(255) UNIQUE NOT NULL,
  `DOB` date,
  `Branch` varchar(255),
  `Minor` varchar(255),
  `Year` int
);

CREATE TABLE `Credentials` (
  `Student_id` int UNIQUE PRIMARY KEY NOT NULL,
  `Password_hash` varchar(255) NOT NULL
);

CREATE TABLE `User_Tokens` (
  `Session_hash` varchar(255) UNIQUE PRIMARY KEY NOT NULL,
  `Student_id` int NOT NULL,
  `CreatedAt` datetime NOT NULL
);

CREATE TABLE `Professors` (
  `Professor_id` int UNIQUE PRIMARY KEY NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Department` varchar(255),
  `Email` varchar(255) UNIQUE NOT NULL,
  `Phone` varchar(255) UNIQUE NOT NULL
);

CREATE TABLE `Projects` (
  `Project_id` int UNIQUE PRIMARY KEY NOT NULL,
  `Title` varchar(255) NOT NULL,
  `Description` varchar(255),
  `Start_date` date,
  `End_date` date
);

CREATE TABLE `Tenth` (
  `Student_id` int UNIQUE PRIMARY KEY NOT NULL,
  `School_name` varchar(255),
  `CGPA` double NOT NULL,
  `Board` varchar(255),
  `Year` int
);

CREATE TABLE `Twelfth` (
  `Student_id` int UNIQUE PRIMARY KEY NOT NULL,
  `School_name` varchar(255),
  `CGPA` double NOT NULL,
  `Board` varchar(255),
  `Year` int
);

CREATE TABLE `References` (
  `Student_id` int NOT NULL,
  `Professor_id` int NOT NULL,
  PRIMARY KEY (`Student_id`, `Professor_id`)
);

CREATE TABLE `Project_relations` (
  `Project_id` int NOT NULL,
  `Student_id` int NOT NULL,
  `Professor_id` int NOT NULL,
  PRIMARY KEY (`Project_id`, `Student_id`, `Professor_id`)
);

CREATE TABLE `SGPA` (
  `Student_id` int NOT NULL,
  `Semester` int NOT NULL,
  `SGPA` float,
  PRIMARY KEY (`Student_id`, `Semester`)
);

CREATE TABLE `Internships` (
  `Student_id` int NOT NULL,
  `Start_date` date NOT NULL,
  `End_date` date NOT NULL,
  `Organization` varchar(255),
  `Designation` varchar(255),
  `Description` varchar(255),
  PRIMARY KEY (`Student_id`, `Start_date`, `End_date`)
);

CREATE TABLE `Extra_Curriculars` (
  `Student_id` int NOT NULL,
  `Title` varchar(255) NOT NULL,
  `Start_date` date NOT NULL,
  `End_date` date NOT NULL,
  `Description` varchar(255),
  PRIMARY KEY (`Student_id`, `Title`, `Start_date`, `End_date`)
);

CREATE TABLE `Skills` (
  `Student_id` int NOT NULL,
  `Skill` varchar(255) NOT NULL,
  PRIMARY KEY (`Student_id`, `Skill`)
);

CREATE TABLE `Languages` (
  `Student_id` int NOT NULL,
  `Language` varchar(255) NOT NULL,
  `Writing` boolean,
  `Reading` boolean,
  `Speaking` boolean,
  PRIMARY KEY (`Student_id`, `Language`)
);

CREATE TABLE `Achievements` (
  `Student_id` int NOT NULL,
  `Achievement` varchar(255) NOT NULL,
  PRIMARY KEY (`Student_id`, `Achievement`)
);

ALTER TABLE `Credentials` ADD FOREIGN KEY (`Student_id`) REFERENCES `Students` (`Student_id`);

ALTER TABLE `User_Tokens` ADD FOREIGN KEY (`Student_id`) REFERENCES `Students` (`Student_id`);

ALTER TABLE `Tenth` ADD FOREIGN KEY (`Student_id`) REFERENCES `Students` (`Student_id`);

ALTER TABLE `Twelfth` ADD FOREIGN KEY (`Student_id`) REFERENCES `Students` (`Student_id`);

ALTER TABLE `References` ADD FOREIGN KEY (`Student_id`) REFERENCES `Students` (`Student_id`);

ALTER TABLE `References` ADD FOREIGN KEY (`Professor_id`) REFERENCES `Professors` (`Professor_id`);

ALTER TABLE `Project_relations` ADD FOREIGN KEY (`Student_id`) REFERENCES `Students` (`Student_id`);

ALTER TABLE `Project_relations` ADD FOREIGN KEY (`Professor_id`) REFERENCES `Professors` (`Professor_id`);

ALTER TABLE `Project_relations` ADD FOREIGN KEY (`Project_id`) REFERENCES `Projects` (`Project_id`);

ALTER TABLE `SGPA` ADD FOREIGN KEY (`Student_id`) REFERENCES `Students` (`Student_id`);

ALTER TABLE `Internships` ADD FOREIGN KEY (`Student_id`) REFERENCES `Students` (`Student_id`);

ALTER TABLE `Extra_Curriculars` ADD FOREIGN KEY (`Student_id`) REFERENCES `Students` (`Student_id`);

ALTER TABLE `Skills` ADD FOREIGN KEY (`Student_id`) REFERENCES `Students` (`Student_id`);

ALTER TABLE `Languages` ADD FOREIGN KEY (`Student_id`) REFERENCES `Students` (`Student_id`);

ALTER TABLE `Achievements` ADD FOREIGN KEY (`Student_id`) REFERENCES `Students` (`Student_id`);

INSERT INTO `cv_builder`.`Students` (`Student_id`, `Name`, `Phone`, `Email`) VALUES (123, 'Noob', 123, 'Test');
INSERT INTO `cv_builder`.`Credentials` (`Student_id`, `Password_hash`) VALUES ('123', '5f575b82b27b73ffaa9038c2d0931f2eca6a7c3e7d278fae0647e3b1fe23acd49689492db19282ee88694547a85a965a8581fc39a1f2a05d819be615938c5e8cc9b5ad40af6a1a87f9d65d9e22300f6db0397af6bdf8c6e6685990f31feae4a7');
