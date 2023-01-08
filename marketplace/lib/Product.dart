// ignore_for_file: file_names

import 'dart:convert';
import 'dart:developer';

import 'Article.dart';
import 'package:http/http.dart' as http;

class Product {
  late int _productID;
  late String _productName;
  late List<Article> lA;

  Product(int productID, String productName) {
    _productID = productID;
    _productName = productName;
  }

  int getProductID() {
    return _productID;
  }

  String getProductName() {
    return _productName;
  }

  Future<List<Article>> getArticleList() async {
    //fetch ici
    final response =
        await http.get(Uri.parse('http://localhost:5000/api/categories/'));
    if (response.statusCode == 200) {
      var a = jsonDecode(response.body);
      log(a.toString());
    }

    //http://cashm-loadb-6c77i08jb3gn-3d2b8e5c5d258b73.elb.eu-west-3.amazonaws.com:8000/api/articles
    return [/* Article(0, "article 1"), Article(1, "article 2") */];
  }
}

//catégory ==> product ==> arcticles
