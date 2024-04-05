CREATE TABLE `students` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Primary key id',
    `name` varchar(64) NOT NULL DEFAULT '' COMMENT 'Name',
    `english` decimal(6, 2) NOT NULL DEFAULT '0.00' COMMENT 'English grade',
    `math` decimal(6, 2) NOT NULL DEFAULT '0.00' COMMENT 'Math grade',
    `chinese` decimal(6, 2) NOT NULL DEFAULT '0.00' COMMENT 'Chinese grade',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHAR SET = utf8 COMMENT = 'Student Table';

CREATE TABLE `teachers` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'Primary key id',
    `name` varchar(64) NOT NULL DEFAULT '' COMMENT 'name',
    `password` varchar(64) NOT NULL DEFAULT '' COMMENT 'password',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHAR SET = utf8 COMMENT = 'Teacher Table';