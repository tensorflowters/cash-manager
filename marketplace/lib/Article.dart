import 'dart:ffi';

import 'package:flutter/cupertino.dart';

class Article {
  late int _articleID;
  late String _articleName;
  late String _url;
  late String _description;
  late Float _price;

  Article(int articleID, String articleName, String url, String description, Float price) {
    _articleID = articleID;
    _articleName = articleName;
    _url = url;
    _description = description;
    _price = price;
  },
  String getArticleName() {
    return _articleName;
  }

  String getUrl(){
    return _url;
  }

  // Widget getArticleWidget() {
  //   return Widget();
  // }
}

//catégory ==> product ==> arcticles
