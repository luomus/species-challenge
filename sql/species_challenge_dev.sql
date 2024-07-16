-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Jul 16, 2024 at 09:41 AM
-- Server version: 10.5.25-MariaDB-ubu2004
-- PHP Version: 8.2.8

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `species_challenge_dev`
--

USE `species_challenge_dev`;

-- --------------------------------------------------------

--
-- Table structure for table `challenges`
--

CREATE TABLE `challenges` (
  `challenge_id` int(11) NOT NULL,
  `taxon` varchar(16) NOT NULL,
  `autocomplete` varchar(256) DEFAULT NULL,
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

INSERT INTO `challenges` (`challenge_id`, `taxon`, `autocomplete`, `year`, `type`, `title`, `status`, `description`, `meta_created_by`, `meta_created_at`, `meta_edited_by`, `meta_edited_at`) VALUES
(1, 'insecta_2024', '', 2024, 'challenge100', 'Hyönteiset 2024', 'draft', '', 'MA.3', '2024-01-28 10:39:59', 'MA.3', '2024-07-16 09:40:19'),
(2, 'fungi_2024', '', 2024, 'challenge100', 'Sienet 2024', 'closed', 'Kuka havaitsee vuoden aikana eniten lajeja omalla kotikunnassaan? Perinteinen kuntahaaste on avoin kilpailu kaikille alueen asukkaille.\r\n\r\nLiikkumistavaksi suositellaan ekovaihtoehtoja, mutta kaikki liikkumistavat ovat kuitenkin sallittuja. Lorem ipsum dolor sit amet. Liikkumistavaksi suositellaan ekovaihtoehtoja, mutta kaikki liikkumistavat ovat kuitenkin sallittuja. Lorem ipsum dolor sit amet.', 'MA.3', '2024-01-28 10:39:59', 'MA.3', '2024-07-16 09:41:06'),
(3, 'fungi_2024', '', 2023, 'challenge100', 'Sienet 2023', 'draft', '', 'MA.3', '2024-01-28 10:41:49', 'MA.3', '2024-07-16 09:40:08'),
(4, 'plantae_2024', '', 2024, 'challenge100', 'Kasvit 2024', 'open', '<img src=\'/static/images/icon_plantae_100.png\'>\r\n\r\nHavaitse 100 kasvilajia vuodessa!\r\n<p>\r\n<a href=\"https://pinkka.laji.fi/pinkat/#/\">Lue lisää haasteen lajeista Pinkasta</a>.', 'MA.3', '2024-01-28 10:42:23', 'MA.3', '2024-07-16 08:21:42'),
(5, 'fungi_2024', '', 2024, 'challenge100', 'Sienihaaste 2024 Playwright', 'open', '<img src=\'/static/images/icon_fungi_100.png\'>\r\n\r\nHavaitse 100 sienilajia vuodessa!', 'MA.3', '2024-01-28 22:32:58', 'MA.3', '2024-07-16 08:22:00'),
(6, 'insecta_2024', '', 2024, 'challenge100', '100 hyönteislajia 2024', 'open', '<img src=\'/static/images/icon_insecta_100.png\'>\r\n\r\nHavaitse 100 hyönteislajia vuodessa!', 'MA.3', '2024-01-28 22:33:44', 'MA.3', '2024-07-16 08:22:10');

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
(1, 2, 'Testaaja 2', 'Helsinki 2', 0, '{}', 'MA.3', '2024-01-28 10:47:46', 'MA.3', '2024-01-31 12:53:43', 1),
(2, 2, 'Teppo Testaaja', 'Vantaa', 0, NULL, 'MA.3', '2024-01-28 10:51:00', 'MA.3', '2024-01-28 10:51:03', 0),
(3, 2, 'Ulla Uusmäki-Vanhalaakso', 'Outokumpu, kummun takana', 0, NULL, 'MA.3', '2024-01-28 13:53:50', 'MA.3', '2024-01-28 13:54:36', 0),
(4, 2, 'Untamo Ikämies-Akana', 'Akaa-Loimaa', 0, NULL, 'MA.3', '2024-01-28 13:54:52', 'MA.3', '2024-01-28 15:18:24', 0),
(5, 4, 'Nimi Merkkinen', 'Nimismiehenkylä', 38, '{\"MX.43922\": \"2024-02-01\", \"MX.43502\": \"2024-02-05\", \"MX.43901\": \"2024-02-05\", \"MX.43956\": \"2024-02-05\", \"MX.44366\": \"2024-02-06\", \"MX.37691\": \"2024-01-30\", \"MX.37717\": \"2024-01-17\", \"MX.37719\": \"2024-01-25\", \"MX.37763\": \"2024-01-01\", \"MX.37771\": \"2024-01-30\", \"MX.37752\": \"2024-01-30\", \"MX.37826\": \"2024-01-30\", \"MX.37812\": \"2024-01-10\", \"MX.37819\": \"2024-01-30\", \"MX.39201\": \"2024-01-30\", \"MX.39235\": \"2024-01-30\", \"MX.39761\": \"2024-02-02\", \"MX.39871\": \"2024-02-06\", \"MX.39887\": \"2024-01-30\", \"MX.39917\": \"2024-01-11\", \"MX.38364\": \"2024-02-06\", \"MX.38279\": \"2024-01-02\", \"MX.38598\": \"2024-01-13\", \"MX.39052\": \"2024-01-20\", \"MX.39038\": \"2024-01-11\", \"MX.39465\": \"2024-01-18\", \"MX.39673\": \"2024-01-30\", \"MX.4994055\": \"2024-01-03\", \"MX.37747\": \"2024-01-30\", \"MX.40138\": \"2024-01-30\", \"MX.4973227\": \"2024-01-17\", \"MX.39967\": \"2024-01-30\", \"MX.38301\": \"2024-01-30\", \"MX.40632\": \"2024-01-11\", \"MX.38843\": \"2024-01-25\", \"MX.40643\": \"2024-02-05\", \"MX.39687\": \"2024-02-06\", \"MX.40028\": \"2024-02-08\"}', 'MA.3', '2024-01-28 15:19:17', 'MA.3', '2024-02-08 19:44:08', 0),
(6, 4, 'André D\'Artágnan', 'Ääkkölä ääkkölärules', 33, '{\"MX.43668\": \"2024-02-02\", \"MX.43901\": \"2024-02-07\", \"MX.43933\": \"2024-02-01\", \"MX.37691\": \"2024-01-11\", \"MX.37721\": \"2024-01-02\", \"MX.37717\": \"2024-01-27\", \"MX.37719\": \"2024-01-28\", \"MX.37763\": \"2024-01-10\", \"MX.37771\": \"2024-01-18\", \"MX.37752\": \"2024-01-30\", \"MX.39201\": \"2024-01-30\", \"MX.39827\": \"2024-01-25\", \"MX.39703\": \"2024-02-02\", \"MX.39711\": \"2024-02-02\", \"MX.38364\": \"2024-02-02\", \"MX.38387\": \"2024-02-02\", \"MX.38795\": \"2024-01-01\", \"MX.38869\": \"2024-02-02\", \"MX.38834\": \"2024-02-02\", \"MX.38863\": \"2024-02-02\", \"MX.38939\": \"2024-02-01\", \"MX.38797\": \"2024-02-02\", \"MX.38802\": \"2024-02-02\", \"MX.37984\": \"2024-02-02\", \"MX.39122\": \"2024-02-02\", \"MX.38750\": \"2024-02-02\", \"MX.4994055\": \"2024-01-18\", \"MX.40138\": \"2024-01-30\", \"MX.40150\": \"2024-01-30\", \"MX.4973227\": \"2024-01-17\", \"MX.4984037\": \"2024-02-02\", \"MX.39750\": \"2024-01-10\", \"MX.38820\": \"2024-02-02\"}', 'MA.3', '2024-01-28 15:29:01', 'MA.3', '2024-02-07 10:33:45', 0),
(7, 5, 'Nollanen', 'Peräkyläntaka', 3, '{\"MX.43922\": \"2024-02-09\", \"MX.37812\": \"2024-02-09\", \"MX.37819\": \"2024-02-09\"}', 'MA.3', '2024-01-29 21:13:01', 'MA.3', '2024-02-09 09:24:59', 0),
(8, 4, 'Meikäläinen', 'Meikäläisenkylä', 9, '{\"MX.37721\": \"2024-01-11\", \"MX.37719\": \"2024-01-16\", \"MX.39201\": \"2024-01-31\", \"MX.39761\": \"2024-01-01\", \"MX.39823\": \"2024-01-31\", \"MX.39328\": \"2024-01-31\", \"MX.38048\": \"2024-01-10\", \"MX.39889\": \"2024-01-30\", \"MX.38004\": \"2024-02-08\"}', 'MA.3', '2024-01-30 15:48:29', 'MA.3', '2024-02-09 08:20:48', 0),
(9, 4, 'Teppo Testaaja', 'Testipaikka', 7, '{\"MX.43922\": \"2024-01-01\", \"MX.43956\": \"2024-02-06\", \"MX.39976\": \"2024-02-01\", \"MX.39890\": \"2024-01-17\", \"MX.38048\": \"2024-01-17\", \"MX.38263\": \"2024-01-06\", \"MX.39158\": \"2024-01-06\"}', 'MA.315', '2024-02-05 12:02:33', 'MA.315', '2024-02-06 07:20:10', 0),
(35, 5, 'Testi Äläpoista', 'Playwright-paikka', 2, '{\"MX.43922\": \"2024-02-09\", \"MX.39687\": \"2024-02-09\"}', 'MA.3', '2024-02-09 08:23:23', 'MA.3', '2024-02-09 08:24:19', 0);

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
  MODIFY `participation_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

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
