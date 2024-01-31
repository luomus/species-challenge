-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Jan 31, 2024 at 09:29 AM
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
(2, 'MX.53078', 2024, 'challenge100', 'Sienet 2024', 'closed', 'Kuka havaitsee vuoden aikana eniten lajeja omalla kotikunnassaan? Perinteinen kuntahaaste on avoin kilpailu kaikille alueen asukkaille.\r\n\r\nLiikkumistavaksi suositellaan ekovaihtoehtoja, mutta kaikki liikkumistavat ovat kuitenkin sallittuja. Lorem ipsum dolor sit amet. Liikkumistavaksi suositellaan ekovaihtoehtoja, mutta kaikki liikkumistavat ovat kuitenkin sallittuja. Lorem ipsum dolor sit amet.', 'MA.3', '2024-01-28 10:39:59', 'MA.3', '2024-01-29 21:37:00'),
(3, 'MX.53062', 2023, 'challenge100', 'Sienet 2023', 'closed', NULL, 'MA.3', '2024-01-28 10:41:49', 'MA.3', '2024-01-28 10:41:49'),
(4, 'MX.53078', 2024, 'challenge100', 'Putkilokasvit 2024 D', 'open', 'Foo bar', 'MA.3', '2024-01-28 10:42:23', 'MA.3', '2024-01-30 15:48:43'),
(5, 'MX.53078', 2024, 'challenge100', 'sdf', 'open', NULL, 'MA.3', '2024-01-28 22:32:58', 'MA.3', '2024-01-28 22:32:58'),
(6, 'MX.53078', 2024, 'challenge-k', '1000 Lajia -haaste', 'open', NULL, 'MA.3', '2024-01-28 22:33:44', 'MA.3', '2024-01-29 13:27:40'),
(7, 'MX.53078', 2000, 'challenge100', 'Testi', 'draft', 'Testi', 'MA.3', '2024-01-30 14:58:59', 'MA.3', '2024-01-30 14:58:59'),
(8, 'MX.53078', 2000, 'challenge100', 'Testi', 'draft', 'Testi', 'MA.3', '2024-01-30 14:59:56', 'MA.3', '2024-01-30 14:59:56'),
(9, 'MX.53078', 2000, 'challenge100', 'Testi', 'draft', 'Testi', 'MA.3', '2024-01-30 15:02:14', 'MA.3', '2024-01-30 15:02:14'),
(10, 'MX.53078', 2001, 'challenge100', 'simplified Chinese 汉语 traditional Chinese 漢語', 'draft', 'simplified Chinese: 汉语; traditional Chinese: 漢語;', 'MA.3', '2024-01-30 15:11:19', 'MA.3', '2024-01-30 15:14:52'),
(11, 'MX.53078', 2024, 'challenge100', 'Temp', 'draft', 'Temp', 'MA.3', '2024-01-30 15:49:13', 'MA.3', '2024-01-30 15:49:13');

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
  `meta_edited_at` datetime NOT NULL,
  `trashed` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `participations`
--

INSERT INTO `participations` (`participation_id`, `challenge_id`, `name`, `place`, `taxa_count`, `taxa_json`, `meta_created_by`, `meta_created_at`, `meta_edited_by`, `meta_edited_at`, `trashed`) VALUES
(1, 2, 'Testaaja 2', 'Helsinki 2', NULL, NULL, 'MA.3', '2024-01-28 10:47:46', 'MA.3', '2024-01-28 13:47:59', 0),
(2, 2, 'Teppo Testaaja', 'Vantaa', NULL, NULL, 'MA.3', '2024-01-28 10:51:00', 'MA.3', '2024-01-28 10:51:03', 0),
(3, 2, 'Ulla Uusmäki-Vanhalaakso', 'Outokumpu, kummun takana', NULL, NULL, 'MA.3', '2024-01-28 13:53:50', 'MA.3', '2024-01-28 13:54:36', 0),
(4, 2, 'Untamo Ikämies-Akana', 'Akaa-Loimaa', NULL, NULL, 'MA.3', '2024-01-28 13:54:52', 'MA.3', '2024-01-28 15:18:24', 0),
(5, 4, 'Nimi Merkkinen', 'Nimismiehenkylä', 28, '{\"MX.37691\": \"2024-01-30\", \"MX.37721\": \"2024-01-30\", \"MX.37717\": \"2024-01-17\", \"MX.37719\": \"2024-01-25\", \"MX.37763\": \"2024-01-01\", \"MX.37771\": \"2024-01-30\", \"MX.4994055\": \"2024-01-03\", \"MX.37752\": \"2024-01-30\", \"MX.37747\": \"2024-01-30\", \"MX.37826\": \"2024-01-30\", \"MX.37812\": \"2024-01-10\", \"MX.37819\": \"2024-01-30\", \"MX.40138\": \"2024-01-30\", \"MX.39201\": \"2024-01-30\", \"MX.39235\": \"2024-01-30\", \"MX.4973227\": \"2024-01-17\", \"MX.39887\": \"2024-01-30\", \"MX.39917\": \"2024-01-11\", \"MX.38279\": \"2024-01-02\", \"MX.38598\": \"2024-01-13\", \"MX.39052\": \"2024-01-20\", \"MX.39038\": \"2024-01-11\", \"MX.39465\": \"2024-01-18\", \"MX.39673\": \"2024-01-30\", \"MX.39967\": \"2024-01-30\", \"MX.38301\": \"2024-01-30\", \"MX.40632\": \"2024-01-11\", \"MX.38843\": \"2024-01-25\"}', 'MA.3', '2024-01-28 15:19:17', 'MA.3', '2024-01-31 08:51:51', 1),
(6, 4, 'André D\'Artágnan', 'Ääkkölä ääkkölärules', 13, '{\"MX.37691\": \"2024-01-11\", \"MX.37721\": \"2024-01-02\", \"MX.37717\": \"2024-01-27\", \"MX.37719\": \"2024-01-28\", \"MX.37763\": \"2024-01-10\", \"MX.37771\": \"2024-01-18\", \"MX.37752\": \"2024-01-30\", \"MX.40138\": \"2024-01-30\", \"MX.40150\": \"2024-01-30\", \"MX.39201\": \"2024-01-30\", \"MX.4973227\": \"2024-01-17\", \"MX.39827\": \"2024-01-25\", \"MX.39917\": \"2024-01-30\"}', 'MA.3', '2024-01-28 15:29:01', 'MA.3', '2024-01-31 08:05:20', 0),
(7, 5, 'Foo', 'Bar', 0, '{}', 'MA.3', '2024-01-29 21:13:01', 'MA.3', '2024-01-29 21:13:11', 0),
(8, 4, 'Foo', 'Bar', 0, '{}', 'MA.3', '2024-01-30 15:48:29', 'MA.3', '2024-01-30 15:48:29', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `challenges`
--
ALTER TABLE `challenges`
  ADD PRIMARY KEY (`challenge_id`),
  ADD KEY `status` (`status`);

--
-- Indexes for table `participations`
--
ALTER TABLE `participations`
  ADD PRIMARY KEY (`participation_id`),
  ADD KEY `challenge_id` (`challenge_id`),
  ADD KEY `meta_created_by` (`meta_created_by`),
  ADD KEY `taxa_count` (`taxa_count`);
ALTER TABLE `participations` ADD FULLTEXT KEY `taxa_json_fulltext` (`taxa_json`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `challenges`
--
ALTER TABLE `challenges`
  MODIFY `challenge_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `participations`
--
ALTER TABLE `participations`
  MODIFY `participation_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

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
