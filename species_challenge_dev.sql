-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Jan 29, 2024 at 02:24 PM
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
  `challenge_id` int(11) NOT NULL,
  `taxon` varchar(16) NOT NULL,
  `year` int(11) DEFAULT NULL,
  `type` varchar(16) NOT NULL,
  `title` varchar(255) NOT NULL,
  `status` varchar(8) NOT NULL,
  `description` varchar(2048) DEFAULT NULL,
  `meta_created_by` varchar(16) NOT NULL,
  `meta_created_at` datetime NOT NULL,
  `meta_edited_by` varchar(16) NOT NULL,
  `meta_edited_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `challenges`
--

INSERT INTO `challenges` (`challenge_id`, `taxon`, `year`, `type`, `title`, `status`, `description`, `meta_created_by`, `meta_created_at`, `meta_edited_by`, `meta_edited_at`) VALUES
(1, 'MX.37613', 2024, 'challenge100', 'Hyönteiset 2024', 'draft', NULL, 'MA.3', '2024-01-28 10:39:59', 'MA.3', '2024-01-28 10:39:59'),
(2, 'MX.53062', 2024, 'challenge100', 'Sienet 2024', 'closed', NULL, 'MA.3', '2024-01-28 10:39:59', 'MA.3', '2024-01-28 10:39:59'),
(3, 'MX.53062', 2023, 'challenge100', 'Sienet 2023', 'closed', NULL, 'MA.3', '2024-01-28 10:41:49', 'MA.3', '2024-01-28 10:41:49'),
(4, 'MX.53078', 2024, 'challenge100', 'Putkilokasvit 2024', 'open', NULL, 'MA.3', '2024-01-28 10:42:23', 'MA.3', '2024-01-28 10:42:23'),
(5, 'sdf', 2024, 'dsf', 'sdf', 'sfd', NULL, 'MA.3', '2024-01-28 22:32:58', 'MA.3', '2024-01-28 22:32:58'),
(6, 'MX.53078', 2024, 'challenge-k', '1000 Lajia -haaste', 'open', NULL, 'MA.3', '2024-01-28 22:33:44', 'MA.3', '2024-01-29 13:27:40');

-- --------------------------------------------------------

--
-- Table structure for table `participations`
--

CREATE TABLE `participations` (
  `participation_id` int(11) NOT NULL,
  `challenge_id` int(11) NOT NULL,
  `name` varchar(128) NOT NULL,
  `place` varchar(128) DEFAULT NULL,
  `taxa_count` int(11) DEFAULT NULL,
  `taxa_json` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`taxa_json`)),
  `meta_created_by` varchar(16) NOT NULL,
  `meta_created_at` datetime NOT NULL,
  `meta_edited_by` varchar(16) NOT NULL,
  `meta_edited_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `participations`
--

INSERT INTO `participations` (`participation_id`, `challenge_id`, `name`, `place`, `taxa_count`, `taxa_json`, `meta_created_by`, `meta_created_at`, `meta_edited_by`, `meta_edited_at`) VALUES
(1, 2, 'Testaaja 2', 'Helsinki 2', NULL, NULL, 'MA.3', '2024-01-28 10:47:46', 'MA.3', '2024-01-28 13:47:59'),
(2, 2, 'Teppo Testaaja', 'Vantaa', NULL, NULL, 'MA.3', '2024-01-28 10:51:00', 'MA.3', '2024-01-28 10:51:03'),
(3, 2, 'Ulla Uusmäki-Vanhalaakso', 'Outokumpu, kummun takana', NULL, NULL, 'MA.3', '2024-01-28 13:53:50', 'MA.3', '2024-01-28 13:54:36'),
(4, 2, 'Untamo Ikämies-Akana', 'Akaa-Loimaa', NULL, NULL, 'MA.3', '2024-01-28 13:54:52', 'MA.3', '2024-01-28 15:18:24'),
(5, 4, 'Nimi Merkkinen', 'Nimismiehenkylä', NULL, NULL, 'MA.3', '2024-01-28 15:19:17', 'MA.3', '2024-01-28 15:19:17'),
(6, 4, 'André D\'Artágnan', 'Ääkkölä ääkkölärules', 4, '{\"MX.37691\": \"2024-01-11\", \"MX.37721\": \"2024-01-02\", \"MX.37717\": \"2024-01-27\", \"MX.37719\": \"2024-01-28\"}', 'MA.3', '2024-01-28 15:29:01', 'MA.3', '2024-01-28 20:47:11');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `challenges`
--
ALTER TABLE `challenges`
  ADD PRIMARY KEY (`challenge_id`);

--
-- Indexes for table `participations`
--
ALTER TABLE `participations`
  ADD PRIMARY KEY (`participation_id`),
  ADD KEY `challenge_id` (`challenge_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `challenges`
--
ALTER TABLE `challenges`
  MODIFY `challenge_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `participations`
--
ALTER TABLE `participations`
  MODIFY `participation_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `participations`
--
ALTER TABLE `participations`
  ADD CONSTRAINT `participations_ibfk_1` FOREIGN KEY (`challenge_id`) REFERENCES `challenges` (`challenge_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
