-- Lunéa Atelier — schéma de la base + catalogue produits
-- Importer dans votre MySQL cloud :  mysql -h <host> -u <user> -p <dbname> < schema.sql


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
DROP TABLE IF EXISTS `commandes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `commandes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `utilisateur_id` int NOT NULL,
  `date_commande` datetime DEFAULT CURRENT_TIMESTAMP,
  `montant_total` decimal(10,2) NOT NULL,
  `statut` varchar(50) DEFAULT 'En attente',
  PRIMARY KEY (`id`),
  KEY `utilisateur_id` (`utilisateur_id`),
  CONSTRAINT `commandes_ibfk_1` FOREIGN KEY (`utilisateur_id`) REFERENCES `utilisateurs` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `details_commande`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `details_commande` (
  `id` int NOT NULL AUTO_INCREMENT,
  `commande_id` int NOT NULL,
  `produit_id` int NOT NULL,
  `quantite` int NOT NULL,
  `prix_unitaire` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `commande_id` (`commande_id`),
  KEY `produit_id` (`produit_id`),
  CONSTRAINT `details_commande_ibfk_1` FOREIGN KEY (`commande_id`) REFERENCES `commandes` (`id`),
  CONSTRAINT `details_commande_ibfk_2` FOREIGN KEY (`produit_id`) REFERENCES `produits` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `personnalisations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personnalisations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `detail_commande_id` int NOT NULL,
  `texte` varchar(255) DEFAULT NULL,
  `couleur` varchar(50) DEFAULT NULL,
  `taille` varchar(50) DEFAULT NULL,
  `type_perles` varchar(100) DEFAULT NULL,
  `police_ecriture` varchar(100) DEFAULT NULL,
  `couleur_texte` varchar(50) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `date_creation` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `detail_commande_id` (`detail_commande_id`),
  CONSTRAINT `personnalisations_ibfk_1` FOREIGN KEY (`detail_commande_id`) REFERENCES `details_commande` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `produits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produits` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `description` text,
  `prix` decimal(10,2) NOT NULL,
  `stock` int DEFAULT '0',
  `image` varchar(255) DEFAULT NULL,
  `categorie` varchar(100) DEFAULT NULL,
  `date_creation` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `utilisateurs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utilisateurs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `date_inscription` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;


-- Données du catalogue

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

LOCK TABLES `produits` WRITE;
/*!40000 ALTER TABLE `produits` DISABLE KEYS */;
INSERT INTO `produits` VALUES (1,'Bracelet Luna','Bracelet artisanal avec perles nacrées dorées, idéal pour graver un prénom ou un message tendre. Fil élastique résistant, finition soignée.',19.99,10,'images/luna.jpg','prenom','2026-06-30 11:36:55'),(2,'Bracelet Élégance','Bracelet chic et délicat, parfait pour offrir lors d\'un anniversaire ou d\'une occasion spéciale. Réalisé à la main avec soin.',24.99,8,'images/elegance.jpg','cadeaux','2026-06-30 11:36:55'),(3,'Bracelet Enfant','Bracelet coloré et léger, spécialement conçu pour les petits poignets. Perles douces et fil sécurisé pour les enfants.',14.99,15,'images/enfant.jpg','enfants','2026-06-30 11:36:55'),(4,'Bracelet Premium','Création raffinée avec finition dorée à l\'or fin. Un bracelet d\'exception pour les moments les plus précieux.',29.99,5,'images/premium.jpg','premium','2026-06-30 11:36:55'),(5,'Bracelet Stella','Bracelet prénom aux petites étoiles dorées, personnalisable avec le prénom de votre choix. Idéal pour un cadeau unique et lumineux.',22.90,12,'images/stella.jpg','prenom','2026-07-03 16:11:18'),(6,'Bracelet Rose','Bracelet romantique avec perles roses pastel et breloque en forme de fleur. Entièrement fait main avec des matériaux hypoallergéniques.',18.50,9,'images/rose.jpg','prenom','2026-07-03 16:11:18'),(7,'Bracelet Amour','Bracelet de couple avec charm cœur en argent, symbole d\'un amour durable. Livré dans un joli écrin cadeau.',26.90,7,'images/amour.jpg','cadeaux','2026-07-03 16:11:18'),(8,'Bracelet Étoile Enfant','Bracelet enfant avec étoiles multicolores, ajustable et ultra-léger. Parfait pour égayer le quotidien des petits aventuriers.',12.90,20,'images/etoile.jpg','enfants','2026-07-03 16:11:18'),(9,'Bracelet Cristal Premium','Bracelet de luxe orné de cristaux Swarovski et d\'une chaîne plaquée or 18 carats. La définition du raffinement fait main.',39.90,4,'images/cristal.jpg','premium','2026-07-03 16:11:18');
/*!40000 ALTER TABLE `produits` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

