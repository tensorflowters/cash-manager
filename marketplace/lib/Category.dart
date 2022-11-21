// ignore_for_file: file_names

import 'Product.dart';
import 'package:http/http.dart' as http;
import 'dart:developer';
import 'dart:convert';

class Category {
  late int _categoryID;
  late String _categoryName;

  Category(int categoryID, String categoryName) {
    _categoryID = categoryID;
    _categoryName = categoryName;
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
        'http://cashm-loadb-6c77i08jb3gn-3d2b8e5c5d258b73.elb.eu-west-3.amazonaws.com:8000/api/products/${_categoryID}'));
    log(response.statusCode.toString());
    if (response.statusCode == 200) {
      List<Product> wP = [];
      var a = jsonDecode(response.body);
      log("INFORMATION CATEGORY");
      log(a.length.toString());
      log(a.toString());

      // for (var i = 0; i < a.length; i++) {
      //   wP.add(Product(a[i]["id"], a[i]["name"]));
      // }
      // log(wP.toString());
      return [];
    }

    //http://cashm-loadb-6c77i08jb3gn-3d2b8e5c5d258b73.elb.eu-west-3.amazonaws.com:8000/api/articles
    return [];
  }
}

//catégory ==> product ==> arcticles
