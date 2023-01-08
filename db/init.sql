INSERT INTO authentication_user (id, "password", username, first_name, last_name, email, is_staff, is_active, last_login, is_superuser)
VALUES (1, 'pbkdf2_sha256$390000$bR9Nr2uUwtb36wbHMEsB5V$P9S0Bg3vCcpW4zlqF9OikywBYlYlVf1VvtJFDWbxdHc=', 'superadmin', 'Super', 'Admin', 'superadmin@dev.org', true, true, CURRENT_TIMESTAMP, true);
INSERT INTO authentication_user (id, "password", username, first_name, last_name, email, is_staff, is_active, last_login, is_superuser)
VALUES (2, 'pbkdf2_sha256$390000$GchnJjepod0Cwc0vQLkEue$3lL3OXA9mb8P7WRpeU0hHH9wfNG2eXLRnoeV7BLx+zI=', 'jdoe', 'John', 'Doe', 'jdoe@mail.org', false, true, CURRENT_TIMESTAMP, false);

INSERT INTO store_cart (user_id, total_amount)
VALUES (1, 0);
INSERT INTO store_cart (user_id, total_amount)
VALUES (2, 0);

INSERT INTO store_category (id, "name", "active", "description", "url", date_created, date_updated)
VALUES (1, 'PC Parts', true, 'Computer hardware is the physical components that a computer system requires to function. It encompasses everything with a circuit board that operates within a PC or laptop; including the motherboard, graphics card, CPU (Central Processing Unit), ventilation fans, webcam, power supply, and so on.', 'https://levvvel.com/wp-content/uploads/pc-parts-in-a-computer-and-their-function.jpg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO store_product (id, "name", active, "description", "url", category_id, date_created, date_updated)
VALUES (1, 'Processors', true, 'A processor is an integrated electronic circuit that performs the calculations that run a computer. A processor performs arithmetical, logical, input/output (I/O) and other basic instructions that are passed from an operating system (OS). Most other processes are dependent on the operations of a processor.', 'https://60a99bedadae98078522-a9b6cded92292ef3bace063619038eb1.ssl.cf2.rackcdn.com/images_CategoryImages_12_2022Home_Page_CPUs.png', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO store_product (id, "name", active, "description", "url", category_id, date_created, date_updated)
VALUES (2, 'Motherboards', true, 'A motherboard is the main printed circuit board (PCB) in general-purpose computers and other expandable systems. It holds and allows communication between many of the crucial electronic components of a system, such as the central processing unit (CPU) and memory, and provides connectors for other peripherals.', 'https://60a99bedadae98078522-a9b6cded92292ef3bace063619038eb1.ssl.cf2.rackcdn.com/images_CategoryImages_motherboards_062022.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO store_product (id, "name", active, "description", "url", category_id, date_created, date_updated)
VALUES (3, 'Graphic cards', true, 'A graphics card (also called a video card, display card, graphics adapter, VGA card/VGA, video adapter, display adapter, or mistakenly GPU) is an expansion card which generates a feed of output images to a display device, such as a computer monitor. Graphics cards are sometimes called discrete or dedicated graphics cards to emphasize their distinction to integrated graphics', 'https://60a99bedadae98078522-a9b6cded92292ef3bace063619038eb1.ssl.cf2.rackcdn.com/images_CategoryImages_videoCards500.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO store_article ("name", "description", price, stripe_price_id, stripe_product_id, active, "url", in_stock_quantity, out_stock_quantity, product_id, date_created, date_updated)
VALUES (
	'MSI GeForce RTX 4090 SUPRIM X 24G Triple-Fan 24GB GDDR6X PCIe 4.0 Graphics Card', 
	'The NVIDIA GeForce RTX 4090 is the ultimate GeForce GPU. It brings an enormous leap in performance, efficiency, and AI-powered graphics. Experience ultra-high performance gaming, incredibly detailed virtual worlds with ray tracing, unprecedented productivity, and new ways to create. Its powered by the NVIDIA Ada Lovelace architecture and comes with 24 GB of G6X memory to deliver the ultimate experience for gamers and creators.', 
	1749.99,
	'',
	'',
	true,
	'https://90a1c75758623581b3f8-5c119c3de181c9857fcb2784776b17ef.ssl.cf2.rackcdn.com/659533_505958_01_front_comping.jpg', 
	15, 
	7, 
	1, 
	CURRENT_TIMESTAMP, 
	CURRENT_TIMESTAMP
);
INSERT INTO store_article ("name", "description", price, stripe_price_id, stripe_product_id, active,  "url", in_stock_quantity, out_stock_quantity, product_id, date_created, date_updated)
VALUES (
	'ASUS NVIDIA GeForce RTX 4080 TUF Gaming Overclocked Triple Fan 16GB GDDR6X PCIe 4.0 Graphics Card', 
	'The NVIDIA Ada Lovelace architecture elevated by buffed cooling and power delivery, and backed with an arsenal of rugged reinforcements to cover your six. Lock, load, and dominate with the TUF Gaming GeForce RTX 4080.', 
	1399.99,
	'',
	'',
	true,
	'https://90a1c75758623581b3f8-5c119c3de181c9857fcb2784776b17ef.ssl.cf2.rackcdn.com/660836_520072_01_front_comping.jpg', 
	12, 
	5, 
	1, 
	CURRENT_TIMESTAMP, 
	CURRENT_TIMESTAMP
);
INSERT INTO store_article ("name", "description", price, stripe_price_id, stripe_product_id, active, "url", in_stock_quantity, out_stock_quantity, product_id, date_created, date_updated)
VALUES (
	'MSI AMD Radeon RX 6750 XT MECH 2X Overclocked Dual Fan 12GB GDDR6 PCIe 4.0 Graphics Card', 
	'MECH brings a performance-focused design that maintains the essentials to accomplish any task at hand. Rocking a trusted dual fan arrangement laid into a rigid industrial design lets this sharp looking graphics card fit into any build.', 
	524.99,
	'',
	'',
	true,
	'https://90a1c75758623581b3f8-5c119c3de181c9857fcb2784776b17ef.ssl.cf2.rackcdn.com/649620_406231_01_front_comping.jpg', 
	29, 
	18, 
	1, 
	CURRENT_TIMESTAMP, 
	CURRENT_TIMESTAMP
);
INSERT INTO store_article ("name", "description", price, stripe_price_id, stripe_product_id, active, "url", in_stock_quantity, out_stock_quantity, product_id, date_created, date_updated)
VALUES (
	'MSI NVIDIA GeForce RTX 3070 Ti Ventus 3X Overclocked Triple-Fan 8GB GDDR6X PCIe 4.0 Graphics Card', 
	'VENTUS brings a performance-focused design that maintains the essentials to accomplish any task at hand. A capable triple fan arrangement laid into a rigid industrial design lets this sharp looking graphics card fit into any build.', 
	669.99,
	'',
	'',
	true,
	'https://90a1c75758623581b3f8-5c119c3de181c9857fcb2784776b17ef.ssl.cf2.rackcdn.com/638567_287029_01_front_comping.jpg', 
	31, 
	12, 
	1, 
	CURRENT_TIMESTAMP, 
	CURRENT_TIMESTAMP
);
INSERT INTO store_article ("name", "description", price, stripe_price_id, stripe_product_id, active, "url", in_stock_quantity, out_stock_quantity, product_id, date_created, date_updated)
VALUES (
	'Gigabyte NVIDIA GeForce RTX 4080 Gaming Overclocked Triple Fan 16GB GDDR6X PCIe 4.0 Graphics Card', 
	'The WINDFORCE cooling system features three 110mm unique blade fans, alternate spinning, 11 composite copper heat pipes, a large vapor chamber directly touches the GPU, 3D active fans and Screen cooling, which together provide high efficiency heat dissipation.', 
	1269.99,
	'',
	'',
	true,
	'https://90a1c75758623581b3f8-5c119c3de181c9857fcb2784776b17ef.ssl.cf2.rackcdn.com/660699_520460_01_front_comping.jpg', 
	10,
	10,
	1,
	CURRENT_TIMESTAMP, 
	CURRENT_TIMESTAMP
);

INSERT INTO store_article ("name", "description", price, stripe_price_id, stripe_product_id, active, "url", in_stock_quantity, out_stock_quantity, product_id, date_created, date_updated)
VALUES (
	'AMD Ryzen 7 7700X Raphael AM5 4.5GHz 8-Core Boxed Processor - Heatsink Not Included',
	'Welcome to the new era of performance. AMD Ryzen 7000 Series ushers in the speed of Zen 4 for gamers and creators with pure power to tackle any game or workflow on the digital playground.',
	343.98,
	'',
	'',
	true,
	'https://90a1c75758623581b3f8-5c119c3de181c9857fcb2784776b17ef.ssl.cf2.rackcdn.com/652683_436501_01_front_comping.jpg', 
	34,
	12,
	2,
	CURRENT_TIMESTAMP, 
	CURRENT_TIMESTAMP
);
INSERT INTO store_article ("name", "description", price, stripe_price_id, stripe_product_id, active, "url", in_stock_quantity, out_stock_quantity, product_id, date_created, date_updated)
VALUES (
	'AMD Ryzen 9 7950X Raphael AM5 4.5GHz 16-Core Boxed Processor - Heatsink Not Included',
	'Welcome to the new era of performance. AMD Ryzen 7000 Series ushers in the speed of Zen 4 for gamers and creators with pure power to tackle any game or workflow on the digital playground.',
	567.98,
	'',
	'',
	true,
	'https://90a1c75758623581b3f8-5c119c3de181c9857fcb2784776b17ef.ssl.cf2.rackcdn.com/652681_436527_01_front_comping.jpg', 
	29,
	14,
	2,
	CURRENT_TIMESTAMP, 
	CURRENT_TIMESTAMP
);
INSERT INTO store_article ("name", "description", price, stripe_price_id, stripe_product_id, active, "url", in_stock_quantity, out_stock_quantity, product_id, date_created, date_updated)
VALUES (
	'Intel Core i7-12700K Alder Lake 3.6GHz Twelve-Core LGA 1700 Boxed Processor - Heatsink Not Included',
	'The 12th generation of Intel processors provides gamers with an ideal setup for streaming or media production, boasting industry-first PCIe 5.0 compatibility and notable DDR5 memory advancements. With speeds up to 4800 MT/s, DDR5 advancements also prove to be beneficial to memory bandwidth, as it too sees an increase in speed. The processor also features an integrated UHD Graphics 770 chip with 8K HDR support and the ability to view four simultaneous 4K displays. Using Gaussian & Neural Accelerator 3.0 (GNA) technology, noise suppression and background blurring are achieved more efficiently and effectively. A standout feature of this processor is the 12 cores unlocked for overclocking, which share 25MB of the L3 cache. The highest clock speed available for these processors is 5.0 GHz, while the base model sits at 3.6 GHz. Managed by the Intel Thread Director, the cores support the operating system to more intelligently channel workloads to the right core at the right time.',
	308.98,
	'',
	'',
	true,
	'https://90a1c75758623581b3f8-5c119c3de181c9857fcb2784776b17ef.ssl.cf2.rackcdn.com/641917_326652_01_front_comping.jpg', 
	26,
	9,
	2,
	CURRENT_TIMESTAMP, 
	CURRENT_TIMESTAMP
);
INSERT INTO store_article ("name", "description", price, stripe_price_id, stripe_product_id, active, "url", in_stock_quantity, out_stock_quantity, product_id, date_created, date_updated)
VALUES (
	'AMD Ryzen Threadripper PRO 5995WX Chagall PRO 2.7GHz 64-Core sWRX8 Boxed Processor - Heatsink Not Included',
	'With 64 cores and 128 threads, the Threadripper PRO 5995WX delivers incredible performance for multithreaded workflows along with robust platform expandability and AMD PRO Technologies.',
	6499.99,
	'',
	'',
	true,
	'https://90a1c75758623581b3f8-5c119c3de181c9857fcb2784776b17ef.ssl.cf2.rackcdn.com/651156_426718_01_front_comping.jpg', 
	5,
	1,
	2,
	CURRENT_TIMESTAMP, 
	CURRENT_TIMESTAMP
);
INSERT INTO store_article ("name", "description", price, stripe_price_id, stripe_product_id, active, "url", in_stock_quantity, out_stock_quantity, product_id, date_created, date_updated)
VALUES (
	'Intel Core i9-13900K Raptor Lake 3.0GHz Twenty Four-Core LGA 1700 Boxed Processor - Heatsink Not Included',
	'13th Gen Intel Core i9-13900K desktop processor. Featuring Intel Adaptive Boost Technology, Intel Thermal Velocity Boost, Intel Turbo Boost Max Technology 3.0, and PCIe 5.0 & 4.0 support, DDR5 and DDR4 support, unlocked 13th Gen Intel Core i9 desktop processors are optimized for enthusiast gamers and serious creators and help deliver high performance. Compatible with Intel 700 Series and Intel 600 Series Chipset based motherboards. 125W Processor Base Power.',
	579.99,
	'',
	'',
	true,
	'https://90a1c75758623581b3f8-5c119c3de181c9857fcb2784776b17ef.ssl.cf2.rackcdn.com/652624_436188_01_front_comping.jpg', 
	23,
	11,
	2,
	CURRENT_TIMESTAMP, 
	CURRENT_TIMESTAMP
);

INSERT INTO store_article ("name", "description", price, stripe_price_id, stripe_product_id, active, "url", in_stock_quantity, out_stock_quantity, product_id, date_created, date_updated)
VALUES (
	'ASUS B550-F ROG Strix Gaming WiFi II AMD AM4 ATX Motherboard',
	'Experience next-level performance and connectivity with the Asus ROG STRIX B550-F GAMING WIFI II, featuring PCIe 4.0, WiFi 6E and 2.5Gb Ethernet. Robust power and effective cooling make the ROG Strix B550-F Gaming (WiFi 6) the perfect partner for 3rd Gen AMD Ryzen CPUs. Futuristic aesthetics, intuitive software, and a reliable Stack Cool 3+ design put your build in the winners circle.',
	204.99,
	'',
	'',
	true,
	'https://90a1c75758623581b3f8-5c119c3de181c9857fcb2784776b17ef.ssl.cf2.rackcdn.com/642839_332098_01_package_comping.jpg', 
	41,
	26,
	3,
	CURRENT_TIMESTAMP, 
	CURRENT_TIMESTAMP
);
INSERT INTO store_article ("name", "description", price, stripe_price_id, stripe_product_id, active, "url", in_stock_quantity, out_stock_quantity, product_id, date_created, date_updated)
VALUES (
	'MSI X570S MAG TOMAHAWK MAX WiFi AMD AM4 ATX Motherboard',
	'With years of experience, MSI is no stranger to building high-performance motherboards. Our R&D and engineering teams have reviewed countless designs, evaluated a wide selection of high quality components, and developed products for reliability even under extreme conditions. World fastest SSDs can start to lower performance when getting hot. Part of the motherboards heatsink design, M.2 SHIELD FROZR is the next generation M.2 thermal solution to avoid this by offering the best thermal protection to make sure that SSD maintains maximum performance.',
	229.99,
	'',
	'',
	true,
	'https://90a1c75758623581b3f8-5c119c3de181c9857fcb2784776b17ef.ssl.cf2.rackcdn.com/640444_310110_01_front_comping.jpg', 
	23,
	15,
	3,
	CURRENT_TIMESTAMP, 
	CURRENT_TIMESTAMP
);
INSERT INTO store_article ("name", "description", price, stripe_price_id, stripe_product_id, active, "url", in_stock_quantity, out_stock_quantity, product_id, date_created, date_updated)
VALUES (
	'MSI X670E MEG GODLIKE AMD AM5 eATX Motherboard',
	'The MEG X670E GODLIKE is designed with a black and heavy heatsink which comes with dark mirror and time carving design in pale gold illuminating that symbolizes the timeless form and function as well as representing perfection in its purest form. Featuring the latest technology, high-speed transmission, ultra-performance, and Industry first M-Vision Dashboard, the MEG X670E GODLIKE is developed to unleash the extreme gaming potential of the AMD X670 chipset and is ready to rule the tournament once again.',
	1299.99,
	'',
	'',
	true,
	'https://90a1c75758623581b3f8-5c119c3de181c9857fcb2784776b17ef.ssl.cf2.rackcdn.com/652260_433060_01_front_comping.jpg', 
	4,
	2,
	3,
	CURRENT_TIMESTAMP, 
	CURRENT_TIMESTAMP
);
INSERT INTO store_article ("name", "description", price, stripe_price_id, stripe_product_id, active, "url", in_stock_quantity, out_stock_quantity, product_id, date_created, date_updated)
VALUES (
	'ASUS Z790-A Prime WiFi Intel LGA 1700 ATX Motherboard',
	'ASUS Prime series motherboards are expertly engineered to unleash the full potential of 13th Gen Intel Core Processors. Boasting a robust power design, comprehensive cooling solutions and intelligent tuning options, PRIME Z790-A WIFI provides users and PC DIY builders with a range of performance optimizations via intuitive software and firmware features. The ASUS PRIME Z790-A WIFI offers this all in a sleek, futuristic-looking package centered around a spaceship design aesthetic, with a silver-toned nameplate and chipset cover.',
	309.99,
	'',
	'',
	true,
	'https://90a1c75758623581b3f8-5c119c3de181c9857fcb2784776b17ef.ssl.cf2.rackcdn.com/653707_443630_01_front_comping.jpg', 
	12,
	9,
	3,
	CURRENT_TIMESTAMP, 
	CURRENT_TIMESTAMP
);
INSERT INTO store_article ("name", "description", price, stripe_price_id, stripe_product_id, active, "url", in_stock_quantity, out_stock_quantity, product_id, date_created, date_updated)
VALUES (
	'MSI B550-A Pro AMD AM4 ATX Motherboard',
	'PRO series helps users work smarter by delivering an efficient and productive experience. Featuring stable functionality and high-quality assembly, PRO series motherboards provide not only optimized professional workflows but also less troubleshooting and longevity.',
	139.99,
	'',
	'',
	true,
	'https://90a1c75758623581b3f8-5c119c3de181c9857fcb2784776b17ef.ssl.cf2.rackcdn.com/625049_141424_01_front_comping.jpg', 
	45,
	32,
	3,
	CURRENT_TIMESTAMP, 
	CURRENT_TIMESTAMP
);
