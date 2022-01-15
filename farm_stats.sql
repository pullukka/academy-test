-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 192.168.1.214
-- Generation Time: Jan 15, 2022 at 06:29 PM
-- Server version: 10.3.32-MariaDB-0ubuntu0.20.04.1
-- PHP Version: 7.4.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `farm_stats`
--

-- --------------------------------------------------------

--
-- Table structure for table `metrics`
--

CREATE TABLE `metrics` (
  `id` int(11) NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  `sensorType` varchar(12) DEFAULT NULL,
  `value` float DEFAULT NULL,
  `fetchdate` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `metrics`
--
ALTER TABLE `metrics`
  ADD PRIMARY KEY (`id`),
  ADD KEY `location` (`location`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `metrics`
--
ALTER TABLE `metrics`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
