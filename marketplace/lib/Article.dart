import 'package:flutter/cupertino.dart';

class Article {
  late int _articleID;
  late String _articleName;

  Article(int articleID, String articleName) {
    _articleID = articleID;
    _articleName = articleName;
  }
  String getArticleName() {
    return _articleName;
  }

  // Widget getArticleWidget() {
  //   return Widget();
  // }
}

//catégory ==> product ==> arcticles
