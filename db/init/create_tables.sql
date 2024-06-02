CREATE TABLE `ai_analysis_log` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `image_path` varchar(255) DEFAULT NULL,
    `success` tinyint(1) NOT NULL,
    `message` varchar(255) DEFAULT NULL,
    `class` int(11) DEFAULT NULL,
    `confidence` decimal(5, 4) DEFAULT NULL,
    `request_timestamp` datetime(6) DEFAULT NULL,
    `response_timestamp` datetime(6) DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;