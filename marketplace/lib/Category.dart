// ignore_for_file: file_names

import 'package:flutter_dotenv/flutter_dotenv.dart';

import 'Product.dart';
import 'package:http/http.dart' as http;
import 'dart:developer';
import 'dart:convert';

class Category {
  late int _categoryID;
  late String _categoryName;
  late String _categoryImg;

  Category(int categoryID, String categoryName, String categoryImg) {
    _categoryID = categoryID;
    _categoryName = categoryName;
    _categoryImg = categoryImg;
  }

  String getCatergoryImage() {
    return _categoryImg;
  }

  String getCategoryName() {
    return _categoryName;
  }

  int getCategoryID() {
    return _categoryID;
  }

  Future<List<Product>> getProductList() async {
    //fetch ici
    final response = await http.get(Uri.parse(
        ('${dotenv.env['PATH_HOST']!}/api/categories/${_categoryID}')));
    if (response.statusCode == 200) {
      List<Product> wP = [];
      var a = jsonDecode(response.body);

      // for (var i = 0; i < a["results"].length; i++) {
      //   wP.add(Product(a["results"][i]["id"], a["results"][i]["name"]));
      // }
      return [];
    }

    //http://cashm-loadb-6c77i08jb3gn-3d2b8e5c5d258b73.elb.eu-west-3.amazonaws.com:8000/api/articles
    return [];
  }
}

//catégory ==> product ==> arcticles