-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: yolo
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `avistaments`
--

DROP TABLE IF EXISTS `avistaments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `avistaments` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `IDVideo` int NOT NULL,
  `IDEspecie` int DEFAULT NULL,
  `fecha_aparicion` datetime NOT NULL,
  `fecha_desaparicion` datetime DEFAULT NULL,
  `inicio_video_segons` int DEFAULT NULL,
  `final_video_segons` int DEFAULT NULL,
  `es_audio` tinyint(1) DEFAULT '0',
  `confianza` float DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `IDEspecie` (`IDEspecie`),
  KEY `fecha_aparicion` (`fecha_aparicion`),
  KEY `IDVideo` (`IDVideo`),
  CONSTRAINT `avistaments_ibfk_1` FOREIGN KEY (`IDVideo`) REFERENCES `video` (`ID`),
  CONSTRAINT `avistaments_ibfk_2` FOREIGN KEY (`IDEspecie`) REFERENCES `especie` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=551 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `avistaments`
--

LOCK TABLES `avistaments` WRITE;
/*!40000 ALTER TABLE `avistaments` DISABLE KEYS */;
INSERT INTO `avistaments` VALUES (550,85,0,'2025-10-27 18:58:37','2025-10-27 19:00:06',68,157,0,0);
/*!40000 ALTER TABLE `avistaments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `camara`
--

DROP TABLE IF EXISTS `camara`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `camara` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `IDUsuario` int DEFAULT NULL,
  `Nombre` varchar(100) NOT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `pais` varchar(100) DEFAULT NULL,
  `latitud` decimal(10,6) DEFAULT NULL,
  `longitud` decimal(10,6) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `IDUsuario` (`IDUsuario`,`Nombre`),
  CONSTRAINT `camara_ibfk_1` FOREIGN KEY (`IDUsuario`) REFERENCES `usuario` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camara`
--

LOCK TABLES `camara` WRITE;
/*!40000 ALTER TABLE `camara` DISABLE KEYS */;
INSERT INTO `camara` VALUES (1,2,'Garden','Barcelona','España',1233.900000,-545.600000);
/*!40000 ALTER TABLE `camara` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `especie`
--

DROP TABLE IF EXISTS `especie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `especie` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `nom_cientific` varchar(100) NOT NULL,
  `nom_comu` varchar(100) DEFAULT NULL,
  `familia` varchar(100) DEFAULT NULL,
  `foto` text,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `nom_cientific` (`nom_cientific`)
) ENGINE=InnoDB AUTO_INCREMENT=1448 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `especie`
--

LOCK TABLES `especie` WRITE;
/*!40000 ALTER TABLE `especie` DISABLE KEYS */;
INSERT INTO `especie` VALUES (0,'???','Ocell desconegut',NULL,NULL),(989,'Merops apiaster','Abellerol comú',NULL,NULL),(990,'Merops persicus','Abellerol de Pèrsia',NULL,NULL),(991,'Ardea alba','Agró blanc',NULL,NULL),(992,'Ardea purpurea','Agró roig',NULL,NULL),(993,'Buteo lagopus','Aligot calçat',NULL,NULL),(994,'Buteo buteo','Aligot comú',NULL,NULL),(995,'Buteo rufinus','Aligot rogenc',NULL,NULL),(996,'Pernis apivorus','Aligot vesper europeu',NULL,NULL),(997,'Eremophila alpestris','Alosa banyuda',NULL,NULL),(998,'Chersophilus duponti','Alosa becuda',NULL,NULL),(999,'Alauda arvensis','Alosa eurasiàtica',NULL,NULL),(1000,'Psittacara mitrata','Aratinga mitrada',NULL,NULL),(1001,'Circus pygargus','Arpella cendrosa',NULL,NULL),(1002,'Circus aeruginosus','Arpella comuna',NULL,NULL),(1003,'Circus cyaneus','Arpella pàl·lida comuna',NULL,NULL),(1004,'Circus macrourus','Arpella pàl·lida russa',NULL,NULL),(1005,'Astur gentilis','Astor comú',NULL,NULL),(1006,'Neophron percnopterus','Aufrany comú',NULL,NULL),(1007,'Puffinus mauretanicus','Baldriga balear',NULL,NULL),(1008,'Puffinus gravis','Baldriga capnegra',NULL,NULL),(1009,'Calonectris diomedea','Baldriga cendrosa atlàntica',NULL,NULL),(1010,'Calonectris diomedea ','Baldriga cendrosa mediterrània',NULL,NULL),(1011,'Ardenna grisea','Baldriga grisa',NULL,NULL),(1012,'Puffinus yelkouan','Baldriga mediterrània',NULL,NULL),(1013,'Tachymarptis melba','Ballester comú',NULL,NULL),(1014,'Acrocephalus arundinaceus','Balquer',NULL,NULL),(1015,'Calidris pugnax','Batallaire',NULL,NULL),(1016,'Recurvirostra avosetta','Bec d\'alena comú',NULL,NULL),(1017,'Estrilda troglodytes','Bec de coral cuanegre',NULL,NULL),(1018,'Estrilda astrild','Bec de coral del Senegal',NULL,NULL),(1019,'Mergus merganser','Bec de serra gros',NULL,NULL),(1020,'Mergus serrator','Bec de serra mitjà',NULL,NULL),(1021,'Mergellus albellus','Bec de serra petit',NULL,NULL),(1022,'Scolopax rusticola','Becada eurasiàtica',NULL,NULL),(1023,'Gallinago gallinago','Becadell comú',NULL,NULL),(1024,'Gallinago media','Becadell gros',NULL,NULL),(1025,'Lymnocryptes minimus','Becadell sord',NULL,NULL),(1026,'Platalea leucorodia','Becplaner comú',NULL,NULL),(1027,'Numenius arquata','Becut eurasiàtic',NULL,NULL),(1028,'Ardea cinerea','Bernat pescaire',NULL,NULL),(1029,'Saxicola rubicola','Bitxac comú',NULL,NULL),(1030,'Saxicola rubetra','Bitxac rogenc',NULL,NULL),(1031,'Saxicola maurus','Bitxac siberià',NULL,NULL),(1032,'Botaurus stellaris','Bitó comú',NULL,NULL),(1033,'Botaurus lentiginosus','Bitó nord-americà',NULL,NULL),(1034,'Alcedo atthis ispida','Blauet comú',NULL,NULL),(1035,'Locustella luscinioides','Boscaler comú',NULL,NULL),(1036,'Locustella naevia','Boscaler pintat gros',NULL,NULL),(1037,'Acrocephalus paludicola','Boscarla d\'aigua',NULL,NULL),(1038,'Acrocephalus agricola','Boscarla d\'arrossar',NULL,NULL),(1039,'Acrocephalus scirpaceus','Boscarla de canyar',NULL,NULL),(1040,'Acrocephalus schoenobaenus','Boscarla dels joncs',NULL,NULL),(1041,'Acrocephalus dumetorum','Boscarla dels matolls',NULL,NULL),(1042,'Acrocephalus palustris','Boscarla menjamosquits',NULL,NULL),(1043,'Acrocephalus melanopogon','Boscarla mostatxuda',NULL,NULL),(1044,'Mniotilta varia','Bosquerola zebrada',NULL,NULL),(1045,'Lanius meridionalis','Botxí ibèric',NULL,NULL),(1046,'Lanius excubitor','Botxí septentrional',NULL,NULL),(1047,'Regulus ignicapilla','Bruel eurasiàtic',NULL,NULL),(1048,'Iduna opaca','Busqueta bruna',NULL,NULL),(1049,'Hippolais polyglotta','Busqueta comuna',NULL,NULL),(1050,'Hippolais icterina','Busqueta icterina',NULL,NULL),(1051,'Tachybaptus ruficollis','Cabusset comú',NULL,NULL),(1052,'Podiceps nigricollis','Cabussó collnegre',NULL,NULL),(1053,'Podiceps cristatus','Cabussó emplomallat',NULL,NULL),(1054,'Podiceps grisegena','Cabussó gris',NULL,NULL),(1055,'Podiceps auritus','Cabussó orellut',NULL,NULL),(1056,'Carduelis carduelis','Cadernera europea',NULL,NULL),(1057,'Gavia arctica','Calàbria agulla',NULL,NULL),(1058,'Gavia immer','Calàbria grossa',NULL,NULL),(1059,'Gavia stellata','Calàbria petita',NULL,NULL),(1060,'Melanocorypha calandra','Calàndria comuna',NULL,NULL),(1061,'Himantopus himantopus','Camallarga comú',NULL,NULL),(1062,'Lanius cristatus','Capsigrany bru',NULL,NULL),(1063,'Lanius senator','Capsigrany comú',NULL,NULL),(1064,'Lanius isabellinus','Capsigrany pàl·lid',NULL,NULL),(1065,'Plegadis falcinellus','Capó reial',NULL,NULL),(1066,'Troglodytes troglodytes','Cargolet eurasiàtic',NULL,NULL),(1067,'Prunella collaris','Cercavores alpí',NULL,NULL),(1068,'Cygnus cygnus','Cigne cantaire',NULL,NULL),(1069,'Cygnus olor','Cigne mut',NULL,NULL),(1070,'Cygnus atratus','Cigne negre',NULL,NULL),(1071,'Cygnus columbianus','Cigne petit',NULL,NULL),(1072,'Ciconia ciconia','Cigonya blanca',NULL,NULL),(1073,'Ciconia nigra','Cigonya negra',NULL,NULL),(1074,'Galerida cristata','Cogullada comuna',NULL,NULL),(1075,'Galerida theklae','Cogullada fosca',NULL,NULL),(1076,'Jynx torquilla','Colltort comú',NULL,NULL),(1077,'Columba livia','Colom roquer',NULL,NULL),(1078,'Corvus corax','Corb comú',NULL,NULL),(1079,'Gulosus aristotelis','Corb marí emplomallat',NULL,NULL),(1080,'Phalacrocorax carbo','Corb marí gros',NULL,NULL),(1081,'Microcarbo pigmeus','Corb marí pigmeu',NULL,NULL),(1082,'Corvus cornix','Cornella emmantellada',NULL,NULL),(1083,'Corvus corone','Cornella negra',NULL,NULL),(1084,'Cursorius cursor','Corredor del desert',NULL,NULL),(1085,'Anarhynchus alexandrinus','Corriol camanegre',NULL,NULL),(1086,'Anarhynchus leschenaultii','Corriol de Leschenault',NULL,NULL),(1087,'Charadrius hiaticula','Corriol gros',NULL,NULL),(1088,'Charadrius dubius','Corriol petit',NULL,NULL),(1089,'Charadrius morinellus','Corriol pit-roig',NULL,NULL),(1090,'Lullula arborea','Cotoliu',NULL,NULL),(1091,'Psittacula krameri','Cotorra de Kramer',NULL,NULL),(1092,'Myiopsitta monachus','Cotorreta pitgrisa',NULL,NULL),(1093,'Luscinia svecica','Cotxa blava',NULL,NULL),(1094,'Phoenicurus phoenicurus','Cotxa cua-roja',NULL,NULL),(1095,'Tarsiger cyanurus','Cotxa cuablava',NULL,NULL),(1096,'Phoenicurus moussieri','Cotxa diademada',NULL,NULL),(1097,'Phoenicurus ochruros','Cotxa fumada',NULL,NULL),(1098,'Emberiza calandra','Cruixidell',NULL,NULL),(1099,'Cercotrichas galactotes','Cuaenlairat rogenc',NULL,NULL),(1100,'Cuculus canorus','Cucut comú',NULL,NULL),(1101,'Clamator glandarius','Cucut reial europeu',NULL,NULL),(1102,'Motacilla alba','Cuereta blanca',NULL,NULL),(1103,'Motacilla citreola','Cuereta citrina',NULL,NULL),(1104,'Motacilla tschutschensis','Cuereta de Txukotka',NULL,NULL),(1105,'Motacilla flava','Cuereta groga',NULL,NULL),(1106,'Motacilla cinerea','Cuereta torrentera',NULL,NULL),(1107,'Sterna nilotica','Curroc comú',NULL,NULL),(1108,'Oenanthe deserti','Còlit del desert',NULL,NULL),(1109,'Oenanthe oenanthe','Còlit gris',NULL,NULL),(1110,'Oenanthe leucura','Còlit negre',NULL,NULL),(1111,'Oenanthe isabellina','Còlit pàl·lid',NULL,NULL),(1112,'Oenanthe hispanica','Còlit ros occidental',NULL,NULL),(1113,'Pluvialis dominica','Daurada americana',NULL,NULL),(1114,'Pluvialis fulva','Daurada del Pacífic',NULL,NULL),(1115,'Pluvialis apricaria','Daurada grossa',NULL,NULL),(1116,'Bubo bubo','Duc eurasiàtic',NULL,NULL),(1117,'Coccothraustes coccothraustes','Durbec comú',NULL,NULL),(1118,'Elanus caeruleus','Elani comú',NULL,NULL),(1119,'Caprimulgus europaeus','Enganyapastors europeu',NULL,NULL),(1120,'Lanius collurio','Escorxador comú',NULL,NULL),(1121,'Phalaropus lobatus','Escuraflascons becfí',NULL,NULL),(1122,'Phalaropus fulicarius','Escuraflascons becgròs',NULL,NULL),(1123,'Phalaropus tricolor','Escuraflascons de Wilson',NULL,NULL),(1124,'Falco columbarius','Esmirla',NULL,NULL),(1125,'Accipiter nisus','Esparver comú',NULL,NULL),(1126,'Ardea ibis','Esplugabous',NULL,NULL),(1127,'Sturnus vulgaris','Estornell comú',NULL,NULL),(1128,'Sturnus unicolor','Estornell negre',NULL,NULL),(1129,'Pastor roseus','Estornell rosat',NULL,NULL),(1130,'Phasianus colchicus','Faisà comú',NULL,NULL),(1131,'Apus affinis','Falciot cuablanc petit',NULL,NULL),(1132,'Apus apus','Falciot negre',NULL,NULL),(1133,'Apus pallidus','Falciot pàl·lid',NULL,NULL),(1134,'Falco vespertinus','Falcó cama-roig',NULL,NULL),(1135,'Falco eleonorae','Falcó d\'Elionor',NULL,NULL),(1136,'Falco biarmicus','Falcó llaner',NULL,NULL),(1137,'Falco subbuteo','Falcó mostatxut europeu',NULL,NULL),(1138,'Falco peregrinus','Falcó pelegrí',NULL,NULL),(1139,'Falco cherrug','Falcó sacre',NULL,NULL),(1140,'Phoenicopterus minor','Flamenc menut',NULL,NULL),(1141,'Phoenicopterus roseus','Flamenc rosat',NULL,NULL),(1142,'Fulica cristata','Fotja banyuda',NULL,NULL),(1143,'Fulica atra','Fotja comuna',NULL,NULL),(1144,'Fratercula arctica','Fraret atlàntic',NULL,NULL),(1145,'Vanellus leucurus','Fredeluga cuablanca',NULL,NULL),(1146,'Vanellus vanellus','Fredeluga europea',NULL,NULL),(1147,'Vanellus gregarius','Fredeluga gregària',NULL,NULL),(1148,'Chlidonias leucopterus','Fumarell alablanc',NULL,NULL),(1149,'Chlidonias hybridus','Fumarell carablanc',NULL,NULL),(1150,'Chlidonias niger','Fumarell negre',NULL,NULL),(1151,'Serinus serinus','Gafarró europeu',NULL,NULL),(1152,'Coracias garrulus','Gaig blau comú',NULL,NULL),(1153,'Garrulus glandarius','Gaig eurasiàtic',NULL,NULL),(1154,'Tetrao urogallus','Gall fer comú',NULL,NULL),(1155,'Strix aluco','Gamarús eurasiàtic',NULL,NULL),(1156,'Tringa flavipes','Gamba groga petita',NULL,NULL),(1157,'Tringa totanus','Gamba roja comuna',NULL,NULL),(1158,'Tringa erythropus','Gamba roja pintada',NULL,NULL),(1159,'Tringa nebularia','Gamba verda',NULL,NULL),(1160,'Pterocles alchata','Ganga eurasiàtica',NULL,NULL),(1161,'Haematopus ostralegus','Garsa de mar eurasiàtica',NULL,NULL),(1162,'Pica pica','Garsa eurasiàtica',NULL,NULL),(1163,'Chroicocephalus genei','Gavina capblanca',NULL,NULL),(1164,'Larus atricilla','Gavina capnegra americana',NULL,NULL),(1165,'Ichthyaetus melanocephalus','Gavina capnegra mediterrània',NULL,NULL),(1166,'Larus canus','Gavina cendrosa',NULL,NULL),(1167,'Ichthyaetus audouinii','Gavina corsa',NULL,NULL),(1168,'Chroicocephalus philadelphia','Gavina de Bonaparte',NULL,NULL),(1169,'Larus delawarensis','Gavina de Delaware',NULL,NULL),(1170,'Larus pipixcan','Gavina de Franklin',NULL,NULL),(1171,'Hydrocoloeus minutus','Gavina menuda',NULL,NULL),(1172,'Chroicocephalus ridibundus','Gavina riallera',NULL,NULL),(1173,'Xema sabini','Gavineta cuaforcada',NULL,NULL),(1174,'Rissa tridactyla','Gavineta de tres dits',NULL,NULL),(1175,'Larus marinus','Gavinot atlàntic',NULL,NULL),(1176,'Larus glaucoides','Gavinot polar',NULL,NULL),(1177,'Larus argentatus','Gavià argentat de potes roses',NULL,NULL),(1178,'Larus cachinnans','Gavià caspi',NULL,NULL),(1179,'Larus michahellis','Gavià de potes grogues',NULL,NULL),(1180,'Larus fuscus','Gavià fosc',NULL,NULL),(1181,'Alca torda','Gavot',NULL,NULL),(1182,'Pyrrhocorax graculus','Gralla becgroga',NULL,NULL),(1183,'Pyrrhocorax pyrrhocorax','Gralla becvermella',NULL,NULL),(1184,'Coloeus monedula','Gralla occidental',NULL,NULL),(1185,'Anthus petrosus','Grasset de costa',NULL,NULL),(1186,'Anthus spinoletta','Grasset de muntanya',NULL,NULL),(1187,'Emberiza cirlus','Gratapalles',NULL,NULL),(1188,'Corvus frugilegus','Graula',NULL,NULL),(1189,'Turdus pilaris','Griva cerdana',NULL,NULL),(1190,'Turdus viscivorus','Griva comuna',NULL,NULL),(1191,'Grus grus','Grua europea',NULL,NULL),(1192,'Tetrastes bonasia','Grèvol comú',NULL,NULL),(1193,'Coturnix coturnix','Guatlla comuna',NULL,NULL),(1194,'Crex crex','Guatlla maresa eurasiàtica',NULL,NULL),(1195,'Emberiza hortulana','Hortolà comú',NULL,NULL),(1196,'Threskiornis aethiopicus','Ibis sagrat africà',NULL,NULL),(1197,'Junco hyemalis','Junco fosc',NULL,NULL),(1198,'Leiothrix lutea','Leiòtrix bec-roig',NULL,NULL),(1199,'Carduelis citrinella','Llucareta europea',NULL,NULL),(1200,'Spinus spinus','Lluer eurasiàtic',NULL,NULL),(1201,'Cyanistes caeruleus','Mallerenga blava eurasiàtica',NULL,NULL),(1202,'Parus major','Mallerenga carbonera',NULL,NULL),(1203,'Aegithalos caudatus','Mallerenga cuallarga eurasiàtica',NULL,NULL),(1204,'Poecile palustris','Mallerenga d\'aigua',NULL,NULL),(1205,'Panurus biarmicus','Mallerenga de bigotis',NULL,NULL),(1206,'Lophophanes cristatus','Mallerenga emplomallada europea',NULL,NULL),(1207,'Periparus ater','Mallerenga petita',NULL,NULL),(1208,'Oxyura leucocephala','Malvasia capblanca',NULL,NULL),(1209,'Oxyura jamaicensis','Malvasia de Jamaica',NULL,NULL),(1210,'Egretta garzetta','Martinet blanc comú',NULL,NULL),(1211,'Nycticorax nycticorax','Martinet de nit comú',NULL,NULL),(1212,'Egretta gularis','Martinet dels esculls',NULL,NULL),(1213,'Botaurus minutus','Martinet menut comú',NULL,NULL),(1214,'Ardeola ralloides','Martinet ros comú',NULL,NULL),(1215,'Morus bassanus','Mascarell atlàntic',NULL,NULL),(1216,'Sula leucogaster','Mascarell bru',NULL,NULL),(1217,'Sula sula','Mascarell cama-roig',NULL,NULL),(1218,'Ficedula hypoleuca','Mastegatatxes',NULL,NULL),(1219,'Monticola solitarius','Merla blava',NULL,NULL),(1220,'Turdus merula','Merla comuna',NULL,NULL),(1221,'Cinclus cinclus','Merla d\'aigua europea',NULL,NULL),(1222,'Turdus torquatus','Merla de pit blanc',NULL,NULL),(1223,'Monticola saxatilis','Merla roquera comuna',NULL,NULL),(1224,'Milvus migrans','Milà negre',NULL,NULL),(1225,'Milvus milvus','Milà reial',NULL,NULL),(1226,'Aythya marila','Morell buixot',NULL,NULL),(1227,'Aythya ferina','Morell cap-roig',NULL,NULL),(1228,'Bucephala clangula','Morell d\'ulls grocs',NULL,NULL),(1229,'Aythya collaris','Morell de collar',NULL,NULL),(1230,'Aythya fuligula','Morell de plomall',NULL,NULL),(1231,'Aythya affinis','Morell menut',NULL,NULL),(1232,'Aythya nyroca','Morell xocolater',NULL,NULL),(1233,'Phylloscopus borealis','Mosquiter boreal',NULL,NULL),(1234,'Phylloscopus collybita','Mosquiter comú',NULL,NULL),(1235,'Phylloscopus humei','Mosquiter de Hume',NULL,NULL),(1236,'Phylloscopus inornatus','Mosquiter de doble ratlla',NULL,NULL),(1237,'Phylloscopus trochilus','Mosquiter de passa',NULL,NULL),(1238,'Phylloscopus fuscatus','Mosquiter fosc',NULL,NULL),(1239,'Phylloscopus ibericus','Mosquiter ibèric',NULL,NULL),(1240,'Phylloscopus bonelli','Mosquiter pàl·lid occidental',NULL,NULL),(1241,'Phylloscopus proregulus','Mosquiter reietó',NULL,NULL),(1242,'Phylloscopus trochiloides','Mosquiter verdós',NULL,NULL),(1243,'Phylloscopus sibilatrix','Mosquiter xiulaire',NULL,NULL),(1244,'Asio otus','Mussol banyut',NULL,NULL),(1245,'Athene noctua','Mussol comú',NULL,NULL),(1246,'Asio flammeus','Mussol emigrant',NULL,NULL),(1247,'Aegolius funereus','Mussol pirinenc',NULL,NULL),(1248,'Glaucidium passerinum','Mussolet eurasiàtic',NULL,NULL),(1249,'Anser anser','Oca comuna',NULL,NULL),(1250,'Alopochen aegyptiacus','Oca d\'Egipte',NULL,NULL),(1251,'Anser brachyrhynchus','Oca de bec curt',NULL,NULL),(1252,'Branta bernicla','Oca de collar',NULL,NULL),(1253,'Branta leucopsis','Oca de galta blanca',NULL,NULL),(1254,'Branta canadensis','Oca del Canadà',NULL,NULL),(1255,'Anser fabalis','Oca pradenca de taigà',NULL,NULL),(1256,'Anser fabalis ','Oca pradenca de tundra',NULL,NULL),(1257,'Anser albifrons','Oca riallera grossa',NULL,NULL),(1258,'Hydrobates leucorhous','Ocell de tempesta de Leach',NULL,NULL),(1259,'Hydrobates pelagicus','Ocell de tempesta europeu',NULL,NULL),(1260,'Hydrobates leucorhous ','Ocell de tempesta oceànic',NULL,NULL),(1261,'Bombycilla garrulus','Ocell sedós europeu',NULL,NULL),(1262,'Hirundo rustica','Oreneta comuna',NULL,NULL),(1263,'Cecropis rufula','Oreneta cua-rogenca',NULL,NULL),(1264,'Delichon urbicum','Oreneta cuablanca comuna',NULL,NULL),(1265,'Riparia riparia','Oreneta de ribera comuna',NULL,NULL),(1266,'Oriolus oriolus','Oriol eurasiàtic',NULL,NULL),(1267,'Ficedula albicollis','Papamosques de collar',NULL,NULL),(1268,'Muscicapa striata','Papamosques gris',NULL,NULL),(1269,'Muscicapa striata ','Papamosques mediterrani',NULL,NULL),(1270,'Ficedula parva','Papamosques menut',NULL,NULL),(1271,'Passer domesticus','Pardal comú',NULL,NULL),(1272,'Montifringilla nivalis','Pardal d\'ala blanca',NULL,NULL),(1273,'Prunella modularis','Pardal de bardissa europeu',NULL,NULL),(1274,'Passer hispaniolensis','Pardal de passa',NULL,NULL),(1275,'Petronia petronia','Pardal roquer',NULL,NULL),(1276,'Passer montanus','Pardal xarrec',NULL,NULL),(1277,'Stercorarius pomarinus','Paràsit cuaample',NULL,NULL),(1278,'Stercorarius longicaudus','Paràsit cuallarg',NULL,NULL),(1279,'Stercorarius parasiticus','Paràsit cuapunxegut',NULL,NULL),(1280,'Stercorarius skua','Paràsit gros boreal',NULL,NULL),(1281,'Linaria cannabina','Passerell eurasiàtic',NULL,NULL),(1282,'Acanthis flammea','Passerell gorjanegre',NULL,NULL),(1283,'Tichodroma muraria','Pela-roques',NULL,NULL),(1284,'Pelecanus onocrotalus','Pelicà blanc comú',NULL,NULL),(1285,'Lagopus muta','Perdiu blanca',NULL,NULL),(1286,'Glareola pratincola','Perdiu de mar europea',NULL,NULL),(1287,'Alectoris rufa','Perdiu roja',NULL,NULL),(1288,'Perdix perdix','Perdiu xerra',NULL,NULL),(1289,'Sitta europaea','Pica-soques eurasiàtic',NULL,NULL),(1290,'Dendrocopos major','Picot garser gros',NULL,NULL),(1291,'Leiopicus medius','Picot garser mitjà',NULL,NULL),(1292,'Dendrocopos minor','Picot garser petit',NULL,NULL),(1293,'Dryocopus martius','Picot negre eurasiàtic',NULL,NULL),(1294,'Picus viridis','Picot verd comú',NULL,NULL),(1295,'Picus sharpei','Picot verd ibèric',NULL,NULL),(1296,'Haliaeetus albicilla','Pigarg cuablanc',NULL,NULL),(1297,'Pluvialis squatarola','Pigre gris',NULL,NULL),(1298,'Pyrrhula pyrrhula','Pinsà borroner eurasiàtic',NULL,NULL),(1299,'Carpodacus erythrinus','Pinsà carminat',NULL,NULL),(1300,'Fringilla coelebs','Pinsà comú',NULL,NULL),(1301,'Fringilla montifringilla','Pinsà mec',NULL,NULL),(1302,'Bucanetes githagineus','Pinsà trompeter',NULL,NULL),(1303,'Otis tarda','Pioc salvatge eurasiàtic',NULL,NULL),(1304,'Erithacus rubecula','Pit-roig',NULL,NULL),(1305,'Anthus hodgsoni','Piula de Hodgson',NULL,NULL),(1306,'Anthus trivialis','Piula dels arbres',NULL,NULL),(1307,'Anthus cervinus','Piula gorja-roja',NULL,NULL),(1308,'Anthus richardi','Piula grossa',NULL,NULL),(1309,'Numenius phaeopus','Polit cantaire',NULL,NULL),(1310,'Porphyrio porphyrio','Polla blava comuna',NULL,NULL),(1311,'Porphyrio alleni','Polla blava d\'Allen',NULL,NULL),(1312,'Gallinula chloropus','Polla d\'aigua comuna',NULL,NULL),(1313,'Paragallinula angulata','Polla menuda',NULL,NULL),(1314,'Porzana porzana','Polla pintada',NULL,NULL),(1315,'Upupa epops','Puput comuna',NULL,NULL),(1316,'Zapornia pusilla','Rasclet europeu',NULL,NULL),(1317,'Zapornia parva','Rascletó',NULL,NULL),(1318,'Rallus aquaticus','Rascló occidental',NULL,NULL),(1319,'Certhia brachydactyla','Raspinell comú',NULL,NULL),(1320,'Certhia familiaris','Raspinell pirinenc',NULL,NULL),(1321,'Regulus regulus','Reietó eurasiàtic',NULL,NULL),(1322,'Arenaria interpres','Remena-rocs comú',NULL,NULL),(1323,'Calcarius lapponicus','Repicatalons de Lapònia',NULL,NULL),(1324,'Emberiza schoeniclus','Repicatalons eurasiàtic',NULL,NULL),(1325,'Emberiza pusilla','Repicatalons petit',NULL,NULL),(1326,'Emberiza rustica','Repicatalons rústic',NULL,NULL),(1327,'Ptyonoprogne rupestris','Roquerol eurasiàtic',NULL,NULL),(1328,'Larvivora cyane','Rossinyol blau',NULL,NULL),(1329,'Cettia cetti','Rossinyol bord comú',NULL,NULL),(1330,'Luscinia megarhynchos','Rossinyol comú',NULL,NULL),(1331,'Caprimulgus ruficollis','Siboc',NULL,NULL),(1332,'Xenus cinereus','Siseta cendrosa',NULL,NULL),(1333,'Tringa stagnatilis','Siseta comuna',NULL,NULL),(1334,'Tetrax tetrax','Sisó comú',NULL,NULL),(1335,'Plectrophenax nivalis','Sit blanc',NULL,NULL),(1336,'Emberiza leucocephalos','Sit capblanc',NULL,NULL),(1337,'Emberiza melanocephala','Sit capnegre',NULL,NULL),(1338,'Zonotrichia albicollis','Sit gorjablanc',NULL,NULL),(1339,'Emberiza cia','Sit negre',NULL,NULL),(1340,'Uria aalge','Somorgollaire comú',NULL,NULL),(1341,'Curruca communis','Tallareta comuna',NULL,NULL),(1342,'Curruca undata','Tallareta cuallarga',NULL,NULL),(1343,'Curruca sarda','Tallareta sarda',NULL,NULL),(1344,'Curruca melanocephala','Tallarol capnegre',NULL,NULL),(1345,'Curruca subalpina','Tallarol de Moltoni',NULL,NULL),(1346,'Sylvia atricapilla','Tallarol de casquet',NULL,NULL),(1347,'Curruca iberiae','Tallarol de garriga occidental',NULL,NULL),(1348,'Curruca cantillans','Tallarol de garriga oriental',NULL,NULL),(1349,'Curruca hortensis','Tallarol emmascarat occidental',NULL,NULL),(1350,'Sylvia borin','Tallarol gros',NULL,NULL),(1351,'Curruca conspicillata','Tallarol trencamates',NULL,NULL),(1352,'Curruca curruca','Tallarol xerraire',NULL,NULL),(1353,'Remiz pendulinus','Teixidor eurasiàtic',NULL,NULL),(1354,'Calandrella brachydactyla','Terrerola comuna',NULL,NULL),(1355,'Ammomanes cinctura','Terrerola cuabarrada',NULL,NULL),(1356,'Alaudala rufescens','Terrerola rogenca mediterrània',NULL,NULL),(1357,'Calidris falcinellus','Territ becadell',NULL,NULL),(1358,'Calidris ferruginea','Territ becllarg',NULL,NULL),(1359,'Calidris himantopus','Territ camallarg',NULL,NULL),(1360,'Calidris fuscicollis','Territ cuablanc',NULL,NULL),(1361,'Calidris bairdii','Territ de Baird',NULL,NULL),(1362,'Calidris temminckii','Territ de Temminck',NULL,NULL),(1363,'Calidris alba','Territ de tres dits',NULL,NULL),(1364,'Calidris maritima','Territ fosc',NULL,NULL),(1365,'Calidris canutus','Territ gros',NULL,NULL),(1366,'Calidris minuta','Territ menut comú',NULL,NULL),(1367,'Calidris minutilla','Territ menut del Canadà',NULL,NULL),(1368,'Calidris melanotos','Territ pectoral',NULL,NULL),(1369,'Calidris subruficollis','Territ rogenc',NULL,NULL),(1370,'Calidris alpina','Territ variant',NULL,NULL),(1371,'Limnodromus scolopaceus','Tetolet becllarg',NULL,NULL),(1372,'Limnodromus griseus','Tetolet gris',NULL,NULL),(1373,'Anthus pratensis','Titella',NULL,NULL),(1374,'Turdus iliacus','Tord ala-roig',NULL,NULL),(1375,'Turdus philomelos','Tord comú',NULL,NULL),(1376,'Turdus naumanni','Tord de Naumann',NULL,NULL),(1377,'Burhinus oedicnemus','Torlit comú',NULL,NULL),(1378,'Lanius minor','Trenca',NULL,NULL),(1379,'Gypaetus barbatus','Trencalòs',NULL,NULL),(1380,'Nucifraga caryocatactes','Trencanous eurasiàtic',NULL,NULL),(1381,'Loxia curvirostra','Trencapinyes comú',NULL,NULL),(1382,'Cisticola juncidis','Trist',NULL,NULL),(1383,'Anthus campestris','Trobat',NULL,NULL),(1384,'Columba palumbus','Tudó',NULL,NULL),(1385,'Limosa lapponica','Tètol cuabarrat',NULL,NULL),(1386,'Limosa limosa','Tètol cuanegre',NULL,NULL),(1387,'Spilopelia senegalensis','Tórtora del Senegal',NULL,NULL),(1388,'Streptopelia turtur','Tórtora eurasiàtica',NULL,NULL),(1389,'Streptopelia decaocto','Tórtora turca',NULL,NULL),(1390,'Tringa glareola','Valona',NULL,NULL),(1391,'Emberiza citrinella','Verderola',NULL,NULL),(1392,'Chloris chloris','Verdum europeu',NULL,NULL),(1393,'Vireo olivaceus','Vireó ullvermell',NULL,NULL),(1394,'Gyps fulvus','Voltor comú',NULL,NULL),(1395,'Gyps rueppellii','Voltor de Rüppell',NULL,NULL),(1396,'Aegypius monachus','Voltor negre',NULL,NULL),(1397,'Spatula querquedula','Xarrasclet',NULL,NULL),(1398,'Anas discors','Xarxet alablau',NULL,NULL),(1399,'Anas carolinensis','Xarxet americà',NULL,NULL),(1400,'Anas crecca','Xarxet comú',NULL,NULL),(1401,'Marmaronetta angustirostris','Xarxet marbrenc',NULL,NULL),(1402,'Thalasseus sandvicensis','Xatrac becllarg',NULL,NULL),(1403,'Thalasseus bengalensis','Xatrac bengalí',NULL,NULL),(1404,'Sterna hirundo','Xatrac comú',NULL,NULL),(1405,'Thalasseus elegans','Xatrac elegant',NULL,NULL),(1406,'Onychoprion anaethetus','Xatrac embridat',NULL,NULL),(1407,'Hydroprogne caspia','Xatrac gros',NULL,NULL),(1408,'Sternula albifrons','Xatrac menut comú',NULL,NULL),(1409,'Thalasseus albididorsalis','Xatrac reial africà',NULL,NULL),(1410,'Thalasseus maximus','Xatrac reial americà',NULL,NULL),(1411,'Sterna dougallii','Xatrac rosat',NULL,NULL),(1412,'Sterna paradisaea','Xatrac àrtic',NULL,NULL),(1413,'Netta rufina','Xibec cap-roig',NULL,NULL),(1414,'Tringa ochropus','Xivita comuna',NULL,NULL),(1415,'Actitis hypoleucos','Xivitona comuna',NULL,NULL),(1416,'Actitis macularia','Xivitona maculada',NULL,NULL),(1417,'Columba oenas','Xixella',NULL,NULL),(1418,'Falco tinnunculus','Xoriguer comú',NULL,NULL),(1419,'Falcons naumannis','Xoriguer petit',NULL,NULL),(1420,'Otus scops','Xot eurasiàtic',NULL,NULL),(1421,'Pterocles orientalis','Xurra',NULL,NULL),(1422,'Hieraaetus pennatus','Àguila calçada comuna',NULL,NULL),(1423,'Clanga clanga','Àguila cridanera',NULL,NULL),(1424,'Aquila fasciata','Àguila cuabarrada',NULL,NULL),(1425,'Aquila chrysaetos','Àguila daurada',NULL,NULL),(1426,'Aquila adalberti','Àguila imperial ibèrica',NULL,NULL),(1427,'Circaetus gallicus','Àguila marcenca',NULL,NULL),(1428,'Pandion haliaetus','Àguila pescadora',NULL,NULL),(1429,'Clanga pomarina','Àguila pomerània',NULL,NULL),(1430,'Tadorna tadorna','Ànec blanc',NULL,NULL),(1431,'Tadorna ferruginea','Ànec canyella',NULL,NULL),(1432,'Anas platyrhynchos','Ànec collverd',NULL,NULL),(1433,'Anas acuta','Ànec cuallarg',NULL,NULL),(1434,'Anas clypeata','Ànec cullerot comú',NULL,NULL),(1435,'Melanitta fusca','Ànec fosc eurasiàtic',NULL,NULL),(1436,'Clangula hyemalis','Ànec glacial',NULL,NULL),(1437,'Mareca strepera','Ànec griset',NULL,NULL),(1438,'Aix galericulata','Ànec mandarí',NULL,NULL),(1439,'Melanitta nigra','Ànec negre comú',NULL,NULL),(1440,'Anas rubripes','Ànec negrós',NULL,NULL),(1441,'Mareca penelope','Ànec xiulador eurasiàtic',NULL,NULL),(1442,'Somateria mollissima','Èider comú',NULL,NULL),(1443,'Somateria spectabilis','Èider reial',NULL,NULL),(1444,'Tyto alba','Òliba comuna',NULL,NULL);
/*!40000 ALTER TABLE `especie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Nik` varchar(50) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Nik` (`Nik`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Cam','123','123@asdsad.sa','2025-07-02 02:04:06'),(2,'ManelTest','2002','manel@example.com','2025-07-02 02:05:04');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video`
--

DROP TABLE IF EXISTS `video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `video` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `IDUsuario` int DEFAULT NULL,
  `IDCamara` int DEFAULT NULL,
  `Nombre` varchar(100) DEFAULT NULL,
  `Dia` date DEFAULT NULL,
  `ruta_video` text NOT NULL,
  `Video` longblob,
  PRIMARY KEY (`ID`),
  KEY `IDUsuario` (`IDUsuario`),
  KEY `Dia` (`Dia`),
  KEY `IDCamara` (`IDCamara`),
  CONSTRAINT `video_ibfk_1` FOREIGN KEY (`IDUsuario`) REFERENCES `usuario` (`ID`),
  CONSTRAINT `video_ibfk_2` FOREIGN KEY (`IDCamara`) REFERENCES `camara` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video`
--

LOCK TABLES `video` WRITE;
/*!40000 ALTER TABLE `video` DISABLE KEYS */;
INSERT INTO `video` VALUES (74,2,1,'stream_20251026','2025-10-26','uploads/videos\\2\\74.mp4',NULL),(82,2,1,'stream_20251027','2025-10-27','uploads/videos\\2\\82.mp4',NULL),(83,2,1,'stream_20251027','2025-10-27','',NULL),(84,2,1,'stream_20251027','2025-10-27','uploads/videos\\2\\84.mp4',NULL),(85,2,1,'stream_20251027','2025-10-27','uploads/videos\\2\\85.mp4',NULL);
/*!40000 ALTER TABLE `video` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'yolo'
--

--
-- Dumping routines for database 'yolo'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-17 18:33:04
