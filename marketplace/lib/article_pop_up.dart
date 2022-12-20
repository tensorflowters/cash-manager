import 'dart:convert';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter/material.dart';
import 'package:quantity_input/quantity_input.dart';
import 'package:http/http.dart' as http;

Future<Product> decodeArticle(id) async {
  final response =
      await http.get(Uri.parse(dotenv.env['PATH_HOST']! + '/api/articles/$id'));
  if (response.statusCode == 200) {
    return Product.fromJson(jsonDecode(response.body));
  } else {
    throw Exception("Failed");
    print("status code : " + response.statusCode.toString());
  }
  //id = int.parse( retunObject.body[0]["id"]);
  //tab = retunObject;
  //print(retunObject);
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
  late Future<Product> n; //= Product(id: 1, title: "title");

  @override
  void initState() {
    super.initState();
    n = decodeArticle(widget.articleId);
  }

  var simpleIntInput = 1;
  //decodeArticle();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: Colors.grey[300],
        body: Center(
            child: FutureBuilder<Product>(
          future: n,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              return Column(
                children: [
                  Expanded(
                    flex: 4,
                    child: Container(
                        padding: EdgeInsets.all(40),
                        child: Image.network(snapshot.data!.url)),
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
                                left: 10.0, right: 0.0, top: 10.0, bottom: 0),
                            child: Container(
                              child: Text(
                                snapshot.data!.name,
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
                              "${snapshot.data!.price}€ ",
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
                          child: const SingleChildScrollView(
                            scrollDirection: Axis.vertical, //.horizontal
                            child: Text(
                              "1 Description that is too long in text format(Here Data is coming from API) jdlksaf j klkjjflkdsjfkddfdfsdfds "
                              "2 Description that is too long in text format(Here Data is coming from API) d fsdfdsfsdfd dfdsfdsf sdfdsfsd d "
                              "3 Description that is too long in text format(Here Data is coming from API)  adfsfdsfdfsdfdsf   dsf dfd fds fs"
                              "4 Description that is too long in text format(Here Data is coming from API) dsaf dsafdfdfsd dfdsfsda fdas dsad"
                              "5 Description that is too long in text format(Here Data is coming from API) dsfdsfd fdsfds fds fdsf dsfds fds "
                              "6 Description that is too long in text format(Here Data is coming from API) asdfsdfdsf fsdf sdfsdfdsf sd dfdsf"
                              "7 Description that is too long in text format(Here Data is coming from API) df dsfdsfdsfdsfds df dsfds fds fsd"
                              "8 Description that is too long in text format(Here Data is coming from API)"
                              "9 Description that is too long in text format(Here Data is coming from API)"
                              "10 Description that is too long in text format(Here Data is coming from API)",
                              style: TextStyle(
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
                              crossAxisAlignment: CrossAxisAlignment.baseline,
                              textBaseline: TextBaseline.alphabetic,
                              children: [
                                Container(
                                  child: QuantityInput(
                                      value: simpleIntInput,
                                      buttonColor:
                                          Color.fromARGB(226, 163, 215, 163),
                                      onChanged: (value) => setState(() =>
                                          simpleIntInput = int.parse(
                                              value.replaceAll(',', '')))),
                                ),
                                Container(
                                  child: Align(
                                    alignment: Alignment.centerRight,
                                    child: Text(
                                      snapshot.data!.price * simpleIntInput,
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
                                  onPressed: () => {Navigator.pop(context)},
                                ),
                              ],
                            )),
                      ]),
                    ),
                  ),
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
