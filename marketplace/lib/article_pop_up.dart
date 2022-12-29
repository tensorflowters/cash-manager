import 'dart:convert';
import 'dart:developer';
import 'dart:io';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter/material.dart';
import 'package:marketplace/Article.dart';
import 'package:quantity_input/quantity_input.dart';
import 'package:http/http.dart' as http;

Future<Article> decodeArticle(id, context) async {
  var response = await http
      .get(Uri.parse('${dotenv.env['PATH_HOST']!}/api/articles/${id!}'));
  if (response.statusCode == 200) {
    /* return Article.fromJson(response.body); */
    return Article.fromJson(jsonDecode(response.body), 1);
  } else {
    log("ERREUR ZEBU");
    print("status code : " + response.statusCode.toString());
    throw Exception("Failed");
  }
}

addToCart(id_article) async {
  var response;
  try {
    response = await http.post(
      Uri.parse(
          '${dotenv.env['PATH_HOST']!}/api/authenticated/cart/2/add/${id_article!}'),
      // Send authorization headers to the backend.
      headers: {
        HttpHeaders.authorizationHeader: 'Bearer ${dotenv.env['TOKEN']}',
      },
    );
  } catch (error) {
    log(error.toString());
  }

  final responseJson = jsonDecode(response.body);
}

class Product {
  //inal int idScan;
  final String name;
  final String price;
  final String description;
  final String url;

  const Product(
      {required this.name,
      required this.price,
      required this.url,
      required this.description});

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
        //idScan: json['userId'],
        description: json['description'],
        name: json['name'],
        price: json['price'],
        url: json['url']);
  }
}

class MyWidget extends StatefulWidget {
  final String articleId;
  const MyWidget(this.articleId);

  @override
  State<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  late Future<Article> n; //= Product(id: 1, title: "title");

  @override
  void initState() {
    super.initState();
    n = decodeArticle(widget.articleId, context);
  }

  var simpleIntInput = 1;
  //decodeArticle();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: Colors.grey[300],
        body: Center(
            child: FutureBuilder<Article>(
          future: n,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              return Stack(
                children: [
                  Column(
                    children: [
                      Expanded(
                        flex: 4,
                        child: Container(
                            padding: EdgeInsets.all(40),
                            child: Image.network(snapshot.data!.getUrl())),
                      ),
                      Expanded(
                        flex: 6,
                        child: Container(
                          padding: const EdgeInsets.only(
                              left: 20.0, right: 20.0, top: 15.0, bottom: 0),
                          decoration: const BoxDecoration(
                            color: Color.fromARGB(255, 255, 255, 255),
                            borderRadius: BorderRadius.vertical(
                              top: Radius.circular(30),
                              bottom: Radius.circular(0),
                            ),
                          ),
                          child: Column(children: [
                            Align(
                              alignment: Alignment.centerLeft,
                              child: Padding(
                                padding: const EdgeInsets.only(
                                    left: 10.0,
                                    right: 0.0,
                                    top: 10.0,
                                    bottom: 0),
                                child: Container(
                                  child: Text(
                                    snapshot.data!.getArticleName(),
                                    style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        color: Colors.grey[800],
                                        fontSize: 30),
                                  ),
                                ),
                              ),
                            ),
                            Align(
                              alignment: Alignment.centerLeft,
                              child: Container(
                                decoration: const BoxDecoration(
                                  color: Color.fromARGB(226, 163, 215, 163),
                                  borderRadius: BorderRadius.vertical(
                                    top: Radius.circular(10),
                                    bottom: Radius.circular(10),
                                  ),
                                ),
                                margin: const EdgeInsets.only(left: 10.0),
                                padding: const EdgeInsets.only(
                                    left: 10.0,
                                    right: 10.0,
                                    top: 5.0,
                                    bottom: 10.0),
                                child: Text(
                                  "${snapshot.data!.getPrice()}€ ",
                                  style: TextStyle(
                                    fontWeight: FontWeight.bold,
                                    color: Colors.grey[800],
                                    fontSize: 20,
                                  ),
                                ),
                              ),
                            ),
                            Container(
                              height: 200,
                              padding: EdgeInsets.all(10),
                              child: SingleChildScrollView(
                                scrollDirection: Axis.vertical, //.horizontal
                                child: Text(
                                  snapshot.data!.getDescription(),
                                  style: const TextStyle(
                                    fontSize: 16.0,
                                    color: Colors.black,
                                  ),
                                ),
                              ),
                            ),
                            const Spacer(),
                            SizedBox(
                                width: double.maxFinite,
                                child: Row(
                                  crossAxisAlignment:
                                      CrossAxisAlignment.baseline,
                                  textBaseline: TextBaseline.alphabetic,
                                  children: [
                                    Container(
                                      child: QuantityInput(
                                          value: simpleIntInput,
                                          buttonColor: Color.fromARGB(
                                              226, 163, 215, 163),
                                          onChanged: (value) => setState(() =>
                                              simpleIntInput = int.parse(
                                                  value.replaceAll(',', '')))),
                                    ),
                                    Container(
                                      child: Align(
                                        alignment: Alignment.centerRight,
                                        child: Text(
                                          (snapshot.data!.getPrice() *
                                                  simpleIntInput)
                                              .toString(),
                                          textAlign: TextAlign.right,
                                        ),
                                      ),
                                    )
                                  ],
                                )),
                            SizedBox(
                                width: double.maxFinite, // <-- match_parent
                                height: 60, // <-- match-parent
                                child: Column(
                                  children: [
                                    ElevatedButton(
                                      style: ElevatedButton.styleFrom(
                                        backgroundColor:
                                            Color.fromARGB(226, 163, 215, 163),
                                        padding: EdgeInsets.all(20),
                                      ),
                                      child: Text('Ajouter au panier'),
                                      onPressed: () async => {
                                        addToCart(widget.articleId),
                                        Navigator.pop(context, "Ok")
                                      },
                                    ),
                                  ],
                                )),
                          ]),
                        ),
                      ),
                    ],
                  ),
                  Positioned(
                      left: 10,
                      top: 30,
                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Color.fromARGB(255, 136, 136, 136),
                          padding: EdgeInsets.all(20),
                        ),
                        child: Text('Retour'),
                        onPressed: () async => {Navigator.pop(context, "Back")},
                      ))
                ],
              );

              //return (Text(snapshot.data!.name));
            } else if (snapshot.hasError) {
              return Text('${snapshot.error}');
            }

            // By default, show a loading spinner.
            return const CircularProgressIndicator();
          },
        )));
  }
}
