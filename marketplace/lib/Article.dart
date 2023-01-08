import 'dart:convert';
import 'dart:developer';
import 'dart:ffi';
import 'dart:io';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:http/http.dart' as http;

import 'package:flutter/cupertino.dart';

class Article {
  late int _articleID;
  late String _articleName;
  late String _url;
  late String _description;
  late double _price;
  late int _quantity;

  Article(int articleID, String articleName, String url, String description,
      double price, int quantity) {
    _articleID = articleID;
    _articleName = articleName;
    _url = url;
    _description = description;
    _price = price;
    _quantity = quantity;
  }
  String getArticleName() {
    return _articleName;
  }

  String getUrl() {
    return _url;
  }

  int getId() {
    return _articleID;
  }

  String getDescription() {
    return _description;
  }

  double getPrice() {
    return _price;
  }

  int getQuantity() {
    return _quantity;
  }

  void setQuantity(int qte) async {
    _quantity = _quantity + qte;

    var response = await http.put(
        Uri.parse(
            '${dotenv.env['PATH_HOST']!}/api/authenticated/cart/2/set_quantity/${_articleID}'),
        // Send authorization headers to the backend.
        headers: {
          "content-type": "application/json",
          HttpHeaders.authorizationHeader: 'Bearer ${dotenv.env['TOKEN']}',
        },
        body: jsonEncode(<String, int>{
          'quantity': _quantity,
        }));
    log((response.body).toString());
  }

  factory Article.fromJson(Map<String, dynamic> json, int quantity) {
    return Article(json['id'], json['name'], json['url'], json['description'],
        double.parse(json['price']), quantity);
  }
  // Widget getArticleWidget() {
  //   return Widget();
  // }
}

//catégory ==> product ==> arcticles
