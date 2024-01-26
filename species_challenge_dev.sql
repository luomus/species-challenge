-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Jan 26, 2024 at 11:28 PM
-- Server version: 10.5.23-MariaDB-1:10.5.23+maria~ubu2004
-- PHP Version: 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `species_challenge_dev`
--

-- --------------------------------------------------------

--
-- Table structure for table `challenges`
--

CREATE TABLE `challenges` (
  `id` char(36) NOT NULL,
  `taxon` varchar(16) NOT NULL,
  `year` int(11) NOT NULL,
  `type` varchar(16) NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` varchar(8) NOT NULL,
  `meta_created_by` varchar(16) NOT NULL,
  `meta_created_at` datetime NOT NULL,
  `meta_edited_by` varchar(16) NOT NULL,
  `meta_edited_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `challenges`
--

INSERT INTO `challenges` (`id`, `taxon`, `year`, `type`, `name`, `status`, `meta_created_by`, `meta_created_at`, `meta_edited_by`, `meta_edited_at`) VALUES
('a04c7b03-bc6f-11ee-837a-0242c0a8a002', 'MX.37613', 2024, 'challenge100', 'Hyönteiset: 100 lajia -haaste 2024', 'open', 'MA.3', '2024-01-26 18:26:33', 'MA.3', '2024-01-26 18:26:33'),
('a04c89f9-bc6f-11ee-837a-0242c0a8a002', 'MX.53078', 2024, 'challenge100', 'Putkilokasvit: 100 lajia -haaste 2024', 'open', 'MA.3', '2024-01-26 18:26:33', 'MA.3', '2024-01-26 18:26:33'),
('f07a828f-bc6f-11ee-837a-0242c0a8a002', 'MX.53062', 2024, 'challenge100', 'Sienet: 100 lajia -haaste 2024', 'open', 'MA.3', '2024-01-26 18:34:43', 'MA.3', '2024-01-26 18:34:43'),
('f07a8c5a-bc6f-11ee-837a-0242c0a8a002', 'MX.53062', 2023, 'challenge100', 'Sienet: 100 lajia -haaste 2023', 'closed', 'MA.3', '2024-01-26 18:34:43', 'MA.3', '2024-01-26 18:34:43');

-- --------------------------------------------------------

--
-- Table structure for table `participations`
--

CREATE TABLE `participations` (
  `id` char(36) NOT NULL,
  `challenge_id` char(36) DEFAULT NULL,
  `participant_name` varchar(128) NOT NULL,
  `location` varchar(128) DEFAULT NULL,
  `taxa_count` int(11) DEFAULT NULL,
  `taxa_json` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`taxa_json`)),
  `meta_created_by` varchar(16) NOT NULL,
  `meta_created_at` datetime NOT NULL,
  `meta_edited_by` varchar(16) NOT NULL,
  `meta_edited_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `challenges`
--
ALTER TABLE `challenges`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `participations`
--
ALTER TABLE `participations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `challenge_id` (`challenge_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `participations`
--
ALTER TABLE `participations`
  ADD CONSTRAINT `participations_ibfk_1` FOREIGN KEY (`challenge_id`) REFERENCES `challenges` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
