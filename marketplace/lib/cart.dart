// ignore_for_file: unnecessary_new
import 'package:flutter/material.dart';
import 'package:quantity_input/quantity_input.dart';
import 'package:http/http.dart' as http;
import 'package:marketplace/Article.dart';

class CartView extends StatefulWidget {
  const CartView({super.key});

  @override
  State<CartView> createState() => _CartViewState();
}

class _CartViewState extends State<CartView> {
  late final List<Article> savedItem;
  var simpleIntInput = 1;

  @override
  Widget build(BuildContext context) {
    return Container(
        color: Color.fromARGB(255, 240, 240, 240),
        padding: EdgeInsets.only(top: 10, left: 10, right: 10),
        child: Column(children: [
          Container(
              padding: EdgeInsets.only(top: 20, bottom: 10),
              child: Text(
                  style: TextStyle(
                      fontWeight: FontWeight.w600,
                      color: Colors.grey[900],
                      fontSize: 24),
                  "Panier")),
          Container(
            height: MediaQuery.of(context).size.height - 215,
            child: ListView.builder(
                scrollDirection: Axis.vertical,
                shrinkWrap: true,
                itemCount: savedItem.length,
                itemBuilder: (BuildContext context, int index) {
                  return Container(
                      margin: EdgeInsets.only(bottom: 10),
                      child: Container(
                        decoration: const BoxDecoration(
                            color: Colors.white,
                            borderRadius:
                                BorderRadius.all(Radius.circular(16.0))),
                        padding: EdgeInsets.all(10),
                        child: IntrinsicHeight(
                            child: Row(
                          /* mainAxisAlignment: MainAxisAlignment.start,
                          crossAxisAlignment: CrossAxisAlignment.center, */
                          children: [
                            Expanded(
                                flex: 1,
                                child: Padding(
                                    padding: EdgeInsets.only(right: 20),
                                    child: Image(
                                      width: 100,
                                      height: 80,
                                      image: NetworkImage(
                                          '${savedItem[index].getUrl()}'),
                                    ))),
                            Expanded(
                                flex: 3,
                                child: Container(
                                    child: Column(
                                        mainAxisAlignment:
                                            MainAxisAlignment.spaceBetween,
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                      Text(
                                          style: TextStyle(
                                              fontWeight: FontWeight.w600,
                                              color: Colors.grey[900],
                                              fontSize: 18),
                                          textAlign: TextAlign.left,
                                          savedItem[index].getArticleName()),
                                      Container(
                                          width: 120,
                                          height: 40,
                                          decoration: BoxDecoration(
                                              border: Border.all(
                                                  width: 1.0,
                                                  color: Colors.black),
                                              borderRadius:
                                                  BorderRadius.circular(5),
                                              color: Colors.white),
                                          child: Row(
                                            mainAxisAlignment:
                                                MainAxisAlignment.spaceBetween,
                                            children: [
                                              IconButton(
                                                iconSize: 20,
                                                icon: const Icon(Icons.remove),
                                                color: Colors.black,
                                                tooltip:
                                                    'Decrease quantity by 1',
                                                onPressed: () {
                                                  setState(() {
                                                    savedItem[index]
                                                        .setQuantity(-1);
                                                  });
                                                },
                                              ),
                                              Text(
                                                  style: TextStyle(
                                                    color: Colors.black,
                                                  ),
                                                  '${savedItem[index].getQuantity()}'),
                                              IconButton(
                                                iconSize: 20,
                                                icon: const Icon(Icons.add),
                                                color: Colors.black,
                                                tooltip:
                                                    'Increase quantity by 1',
                                                onPressed: () {
                                                  setState(() {
                                                    savedItem[index]
                                                        .setQuantity(1);
                                                  });
                                                },
                                              ),
                                            ],
                                          ))
                                    ]))),
                            Expanded(
                              flex: 1,
                              child: Container(
                                  width: 100,
                                  alignment: Alignment.centerRight,
                                  margin: EdgeInsets.only(right: 10),
                                  child: Column(
                                    mainAxisAlignment:
                                        MainAxisAlignment.spaceBetween,
                                    //crossAxisAlignment: CrossAxisAlignment.end,
                                    children: [
                                      Container(
                                        child: IconButton(
                                          icon: Icon(Icons.close),
                                          onPressed: () {},
                                        ),
                                      ),
                                      Container(
                                        child: Text(
                                            style: TextStyle(
                                                fontWeight: FontWeight.w600,
                                                color: Colors.grey[900],
                                                fontSize: 16),
                                            "10€"),
                                      )
                                    ],
                                  )),
                            )
                          ],
                        )),
                      ));
                }),
          ),
          Container(
              height: 60,
              child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    TextButton(
                      style: ButtonStyle(
                          padding: MaterialStateProperty.all<EdgeInsets>(
                              EdgeInsets.all(15)),
                          maximumSize:
                              MaterialStateProperty.all(const Size(200, 100)),
                          backgroundColor:
                              MaterialStateProperty.all(Colors.green[400]),
                          foregroundColor:
                              MaterialStateProperty.all(Colors.white),
                          textStyle: MaterialStateProperty.all(
                              TextStyle(fontSize: 20, color: Colors.white))),
                      onPressed: () {},
                      child: Text('Valider le panier'),
                    )
                  ]))
        ]));
  }
}
