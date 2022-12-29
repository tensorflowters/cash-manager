import 'dart:ffi';

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

  String getDescription() {
    return _description;
  }

  double getPrice() {
    return _price;
  }

  int getQuantity() {
    return _quantity;
  }

  int setQuantity(int qte) {
    _quantity = _quantity + qte;
    if (_quantity < 1) {
      _quantity = 0;
      return _quantity;
    } else {
      return _quantity;
    }
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
