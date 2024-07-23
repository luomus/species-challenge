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
  `date_begin` varchar(10) DEFAULT NULL,
  `date_end` varchar(10) DEFAULT NULL,
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

INSERT INTO `challenges` (`challenge_id`, `taxon`, `autocomplete`, `date_begin`, `date_end`, `type`, `title`, `status`, `description`, `meta_created_by`, `meta_created_at`, `meta_edited_by`, `meta_edited_at`) VALUES
(1, 'insecta_2024', '', NULL, NULL, 'challenge100', 'Hyönteiset 2024', 'draft', '', 'MA.3', '2024-01-28 10:39:59', 'MA.3', '2024-07-16 09:40:19'),
(2, 'fungi_2024', '', NULL, NULL, 'challenge100', 'Sienet 2024', 'closed', 'Kuka havaitsee vuoden aikana eniten lajeja omalla kotikunnassaan? Perinteinen kuntahaaste on avoin kilpailu kaikille alueen asukkaille.\r\n\r\nLiikkumistavaksi suositellaan ekovaihtoehtoja, mutta kaikki liikkumistavat ovat kuitenkin sallittuja. Lorem ipsum dolor sit amet. Liikkumistavaksi suositellaan ekovaihtoehtoja, mutta kaikki liikkumistavat ovat kuitenkin sallittuja. Lorem ipsum dolor sit amet.', 'MA.3', '2024-01-28 10:39:59', 'MA.3', '2024-07-16 09:41:06'),
(3, 'fungi_2024', '', '2024-07-01', '2024-07-31', 'challenge100', 'Luonnos sienet', 'open', '', 'MA.3', '2024-01-28 10:41:49', 'MA.3', '2024-07-23 12:51:34'),
(4, 'plantae_2024', '', '2024-01-01', '2024-12-31', 'challenge100', 'Kasvit 2024', 'open', '<img src=\'/static/images/icon_plantae_100.png\'>\r\n\r\nHavaitse 100 kasvilajia vuodessa!\r\n<p>\r\n<a href=\"https://pinkka.laji.fi/pinkat/#/\">Lue lisää haasteen lajeista Pinkasta</a>.', 'MA.3', '2024-01-28 10:42:23', 'MA.3', '2024-07-23 08:51:55'),
(5, 'fungi_2024', '', NULL, NULL, 'challenge100', 'Sienihaaste 2024 Playwright', 'open', '<img src=\'/static/images/icon_fungi_100.png\'>\r\n\r\nHavaitse 100 sienilajia vuodessa!', 'MA.3', '2024-01-28 22:32:58', 'MA.3', '2024-07-16 08:22:00'),
(6, 'insecta_2024', '', NULL, NULL, 'challenge100', '100 hyönteislajia 2024', 'open', '<img src=\'/static/images/icon_insecta_100.png\'>\r\n\r\nHavaitse 100 hyönteislajia vuodessa!', 'MA.3', '2024-01-28 22:33:44', 'MA.3', '2024-07-16 08:22:10'),
(12, 'plantae_2024', '', '2024-07-01', '2024-07-31', 'challenge100', 'Heinähaaste eli testi', 'open', 'Testi 2', 'MA.3', '2024-07-23 08:57:59', 'MA.3', '2024-07-23 08:58:09');

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
(5, 4, 'Nimi Merkkinen', 'Nimismiehenkylä', 159, '{\"MX.4994055\": \"2024-01-03\", \"MX.37747\": \"2024-01-30\", \"MX.40138\": \"2024-01-30\", \"MX.4973227\": \"2024-01-17\", \"MX.39967\": \"2024-01-30\", \"MX.38301\": \"2024-01-30\", \"MX.40632\": \"2024-01-11\", \"MX.38843\": \"2024-01-25\", \"MX.40643\": \"2024-02-05\", \"MX.39687\": \"2024-02-06\", \"MX.40028\": \"2024-02-08\", \"MX.43922\": \"2024-02-01\", \"MX.43502\": \"2024-02-05\", \"MX.43983\": \"2024-07-17\", \"MX.43668\": \"2024-07-17\", \"MX.43901\": \"2024-02-05\", \"MX.43956\": \"2024-02-05\", \"MX.43803\": \"2024-07-17\", \"MX.43933\": \"2024-07-17\", \"MX.44366\": \"2024-02-06\", \"MX.44182\": \"2024-07-17\", \"MX.37691\": \"2024-01-30\", \"MX.37721\": \"2024-07-17\", \"MX.37717\": \"2024-01-17\", \"MX.37719\": \"2024-01-25\", \"MX.37763\": \"2024-01-01\", \"MX.37771\": \"2024-01-30\", \"MX.37752\": \"2024-01-30\", \"MX.37826\": \"2024-01-30\", \"MX.37812\": \"2024-01-10\", \"MX.37819\": \"2024-01-30\", \"MX.40092\": \"2024-07-17\", \"MX.39201\": \"2024-01-30\", \"MX.39235\": \"2024-01-30\", \"MX.39185\": \"2024-07-17\", \"MX.39970\": \"2024-07-17\", \"MX.39976\": \"2024-07-17\", \"MX.39974\": \"2024-07-17\", \"MX.39812\": \"2024-07-17\", \"MX.39809\": \"2024-07-17\", \"MX.39761\": \"2024-02-02\", \"MX.39871\": \"2024-02-06\", \"MX.39835\": \"2024-07-17\", \"MX.39890\": \"2024-07-17\", \"MX.39887\": \"2024-01-30\", \"MX.39827\": \"2024-07-17\", \"MX.39917\": \"2024-01-11\", \"MX.39727\": \"2024-07-17\", \"MX.39830\": \"2024-07-17\", \"MX.42419\": \"2024-07-17\", \"MX.39823\": \"2024-07-17\", \"MX.39847\": \"2024-07-17\", \"MX.39703\": \"2024-07-17\", \"MX.39711\": \"2024-07-17\", \"MX.39328\": \"2024-07-17\", \"MX.39402\": \"2024-07-17\", \"MX.38364\": \"2024-02-06\", \"MX.38387\": \"2024-07-17\", \"MX.38073\": \"2024-07-17\", \"MX.38131\": \"2024-07-17\", \"MX.38055\": \"2024-07-17\", \"MX.38048\": \"2024-07-17\", \"MX.38780\": \"2024-07-17\", \"MX.38217\": \"2024-07-17\", \"MX.38279\": \"2024-01-02\", \"MX.38285\": \"2024-07-17\", \"MX.38263\": \"2024-07-17\", \"MX.39166\": \"2024-07-17\", \"MX.39336\": \"2024-07-17\", \"MX.39368\": \"2024-07-17\", \"MX.39343\": \"2024-07-17\", \"MX.39347\": \"2024-07-17\", \"MX.39358\": \"2024-07-17\", \"MX.39158\": \"2024-07-17\", \"MX.38614\": \"2024-07-17\", \"MX.38598\": \"2024-01-13\", \"MX.38646\": \"2024-07-17\", \"MX.38634\": \"2024-07-17\", \"MX.38626\": \"2024-07-17\", \"MX.38605\": \"2024-07-17\", \"MX.38622\": \"2024-07-17\", \"MX.38618\": \"2024-07-17\", \"MX.38621\": \"2024-07-17\", \"MX.38620\": \"2024-07-17\", \"MX.38676\": \"2024-07-17\", \"MX.38674\": \"2024-07-17\", \"MX.38670\": \"2024-07-17\", \"MX.39002\": \"2024-07-17\", \"MX.38950\": \"2024-07-17\", \"MX.39047\": \"2024-07-17\", \"MX.39052\": \"2024-01-20\", \"MX.39038\": \"2024-01-11\", \"MX.39046\": \"2024-07-17\", \"MX.38972\": \"2024-07-17\", \"MX.38008\": \"2024-07-17\", \"MX.38010\": \"2024-07-17\", \"MX.37993\": \"2024-07-17\", \"MX.37999\": \"2024-07-17\", \"MX.38016\": \"2024-07-17\", \"MX.37990\": \"2024-07-17\", \"MX.39288\": \"2024-07-17\", \"MX.39287\": \"2024-07-17\", \"MX.39292\": \"2024-07-17\", \"MX.39138\": \"2024-07-17\", \"MX.39465\": \"2024-01-18\", \"MX.39493\": \"2024-07-17\", \"MX.39500\": \"2024-07-17\", \"MX.39331\": \"2024-07-17\", \"MX.39633\": \"2024-07-17\", \"MX.39632\": \"2024-07-17\", \"MX.39661\": \"2024-07-17\", \"MX.39663\": \"2024-07-17\", \"MX.39589\": \"2024-07-17\", \"MX.39673\": \"2024-01-30\", \"MX.39609\": \"2024-07-17\", \"MX.39608\": \"2024-07-17\", \"MX.38590\": \"2024-07-17\", \"MX.38563\": \"2024-07-17\", \"MX.38338\": \"2024-07-17\", \"MX.38331\": \"2024-07-17\", \"MX.38321\": \"2024-07-17\", \"MX.38336\": \"2024-07-17\", \"MX.38686\": \"2024-07-17\", \"MX.38715\": \"2024-07-17\", \"MX.39079\": \"2024-07-17\", \"MX.39088\": \"2024-07-17\", \"MX.39105\": \"2024-07-17\", \"MX.39130\": \"2024-07-17\", \"MX.40258\": \"2024-07-17\", \"MX.40261\": \"2024-07-17\", \"MX.40196\": \"2024-07-17\", \"MX.40505\": \"2024-07-17\", \"MX.40639\": \"2024-07-17\", \"MX.40188\": \"2024-07-17\", \"MX.37962\": \"2024-07-17\", \"MX.37859\": \"2024-07-17\", \"MX.37879\": \"2024-07-17\", \"MX.37863\": \"2024-07-17\", \"MX.37924\": \"2024-07-17\", \"MX.37890\": \"2024-07-17\", \"MX.37897\": \"2024-07-17\", \"MX.37922\": \"2024-07-17\", \"MX.37896\": \"2024-07-17\", \"MX.38844\": \"2024-07-17\", \"MX.38832\": \"2024-07-17\", \"MX.38795\": \"2024-07-17\", \"MX.38869\": \"2024-07-17\", \"MX.38834\": \"2024-07-17\", \"MX.38863\": \"2024-07-17\", \"MX.38939\": \"2024-07-17\", \"MX.38815\": \"2024-07-17\", \"MX.38799\": \"2024-07-17\", \"MX.38797\": \"2024-07-17\", \"MX.38804\": \"2024-07-17\", \"MX.38802\": \"2024-07-17\", \"MX.38910\": \"2024-07-17\", \"MX.37984\": \"2024-07-17\", \"MX.39122\": \"2024-07-17\", \"MX.38750\": \"2024-07-17\"}', 'MA.3', '2024-01-28 15:19:17', 'MA.3', '2024-07-17 08:54:15', 0),
(6, 4, 'André D\'Artágnan', 'Ääkkölä ääkkölärules', 33, '{\"MX.43668\": \"2024-02-02\", \"MX.43901\": \"2024-02-07\", \"MX.43933\": \"2024-02-01\", \"MX.37691\": \"2024-01-11\", \"MX.37721\": \"2024-01-02\", \"MX.37717\": \"2024-01-27\", \"MX.37719\": \"2024-01-28\", \"MX.37763\": \"2024-01-10\", \"MX.37771\": \"2024-01-18\", \"MX.37752\": \"2024-01-30\", \"MX.39201\": \"2024-01-30\", \"MX.39827\": \"2024-01-25\", \"MX.39703\": \"2024-02-02\", \"MX.39711\": \"2024-02-02\", \"MX.38364\": \"2024-02-02\", \"MX.38387\": \"2024-02-02\", \"MX.38795\": \"2024-01-01\", \"MX.38869\": \"2024-02-02\", \"MX.38834\": \"2024-02-02\", \"MX.38863\": \"2024-02-02\", \"MX.38939\": \"2024-02-01\", \"MX.38797\": \"2024-02-02\", \"MX.38802\": \"2024-02-02\", \"MX.37984\": \"2024-02-02\", \"MX.39122\": \"2024-02-02\", \"MX.38750\": \"2024-02-02\", \"MX.4994055\": \"2024-01-18\", \"MX.40138\": \"2024-01-30\", \"MX.40150\": \"2024-01-30\", \"MX.4973227\": \"2024-01-17\", \"MX.4984037\": \"2024-02-02\", \"MX.39750\": \"2024-01-10\", \"MX.38820\": \"2024-02-02\"}', 'MA.3', '2024-01-28 15:29:01', 'MA.3', '2024-02-07 10:33:45', 0),
(7, 5, 'Nollanen', 'Peräkyläntaka', 3, '{\"MX.43922\": \"2024-02-09\", \"MX.37812\": \"2024-02-09\", \"MX.37819\": \"2024-02-09\"}', 'MA.3', '2024-01-29 21:13:01', 'MA.3', '2024-02-09 09:24:59', 0),
(8, 4, 'Pekka Paljonlajeja', 'Meikäläisenkylä', 715, '{\"MX.200035\": \"2024-03-26\", \"MX.39979\": \"2024-07-08\", \"MX.39788\": \"2024-07-08\", \"MX.209578\": \"2024-04-07\", \"MX.39236\": \"2024-07-08\", \"MX.39750\": \"2024-05-15\", \"MX.39936\": \"2024-05-26\", \"MX.39144\": \"2024-06-16\", \"MX.38238\": \"2024-07-08\", \"MX.39050\": \"2024-07-08\", \"MX.38228\": \"2024-07-08\", \"MX.39248\": \"2024-05-17\", \"MX.38229\": \"2024-07-08\", \"MX.40129\": \"2024-05-22\", \"MX.40436\": \"2024-07-07\", \"MX.40449\": \"2024-07-08\", \"MX.37943\": \"2024-07-01\", \"MX.38882\": \"2024-07-08\", \"MX.38884\": \"2024-07-08\", \"MX.38888\": \"2024-06-24\", \"MX.40896\": \"2024-07-08\", \"MX.5000832\": \"2024-07-08\", \"MX.41295\": \"2024-07-08\", \"MX.39199\": \"2024-05-13\", \"MX.38234\": \"2024-07-08\", \"MX.38856\": \"2024-04-17\", \"MX.38858\": \"2024-07-08\", \"MX.39704\": \"2024-04-01\", \"MX.39709\": \"2024-04-01\", \"MX.39707\": \"2024-07-08\", \"MX.39708\": \"2024-07-08\", \"MX.39705\": \"2024-04-17\", \"MX.39209\": \"2024-07-07\", \"MX.39754\": \"2024-07-08\", \"MX.38103\": \"2024-07-08\", \"MX.39587\": \"2024-07-07\", \"MX.39706\": \"2024-06-26\", \"MX.39772\": \"2024-06-14\", \"MX.38817\": \"2024-06-16\", \"MX.38820\": \"2024-06-08\", \"MX.38818\": \"2024-05-16\", \"MX.40593\": \"2024-03-25\", \"MX.38395\": \"2024-07-06\", \"MX.40209\": \"2024-06-07\", \"MX.39826\": \"2024-06-17\", \"MX.38377\": \"2024-05-22\", \"MX.38170\": \"2024-07-06\", \"MX.38191\": \"2024-07-02\", \"MX.43655\": \"2024-07-02\", \"MX.39100\": \"2024-07-02\", \"MX.41520\": \"2024-07-01\", \"MX.41550\": \"2024-07-01\", \"MX.39231\": \"2024-07-01\", \"MX.39223\": \"2024-06-08\", \"MX.38056\": \"2024-06-08\", \"MX.43982\": \"2024-06-08\", \"MX.40554\": \"2024-06-08\", \"MX.40229\": \"2024-06-05\", \"MX.42524\": \"2024-06-03\", \"MX.40333\": \"2024-06-08\", \"MX.40331\": \"2024-06-08\", \"MX.40523\": \"2024-06-16\", \"MX.39889\": \"2024-03-30\", \"MX.38106\": \"2024-06-05\", \"MX.40295\": \"2024-06-08\", \"MX.40296\": \"2024-06-14\", \"MX.40340\": \"2024-06-09\", \"MX.40339\": \"2024-06-09\", \"MX.39779\": \"2024-06-08\", \"MX.39679\": \"2024-04-22\", \"MX.40049\": \"2024-06-08\", \"MX.39518\": \"2024-06-08\", \"MX.39359\": \"2024-05-17\", \"MX.4972164\": \"2024-05-26\", \"MX.38629\": \"2024-06-15\", \"MX.40869\": \"2024-05-26\", \"MX.39157\": \"2024-06-09\", \"MX.44042\": \"2024-06-08\", \"MX.37716\": \"2024-06-08\", \"MX.39155\": \"2024-06-08\", \"MX.39082\": \"2024-06-08\", \"MX.38047\": \"2024-06-08\", \"MX.38049\": \"2024-06-05\", \"MX.39039\": \"2024-05-31\", \"MX.41442\": \"2024-05-27\", \"MX.39522\": \"2024-05-27\", \"MX.39674\": \"2024-05-25\", \"MX.39767\": \"2024-05-25\", \"MX.40795\": \"2024-05-26\", \"MX.39177\": \"2024-05-26\", \"MX.5021101\": \"2024-05-26\", \"MX.38350\": \"2024-05-26\", \"MX.40006\": \"2024-05-26\", \"MX.39790\": \"2024-05-16\", \"MX.38931\": \"2024-05-16\", \"MX.39221\": \"2024-05-25\", \"MX.5014645\": \"2024-05-26\", \"MX.37869\": \"2024-05-26\", \"MX.39348\": \"2024-05-25\", \"MX.38514\": \"2024-05-25\", \"MX.38247\": \"2024-05-25\", \"MX.40775\": \"2024-04-19\", \"MX.40774\": \"2024-05-26\", \"MX.41056\": \"2024-05-25\", \"MX.42792\": \"2024-05-26\", \"MX.37918\": \"2024-05-22\", \"MX.4973120\": \"2024-05-26\", \"MX.41454\": \"2024-05-26\", \"MX.41073\": \"2024-05-25\", \"MX.40281\": \"2024-04-10\", \"MX.5023853\": \"2024-05-26\", \"MX.41223\": \"2024-05-25\", \"MX.39273\": \"2024-05-25\", \"MX.39537\": \"2024-05-19\", \"MX.39091\": \"2024-05-26\", \"MX.5022210\": \"2024-05-26\", \"MX.40895\": \"2024-05-25\", \"MX.39771\": \"2024-05-25\", \"MX.42799\": \"2024-05-26\", \"MX.42062\": \"2024-05-26\", \"MX.40871\": \"2024-05-26\", \"MX.40866\": \"2024-05-15\", \"MX.42711\": \"2024-05-26\", \"MX.42500\": \"2024-05-26\", \"MX.41007\": \"2024-05-25\", \"MX.40729\": \"2024-05-26\", \"MX.43757\": \"2024-05-26\", \"MX.38266\": \"2024-05-25\", \"MX.39383\": \"2024-05-25\", \"MX.4973125\": \"2024-05-25\", \"MX.42701\": \"2024-05-24\", \"MX.38142\": \"2024-05-22\", \"MX.40840\": \"2024-05-25\", \"MX.39280\": \"2024-05-25\", \"MX.40951\": \"2024-05-25\", \"MX.43617\": \"2024-05-25\", \"MX.38398\": \"2024-05-25\", \"MX.39240\": \"2024-05-25\", \"MX.38146\": \"2024-05-25\", \"MX.39284\": \"2024-04-25\", \"MX.38311\": \"2024-05-25\", \"MX.39582\": \"2024-05-21\", \"MX.40021\": \"2024-05-18\", \"MX.40417\": \"2024-05-22\", \"MX.41389\": \"2024-05-25\", \"MX.39852\": \"2024-05-25\", \"MX.39054\": \"2024-05-25\", \"MX.39735\": \"2024-05-25\", \"MX.38843\": \"2024-04-10\", \"MX.39444\": \"2024-05-22\", \"MX.39411\": \"2024-05-21\", \"MX.39408\": \"2024-05-21\", \"MX.39942\": \"2024-05-21\", \"MX.38712\": \"2024-05-19\", \"MX.38454\": \"2024-05-10\", \"MX.38415\": \"2024-05-14\", \"MX.38323\": \"2024-05-17\", \"MX.40461\": \"2024-03-26\", \"MX.39468\": \"2024-03-28\", \"MX.39469\": \"2024-05-22\", \"MX.38475\": \"2024-05-22\", \"MX.40577\": \"2024-05-22\", \"MX.40269\": \"2024-05-22\", \"MX.38457\": \"2024-05-22\", \"MX.41656\": \"2024-05-25\", \"MX.40812\": \"2024-05-11\", \"MX.39615\": \"2024-05-15\", \"MX.42801\": \"2024-04-24\", \"MX.41698\": \"2024-05-15\", \"MX.39600\": \"2024-04-13\", \"MX.38097\": \"2024-03-25\", \"MX.38100\": \"2024-05-22\", \"MX.37939\": \"2024-05-15\", \"MX.42786\": \"2024-05-25\", \"MX.38066\": \"2024-05-22\", \"MX.4974006\": \"2024-05-25\", \"MX.38829\": \"2024-05-24\", \"MX.38179\": \"2024-05-25\", \"MX.40626\": \"2024-05-25\", \"MX.37841\": \"2024-05-22\", \"MX.37845\": \"2024-05-22\", \"MX.39512\": \"2024-05-25\", \"MX.41543\": \"2024-05-25\", \"MX.38773\": \"2024-05-25\", \"MX.38875\": \"2024-04-09\", \"MX.40865\": \"2024-05-24\", \"MX.38381\": \"2024-05-15\", \"MX.39005\": \"2024-05-21\", \"MX.39270\": \"2024-04-15\", \"MX.4978971\": \"2024-05-25\", \"MX.38531\": \"2024-03-25\", \"MX.37854\": \"2024-05-25\", \"MX.39467\": \"2024-04-30\", \"MX.39229\": \"2024-05-15\", \"MX.37895\": \"2024-05-15\", \"MX.39740\": \"2024-05-22\", \"MX.40415\": \"2024-05-25\", \"MX.37971\": \"2024-05-25\", \"MX.4973514\": \"2024-05-25\", \"MX.4973686\": \"2024-05-25\", \"MX.39309\": \"2024-05-25\", \"MX.39404\": \"2024-05-25\", \"MX.42960\": \"2024-05-25\", \"MX.38860\": \"2024-05-19\", \"MX.38241\": \"2024-05-21\", \"MX.39375\": \"2024-05-21\", \"MX.41075\": \"2024-05-20\", \"MX.38741\": \"2024-05-19\", \"MX.38748\": \"2024-03-30\", \"MX.38830\": \"2024-05-18\", \"MX.40582\": \"2024-05-19\", \"MX.43768\": \"2024-05-19\", \"MX.37979\": \"2024-05-19\", \"MX.39428\": \"2024-05-14\", \"MX.37885\": \"2024-05-17\", \"MX.39057\": \"2024-05-17\", \"MX.40557\": \"2024-05-17\", \"MX.42856\": \"2024-05-17\", \"MX.37887\": \"2024-05-17\", \"MX.41195\": \"2024-05-17\", \"MX.41093\": \"2024-05-17\", \"MX.40117\": \"2024-05-17\", \"MX.41086\": \"2024-05-17\", \"MX.41231\": \"2024-05-17\", \"MX.41229\": \"2024-05-17\", \"MX.40215\": \"2024-05-16\", \"MX.38993\": \"2024-05-15\", \"MX.42808\": \"2024-05-16\", \"MX.41604\": \"2024-05-16\", \"MX.40009\": \"2024-05-16\", \"MX.40094\": \"2024-05-16\", \"MX.39995\": \"2024-05-16\", \"MX.39285\": \"2024-05-16\", \"MX.37776\": \"2024-05-15\", \"MX.39908\": \"2024-04-11\", \"MX.40377\": \"2024-05-15\", \"MX.40228\": \"2024-05-15\", \"MX.39426\": \"2024-05-15\", \"MX.43572\": \"2024-05-15\", \"MX.38366\": \"2024-04-22\", \"MX.39614\": \"2024-05-15\", \"MX.39996\": \"2024-05-15\", \"MX.38567\": \"2024-05-15\", \"MX.38092\": \"2024-05-15\", \"MX.39143\": \"2024-05-15\", \"MX.38611\": \"2024-03-25\", \"MX.41672\": \"2024-04-14\", \"MX.39275\": \"2024-04-14\", \"MX.42823\": \"2024-05-11\", \"MX.39986\": \"2024-05-15\", \"MX.41673\": \"2024-05-12\", \"MX.4973419\": \"2024-05-12\", \"MX.39807\": \"2024-05-14\", \"MX.4973472\": \"2024-05-11\", \"MX.5068745\": \"2024-05-11\", \"MX.40298\": \"2024-05-15\", \"MX.38489\": \"2024-05-13\", \"MX.41649\": \"2024-05-11\", \"MX.39840\": \"2024-03-25\", \"MX.40098\": \"2024-05-04\", \"MX.40681\": \"2024-05-11\", \"MX.40011\": \"2024-05-14\", \"MX.39972\": \"2024-05-11\", \"MX.38367\": \"2024-05-13\", \"MX.37747\": \"2024-05-11\", \"MX.39967\": \"2024-05-13\", \"MX.38654\": \"2024-05-09\", \"MX.38655\": \"2024-05-11\", \"MX.37857\": \"2024-05-05\", \"MX.41264\": \"2024-04-24\", \"MX.37883\": \"2024-05-09\", \"MX.41090\": \"2024-05-10\", \"MX.41064\": \"2024-04-05\", \"MX.38455\": \"2024-04-12\", \"MX.38585\": \"2024-05-10\", \"MX.38413\": \"2024-05-10\", \"MX.38493\": \"2024-05-10\", \"MX.209506\": \"2024-04-22\", \"MX.39453\": \"2024-04-30\", \"MX.40015\": \"2024-04-29\", \"MX.39997\": \"2024-04-28\", \"MX.38792\": \"2024-04-28\", \"MX.38105\": \"2024-04-28\", \"MX.4984171\": \"2024-04-28\", \"MX.38249\": \"2024-04-27\", \"MX.39010\": \"2024-04-26\", \"MX.41572\": \"2024-04-10\", \"MX.38873\": \"2024-04-25\", \"MX.38348\": \"2024-04-25\", \"MX.39264\": \"2024-04-25\", \"MX.38185\": \"2024-04-25\", \"MX.40788\": \"2024-04-25\", \"MX.39562\": \"2024-04-25\", \"MX.39559\": \"2024-04-25\", \"MX.41031\": \"2024-04-23\", \"MX.41029\": \"2024-04-24\", \"MX.40434\": \"2024-04-24\", \"MX.40672\": \"2024-04-24\", \"MX.39912\": \"2024-04-24\", \"MX.5022556\": \"2024-04-24\", \"MX.42805\": \"2024-04-24\", \"MX.4973286\": \"2024-04-24\", \"MX.41230\": \"2024-04-24\", \"MX.39205\": \"2024-04-24\", \"MX.38794\": \"2024-04-12\", \"MX.40685\": \"2024-04-24\", \"MX.39123\": \"2024-04-22\", \"MX.43834\": \"2024-04-22\", \"MX.40601\": \"2024-04-22\", \"MX.5082908\": \"2024-04-22\", \"MX.41208\": \"2024-04-21\", \"MX.37806\": \"2024-04-23\", \"MX.38707\": \"2024-04-22\", \"MX.40016\": \"2024-04-22\", \"MX.43689\": \"2024-04-22\", \"MX.39025\": \"2024-04-22\", \"MX.38373\": \"2024-04-20\", \"MX.39730\": \"2024-04-21\", \"MX.41429\": \"2024-04-20\", \"MX.39665\": \"2024-04-20\", \"MX.41158\": \"2024-04-21\", \"MX.4973234\": \"2024-04-20\", \"MX.39345\": \"2024-04-20\", \"MX.39346\": \"2024-04-20\", \"MX.43740\": \"2024-04-12\", \"MX.40682\": \"2024-04-21\", \"MX.5082909\": \"2024-04-15\", \"MX.5082474\": \"2024-04-17\", \"MX.37967\": \"2024-04-19\", \"MX.38916\": \"2024-04-19\", \"MX.38129\": \"2024-04-18\", \"MX.39473\": \"2024-04-19\", \"MX.4973473\": \"2024-04-19\", \"MX.39366\": \"2024-04-19\", \"MX.38872\": \"2024-04-12\", \"MX.41576\": \"2024-04-19\", \"MX.40977\": \"2024-04-17\", \"MX.5014938\": \"2024-04-19\", \"MX.39136\": \"2024-04-17\", \"MX.40996\": \"2024-04-17\", \"MX.39849\": \"2024-04-13\", \"MX.41603\": \"2024-04-14\", \"MX.38065\": \"2024-04-14\", \"MX.40457\": \"2024-04-10\", \"MX.39990\": \"2024-04-12\", \"MX.40817\": \"2024-04-12\", \"MX.41530\": \"2024-04-07\", \"MX.41303\": \"2024-04-13\", \"MX.40637\": \"2024-04-13\", \"MX.40467\": \"2024-04-12\", \"MX.37766\": \"2024-04-13\", \"MX.40474\": \"2024-04-13\", \"MX.38789\": \"2024-04-13\", \"MX.41583\": \"2024-04-13\", \"MX.43667\": \"2024-04-10\", \"MX.41420\": \"2024-04-13\", \"MX.43485\": \"2024-04-12\", \"MX.39302\": \"2024-04-13\", \"MX.38803\": \"2024-04-13\", \"MX.41152\": \"2024-04-12\", \"MX.41151\": \"2024-04-12\", \"MX.37836\": \"2024-04-13\", \"MX.40378\": \"2024-03-27\", \"MX.40189\": \"2024-04-13\", \"MX.39597\": \"2024-04-12\", \"MX.41542\": \"2024-04-13\", \"MX.37805\": \"2024-04-13\", \"MX.37969\": \"2024-04-09\", \"MX.40924\": \"2024-04-12\", \"MX.42653\": \"2024-04-12\", \"MX.38630\": \"2024-04-12\", \"MX.43683\": \"2024-04-13\", \"MX.41313\": \"2024-04-13\", \"MX.43698\": \"2024-04-13\", \"MX.40786\": \"2024-04-11\", \"MX.41097\": \"2024-04-11\", \"MX.44051\": \"2024-04-10\", \"MX.44037\": \"2024-04-10\", \"MX.44055\": \"2024-04-10\", \"MX.44036\": \"2024-04-10\", \"MX.5001617\": \"2024-04-10\", \"MX.44039\": \"2024-04-10\", \"MX.44070\": \"2024-04-10\", \"MX.5001616\": \"2024-04-10\", \"MX.44044\": \"2024-04-10\", \"MX.44060\": \"2024-04-10\", \"MX.44061\": \"2024-04-10\", \"MX.43938\": \"2024-04-10\", \"MX.44030\": \"2024-03-30\", \"MX.44035\": \"2024-03-25\", \"MX.44045\": \"2024-04-10\", \"MX.40341\": \"2024-04-10\", \"MX.44041\": \"2024-04-10\", \"MX.38619\": \"2024-04-10\", \"MX.38004\": \"2024-04-10\", \"MX.43826\": \"2024-04-11\", \"MX.38452\": \"2024-04-08\", \"MX.38813\": \"2024-04-09\", \"MX.40303\": \"2024-04-09\", \"MX.43905\": \"2024-04-02\", \"MX.40960\": \"2024-04-08\", \"MX.5013664\": \"2024-04-08\", \"MX.43937\": \"2024-04-08\", \"MX.41633\": \"2024-04-06\", \"MX.41447\": \"2024-04-07\", \"MX.41131\": \"2024-04-08\", \"MX.37781\": \"2024-04-08\", \"MX.38301\": \"2024-04-08\", \"MX.41269\": \"2024-04-08\", \"MX.41297\": \"2024-04-08\", \"MX.39390\": \"2024-04-08\", \"MX.38302\": \"2024-04-08\", \"MX.41308\": \"2024-04-08\", \"MX.41315\": \"2024-04-02\", \"MX.40838\": \"2024-04-05\", \"MX.41279\": \"2024-04-02\", \"MX.41573\": \"2024-04-05\", \"MX.38583\": \"2024-04-07\", \"MX.39294\": \"2024-04-05\", \"MX.41670\": \"2024-04-07\", \"MX.41132\": \"2024-04-07\", \"MX.41306\": \"2024-04-07\", \"MX.40839\": \"2024-04-07\", \"MX.39959\": \"2024-04-07\", \"MX.38240\": \"2024-04-03\", \"MX.39508\": \"2024-04-07\", \"MX.38671\": \"2024-04-07\", \"MX.38292\": \"2024-04-07\", \"MX.38570\": \"2024-04-07\", \"MX.41212\": \"2024-04-07\", \"MX.41574\": \"2024-04-07\", \"MX.38955\": \"2024-04-07\", \"MX.41311\": \"2024-04-07\", \"MX.40606\": \"2024-04-07\", \"MX.41527\": \"2024-04-07\", \"MX.40726\": \"2024-04-07\", \"MX.37823\": \"2024-04-06\", \"MX.38769\": \"2024-04-07\", \"MX.38935\": \"2024-04-07\", \"MX.37821\": \"2024-04-07\", \"MX.38816\": \"2024-04-07\", \"MX.37817\": \"2024-04-07\", \"MX.38163\": \"2024-04-07\", \"MX.38114\": \"2024-04-05\", \"MX.38673\": \"2024-04-04\", \"MX.37937\": \"2024-04-04\", \"MX.38107\": \"2024-04-04\", \"MX.40241\": \"2024-03-25\", \"MX.43747\": \"2024-03-25\", \"MX.38557\": \"2024-03-26\", \"MX.38556\": \"2024-03-26\", \"MX.38550\": \"2024-03-26\", \"MX.38528\": \"2024-03-26\", \"MX.43777\": \"2024-03-26\", \"MX.40202\": \"2024-03-26\", \"MX.39244\": \"2024-03-25\", \"MX.43928\": \"2024-03-25\", \"MX.43936\": \"2024-03-25\", \"MX.43551\": \"2024-03-26\", \"MX.43553\": \"2024-03-25\", \"MX.43673\": \"2024-03-26\", \"MX.39090\": \"2024-03-26\", \"MX.39928\": \"2024-03-25\", \"MX.40614\": \"2024-03-25\", \"MX.4972472\": \"2024-03-26\", \"MX.37694\": \"2024-03-25\", \"MX.40668\": \"2024-03-26\", \"MX.39338\": \"2024-03-26\", \"MX.38774\": \"2024-03-26\", \"MX.38768\": \"2024-03-26\", \"MX.38761\": \"2024-03-26\", \"MX.41431\": \"2024-03-25\", \"MX.40567\": \"2024-03-25\", \"MX.40564\": \"2024-03-25\", \"MX.40438\": \"2024-03-26\", \"MX.40445\": \"2024-03-26\", \"MX.40488\": \"2024-03-25\", \"MX.4994055\": \"2024-03-25\", \"MX.40175\": \"2024-03-25\", \"MX.41546\": \"2024-03-25\", \"MX.40203\": \"2024-03-26\", \"MX.39333\": \"2024-03-25\", \"MX.41541\": \"2024-03-25\", \"MX.38907\": \"2024-03-25\", \"MX.38592\": \"2024-03-26\", \"MX.39579\": \"2024-03-25\", \"MX.39577\": \"2024-03-26\", \"MX.37975\": \"2024-03-25\", \"MX.39831\": \"2024-03-25\", \"MX.4973216\": \"2024-03-25\", \"MX.38924\": \"2024-03-26\", \"MX.38786\": \"2024-03-25\", \"MX.41290\": \"2024-03-25\", \"MX.37810\": \"2024-03-25\", \"MX.39349\": \"2024-03-25\", \"MX.37976\": \"2024-03-26\", \"MX.37820\": \"2024-03-25\", \"MX.38842\": \"2024-03-25\", \"MX.39168\": \"2024-03-25\", \"MX.41278\": \"2024-03-25\", \"MX.39340\": \"2024-03-25\", \"MX.41413\": \"2024-03-25\", \"MX.4974029\": \"2024-03-25\", \"MX.37750\": \"2024-03-25\", \"MX.38938\": \"2024-03-25\", \"MX.43496\": \"2024-03-26\", \"MX.43981\": \"2024-03-25\", \"MX.38920\": \"2024-03-25\", \"MX.39000\": \"2024-03-26\", \"MX.40752\": \"2024-03-25\", \"MX.41307\": \"2024-03-26\", \"MX.38836\": \"2024-03-25\", \"MX.40617\": \"2024-03-25\", \"MX.40622\": \"2024-03-25\", \"MX.43805\": \"2024-03-25\", \"MX.43645\": \"2024-03-26\", \"MX.43875\": \"2024-03-29\", \"MX.38150\": \"2024-03-27\", \"MX.39904\": \"2024-03-26\", \"MX.43807\": \"2024-03-27\", \"MX.44080\": \"2024-03-27\", \"MX.38851\": \"2024-03-27\", \"MX.38439\": \"2024-03-27\", \"MX.43839\": \"2024-03-28\", \"MX.39425\": \"2024-03-28\", \"MX.38752\": \"2024-03-28\", \"MX.39949\": \"2024-03-28\", \"MX.40632\": \"2024-03-28\", \"MX.39883\": \"2024-03-29\", \"MX.40537\": \"2024-03-29\", \"MX.43988\": \"2024-03-29\", \"MX.43957\": \"2024-03-30\", \"MX.38253\": \"2024-03-29\", \"MX.40353\": \"2024-03-30\", \"MX.43979\": \"2024-03-30\", \"MX.38743\": \"2024-03-25\", \"MX.40373\": \"2024-03-25\", \"MX.40244\": \"2024-03-29\", \"MX.40022\": \"2024-03-30\", \"MX.38918\": \"2024-03-29\", \"MX.40751\": \"2024-03-29\", \"MX.38088\": \"2024-03-25\", \"MX.4976000\": \"2024-03-29\", \"MX.38790\": \"2024-03-26\", \"MX.39558\": \"2024-03-31\", \"MX.40854\": \"2024-03-31\", \"MX.39885\": \"2024-03-31\", \"MX.41650\": \"2024-03-31\", \"MX.38980\": \"2024-03-31\", \"MX.43612\": \"2024-03-26\", \"MX.43813\": \"2024-03-31\", \"MX.200455\": \"2024-03-31\", \"MX.43523\": \"2024-03-30\", \"MX.43500\": \"2024-03-31\", \"MX.43877\": \"2024-03-31\", \"MX.44360\": \"2024-03-31\", \"MX.43887\": \"2024-03-31\", \"MX.44180\": \"2024-03-31\", \"MX.44181\": \"2024-03-31\", \"MX.39293\": \"2024-04-01\", \"MX.38953\": \"2024-03-31\", \"MX.39984\": \"2024-04-01\", \"MX.43954\": \"2024-04-01\", \"MX.43554\": \"2024-04-01\", \"MX.43552\": \"2024-04-01\", \"MX.43827\": \"2024-04-01\", \"MX.200443\": \"2024-04-01\", \"MX.39947\": \"2024-04-01\", \"MX.39149\": \"2024-04-01\", \"MX.43484\": \"2024-04-01\", \"MX.43597\": \"2024-04-01\", \"MX.44392\": \"2024-04-01\", \"MX.44250\": \"2024-04-01\", \"MX.43804\": \"2024-04-01\", \"MX.43811\": \"2024-04-01\", \"MX.43922\": \"2024-03-31\", \"MX.43502\": \"2024-03-25\", \"MX.43983\": \"2024-03-25\", \"MX.43668\": \"2024-03-25\", \"MX.43901\": \"2024-03-25\", \"MX.43956\": \"2024-03-25\", \"MX.43803\": \"2024-03-26\", \"MX.43933\": \"2024-03-30\", \"MX.44366\": \"2024-03-28\", \"MX.44182\": \"2024-04-01\", \"MX.37691\": \"2024-04-10\", \"MX.37721\": \"2024-04-27\", \"MX.37717\": \"2024-03-29\", \"MX.37719\": \"2024-04-15\", \"MX.37763\": \"2024-05-25\", \"MX.37771\": \"2024-05-19\", \"MX.37752\": \"2024-03-25\", \"MX.37796\": \"2024-03-25\", \"MX.37826\": \"2024-03-25\", \"MX.37812\": \"2024-03-25\", \"MX.37819\": \"2024-03-25\", \"MX.40092\": \"2024-04-10\", \"MX.39201\": \"2024-04-01\", \"MX.39235\": \"2024-03-25\", \"MX.39185\": \"2024-03-29\", \"MX.39970\": \"2024-03-31\", \"MX.39976\": \"2024-05-13\", \"MX.39974\": \"2024-05-13\", \"MX.39812\": \"2024-03-25\", \"MX.39809\": \"2024-03-29\", \"MX.39761\": \"2024-04-14\", \"MX.39871\": \"2024-03-25\", \"MX.39835\": \"2024-03-25\", \"MX.39890\": \"2024-03-27\", \"MX.39887\": \"2024-04-12\", \"MX.39833\": \"2024-03-26\", \"MX.39827\": \"2024-06-16\", \"MX.39917\": \"2024-04-19\", \"MX.39727\": \"2024-03-25\", \"MX.39830\": \"2024-03-29\", \"MX.42419\": \"2024-03-26\", \"MX.39823\": \"2024-03-31\", \"MX.39847\": \"2024-03-31\", \"MX.39703\": \"2024-05-26\", \"MX.39711\": \"2024-03-30\", \"MX.39402\": \"2024-03-25\", \"MX.38364\": \"2024-03-28\", \"MX.38387\": \"2024-03-29\", \"MX.38073\": \"2024-03-28\", \"MX.38131\": \"2024-03-26\", \"MX.38055\": \"2024-05-23\", \"MX.38048\": \"2024-03-29\", \"MX.38780\": \"2024-06-05\", \"MX.38217\": \"2024-04-12\", \"MX.38279\": \"2024-04-01\", \"MX.38285\": \"2024-03-25\", \"MX.38263\": \"2024-03-25\", \"MX.39166\": \"2024-05-24\", \"MX.39336\": \"2024-03-25\", \"MX.39343\": \"2024-04-10\", \"MX.39347\": \"2024-04-05\", \"MX.39358\": \"2024-05-17\", \"MX.39158\": \"2024-05-23\", \"MX.38614\": \"2024-03-26\", \"MX.38598\": \"2024-03-25\", \"MX.38646\": \"2024-03-31\", \"MX.38634\": \"2024-04-08\", \"MX.38626\": \"2024-04-25\", \"MX.38605\": \"2024-03-27\", \"MX.38622\": \"2024-03-25\", \"MX.38618\": \"2024-04-10\", \"MX.38621\": \"2024-03-27\", \"MX.38620\": \"2024-03-25\", \"MX.38676\": \"2024-05-23\", \"MX.38670\": \"2024-03-29\", \"MX.39002\": \"2024-03-26\", \"MX.38950\": \"2024-03-25\", \"MX.39047\": \"2024-07-17\", \"MX.39052\": \"2024-03-26\", \"MX.39038\": \"2024-03-26\", \"MX.39046\": \"2024-07-17\", \"MX.38972\": \"2024-03-26\", \"MX.38008\": \"2024-03-25\", \"MX.38010\": \"2024-03-26\", \"MX.37993\": \"2024-03-25\", \"MX.37999\": \"2024-03-25\", \"MX.38016\": \"2024-03-25\", \"MX.37990\": \"2024-03-25\", \"MX.39292\": \"2024-03-26\", \"MX.39138\": \"2024-03-31\", \"MX.39493\": \"2024-03-30\", \"MX.39500\": \"2024-03-28\", \"MX.39331\": \"2024-03-25\", \"MX.39633\": \"2024-05-10\", \"MX.39663\": \"2024-07-08\", \"MX.39589\": \"2024-03-31\", \"MX.39673\": \"2024-03-26\", \"MX.39609\": \"2024-03-29\", \"MX.39608\": \"2024-03-26\", \"MX.38590\": \"2024-03-25\", \"MX.38563\": \"2024-03-25\", \"MX.38338\": \"2024-05-10\", \"MX.38331\": \"2024-05-23\", \"MX.38321\": \"2024-04-12\", \"MX.38336\": \"2024-04-12\", \"MX.38686\": \"2024-03-25\", \"MX.38715\": \"2024-04-04\", \"MX.39079\": \"2024-03-25\", \"MX.39088\": \"2024-03-26\", \"MX.39130\": \"2024-04-10\", \"MX.40258\": \"2024-05-17\", \"MX.40261\": \"2024-03-27\", \"MX.40196\": \"2024-06-08\", \"MX.40505\": \"2024-05-16\", \"MX.40639\": \"2024-03-25\", \"MX.40188\": \"2024-03-25\", \"MX.37962\": \"2024-03-28\", \"MX.37859\": \"2024-05-10\", \"MX.37879\": \"2024-04-01\", \"MX.37863\": \"2024-04-12\", \"MX.37924\": \"2024-04-11\", \"MX.37890\": \"2024-03-25\", \"MX.37897\": \"2024-04-08\", \"MX.37896\": \"2024-03-26\", \"MX.38844\": \"2024-05-15\", \"MX.38832\": \"2024-05-25\", \"MX.38795\": \"2024-03-25\", \"MX.38869\": \"2024-03-25\", \"MX.38834\": \"2024-04-09\", \"MX.38863\": \"2024-05-31\", \"MX.38939\": \"2024-03-25\", \"MX.38815\": \"2024-03-25\", \"MX.38799\": \"2024-05-31\", \"MX.38797\": \"2024-04-10\", \"MX.38804\": \"2024-03-25\", \"MX.38802\": \"2024-05-18\", \"MX.38910\": \"2024-03-25\", \"MX.37984\": \"2024-03-29\", \"MX.39122\": \"2024-03-25\", \"MX.38750\": \"2024-03-26\"}', 'MA.3', '2024-01-30 15:48:29', 'MA.3', '2024-07-17 09:07:41', 0),
(9, 4, 'Teppo Testaaja', 'Testipaikka', 7, '{\"MX.43922\": \"2024-01-01\", \"MX.43956\": \"2024-02-06\", \"MX.39976\": \"2024-02-01\", \"MX.39890\": \"2024-01-17\", \"MX.38048\": \"2024-01-17\", \"MX.38263\": \"2024-01-06\", \"MX.39158\": \"2024-01-06\"}', 'MA.315', '2024-02-05 12:02:33', 'MA.315', '2024-02-06 07:20:10', 0),
(35, 5, 'Testi Äläpoista', 'Playwright-paikka', 2, '{\"MX.43922\": \"2024-02-09\", \"MX.39687\": \"2024-02-09\"}', 'MA.3', '2024-02-09 08:23:23', 'MA.3', '2024-02-09 08:24:19', 0),
(49, 4, 'Nolla', 'Nolla', 0, '{}', 'MA.3', '2024-07-16 10:42:20', 'MA.3', '2024-07-16 10:42:20', 0),
(50, 6, 'Nolla', 'Nolla', 0, '{}', 'MA.3', '2024-07-16 10:47:50', 'MA.3', '2024-07-16 10:47:50', 0),
(51, 3, 'Testi', 'Testi', 14, '{\"MX.71663\": \"2024-07-23\", \"MX.73283\": \"2024-07-23\", \"MX.72788\": \"2024-07-23\", \"MX.72555\": \"2024-07-23\", \"MX.72358\": \"2024-07-23\", \"MX.72148\": \"2024-07-23\", \"MX.72561\": \"2024-07-23\", \"MX.69690\": \"2024-07-23\", \"MX.71822\": \"2024-07-23\", \"MX.73304\": \"2024-07-23\", \"MX.72814\": \"2024-07-23\", \"MX.73307\": \"2024-07-23\", \"MX.292558\": \"2024-07-23\", \"MX.73330\": \"2024-07-23\"}', 'MA.3', '2024-07-16 12:48:37', 'MA.3', '2024-07-23 12:52:31', 0),
(52, 4, 'Ukko Uusinen', 'Uusimaa', 3, '{\"MX.43922\": \"2024-07-01\", \"MX.43502\": \"2024-07-22\", \"MX.43983\": \"2024-07-10\"}', 'MA.3', '2024-07-22 13:17:37', 'MA.3', '2024-07-23 11:57:26', 1);

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
  MODIFY `challenge_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `participations`
--
ALTER TABLE `participations`
  MODIFY `participation_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

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
