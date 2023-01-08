import 'package:flutter/material.dart';

import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:marketplace/Article.dart';
import 'package:marketplace/Product.dart';
import 'package:marketplace/qrcode.dart';
import 'package:marketplace/cart.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:marketplace/login_screen.dart';
import 'package:responsive_grid_list/responsive_grid_list.dart';
import 'package:http/http.dart' as http;
import 'User.dart';
import 'Category.dart';
import 'dart:developer';
import 'dart:convert';

import 'dart:io' show Platform;
import 'dart:ui' as ui;

// List<Object> itemList = [
//   {'caterogyID': 0, 'nategoryName': 'fromage'},
//   {'caterogyID': 1, 'nategoryName': 'légumes'},
//   {'caterogyID': 2, 'nategoryName': 'pizzas'},
// ];

// [
//   "fromages",
//   "légumes",
//   "condiments",
//   "Alcool",
//   "viande",
//   "conserve",
//   "fruits"
// ];

// List<Widget> widgetItems = [];

void main() async {
  await dotenv.load();

  runApp(
    MyApp(),
  );
}

class MyApp extends StatefulWidget {
  MyApp({super.key});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".
  final currentUser = new User();
  final savedItem = <String>{};
  final selectexIndex = 0;
  List<Category> categoryList = [];

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
/*   Future<List<Product>> fetchCategoryList() async {
    //fetch ici
    /* final response =
        await http.get(Uri.parse('${dotenv.env['PATH_HOST']!}/api/categories'));
    if (response.statusCode == 200) {
      var a = jsonDecode(response.body);

      for (var i = 0; i < a["results"].length; i++) {
        setState(() {
          widget.categoryList.add(Category(a["results"][i]["id"],
              a["results"][i]["name"], a["results"][i]["url"]));
        });
      }
      return [];
    }
    return []; */
  } */

  @override
  void initState() {
    super.initState();
    //fetchCategoryList();
  }

  Future<String?> accesToken() async {
    final storage = new FlutterSecureStorage();
    String? accessToken = await storage.read(key: "accessToken");

    return accessToken.toString();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(

          // This is the theme of your application.
          //
          // Try running your application with "flutter run". You'll see the
          // application has a blue toolbar. Then, without quitting the app, try
          // changing the primarySwatch below to Colors.green and then invoke
          // "hot reload" (press "r" in the console where you ran "flutter run",
          // or simply save your changes to "hot reload" in a Flutter IDE).
          // Notice that the counter didn't reset back to zero; the application
          // is not restarted.
          //primarySwatch: Colors.blue,
          ),
      home: MyHomePage(
        title: 'dsq',
        savedItem: widget.savedItem,
        user: widget.currentUser,
        selectedIndex: widget.selectexIndex,
        categoryList: widget.categoryList,
      ),

      // Start the app with the "/" named route. In this case, the app starts
      // on the FirstScreen widget.
      //initialRoute: '/',
      //routes: setItem(context),
      // {
      //   // When navigating to the "/" route, build the FirstScreen widget.
      //   '/home': (context) => const MyHomePage(title: 'Market Place'),
      //   // When navigating to the "/second" route, build the CatalogueItems widget.
      // }
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage(
      {super.key,
      required this.title,
      required this.savedItem,
      required this.user,
      required this.selectedIndex,
      required this.categoryList});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;
  final Set<String> savedItem;
  final User user;
  int selectedIndex;
  int index = 0;
  List<Category> categoryList;
  List<Widget> widgetCatList = [];
  List<Widget> widgetProductList = [];

  Object state = {
    "state": 0,
  };

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  void setWid() {
    // log("1");
    widget.widgetCatList = [];
    widget.widgetProductList = [];
    for (var i = 0; i < widget.categoryList.length; i++) {
      Widget containerGlobal = Container(
          alignment: Alignment.center,
          child: Container(
            width: 250.0,
            height: 250.0,
            decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(30.0),
                image: DecorationImage(
                    image: NetworkImage(
                      '${widget.categoryList[i].getCatergoryImage()}',
                    ),
                    fit: BoxFit.cover)),
            child: Column(
              children: [
                SizedBox(
                  width: 200,
                  height: 230,
                  child: InkWell(
                    splashColor: Colors.blue.withAlpha(30),
                    onTap: () {
                      setState(() {
                        log("ntm");
                        widget.state = {"state": 1};
                        widget.index = i;
                        // widget.widgetProductList.add(Catalogue(
                        //     categorie: widget.categoryList[i],
                        //     savedItem: widget.savedItem));
                        // log("widget 2 List: " +
                        //     widget.widgetProductList.toString());
                      });
                    },
                  ),
                ),
                Text(
                  '${widget.categoryList[i].getCategoryName()}',
                  // style: TextStyle(fontFamily: 'Raleway'),
                ),
              ],
            ),
          ));
      widget.widgetCatList.add(containerGlobal);
      setState(() {
        widget.widgetProductList.add(Catalogue(
            categorie: widget.categoryList[i],
            savedItem: widget.savedItem,
            state: widget.state,
            f: () {
              setState(() {
                widget.state = {"state": 0};
              });
            }));
      });
      // wL.add(containerGlobal);
    }
    log("widget 1 List: " + widget.widgetCatList.toString());
    log("widget 3 List: " + widget.widgetProductList.toString());
  }

  int _selectedIndex = 0;

  void _onItemTapped(int index) {
    setState(() {
      widget.selectedIndex = index;
    });
  }

  @override
  void initState() {
    super.initState();
    setWid();
    //fetchCategoryList();
  }

  // List<Widget> _wO = <Widget>[
  //   Center(
  //     child: ResponsiveGridList(
  //         minItemWidth: 250,
  //         minItemsPerRow:
  //             2, // The minimum items to show in a single row. Takes precedence over minItemWidth
  //         maxItemsPerRow: 5,
  //         children: setWidgets(context)),
  //   )
  // ];

  @override
  Widget build(BuildContext context) {
    setWid();
    Object obj = {};

    List<Widget> lw = [
      Center(
        child: ResponsiveGridList(
            minItemWidth: 250,
            minItemsPerRow:
                2, // The minimum items to show in a single row. Takes precedence over minItemWidth
            maxItemsPerRow: 5,
            children: widget.widgetCatList),
      ),
      Center(child: QRViewExample()),
      Center(child: CartView()),
      PannierView(savedItem: widget.savedItem)
    ];

    return Scaffold(
      appBar: AppBar(
        toolbarHeight: 0,
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Container(
            alignment: Alignment.center,
            child: Container(
              width: 300.0,
              height: 300.0,
              decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(30.0),
                  image: DecorationImage(
                      image: NetworkImage(
                        'https://picsum.photos/250?image=9',
                      ),
                      fit: BoxFit.cover)),
            )),
        backgroundColor: Color.fromARGB(255, 233, 39, 10),
      ),
      body: widget.state.toString() == "{state: 0}"
          ? lw.elementAt(_selectedIndex)
          : widget.widgetProductList.elementAt(widget.index),
      bottomNavigationBar: BottomNavigationBar(
          items: <BottomNavigationBarItem>[
            BottomNavigationBarItem(
              icon: Icon(Icons.list),
              label: 'Catalog',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.camera_enhance_rounded),
              label: 'Camera',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.business),
              label: 'Business',
            ),
            widget.user.getUserID() == -1
                ? (BottomNavigationBarItem(
                    icon: Icon(Icons.app_registration_outlined),
                    label: 'Connect / Register',
                  ))
                : BottomNavigationBarItem(
                    icon: Icon(Icons.account_box_rounded),
                    label: 'Profil',
                  )
          ],
          currentIndex: widget.selectedIndex,
          selectedItemColor: Colors.amber[800],
          unselectedItemColor: Colors.amber[800],
          onTap: ((value) {
            debugPrint(value.toString());
            debugPrint("state : " + widget.state.toString());
            setState(() {
              _selectedIndex = value;
              widget.state = {"state": 0};
            });
            // _selectedIndex = value;
            // String where = "";
            // log("le wid 111 : " + lw.toString());
            // log("le wid :  " + lw.elementAt(_selectedIndex).toString());
            // if (value == 0) {
            //   widget.widgetCatList = [];
            //   setWid();
            //   where = "/";
            // } else if (value == 1) {
            //   where = "/";
            // } else if (value == 2) {
            //   where = "/";
            // } else {
            //   where = "/";
            // }
            // if (value == 3) {
            //   setState(() {
            //     widget.user.setUserID(12);
            //   });
            //   Navigator.of(context).push(MaterialPageRoute(builder: (content) {
            //     return PannierView(
            //       savedItem: widget.savedItem,
            //     );
            //   }));
            // }
            //Navigator.pushNamed(context, where);
          })),

      // floatingActionButton: FloatingActionButton(
      //   onPressed: _incrementCounter,
      //   tooltip: 'Increment',
      //   child: const Icon(Icons.add),
      // ),
      // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}

class Catalogue extends StatefulWidget {
  Catalogue(
      {super.key,
      required this.categorie,
      required this.savedItem,
      required this.state,
      required this.f});
  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final Category categorie;

  Object state;

  final void f;

  final Set<String> savedItem;

  final List<Product> wL = [];

  final List<Widget> wW = [];

  @override
  State<Catalogue> createState() => _CatalogueState();
}

class _CatalogueState extends State<Catalogue> {
  Future<List<Product>> fetchCategoryList() async {
    //fetch ici
    final response = await http.get(Uri.parse(
        'http://cashm-LoadB-ZPP2BA9ENVKM-e390742801ec8946.elb.eu-west-3.amazonaws.com:8000/api/products/?category_id=${widget.categorie.getCategoryID()}'));
    if (response.statusCode == 200) {
      var a = jsonDecode(response.body);

      for (var i = 0; i < a["results"].length; i++) {
        setState(() {
          Widget obj = Container(
              alignment: Alignment.center,
              child: Container(
                  width: 250.0,
                  height: 250.0,
                  decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(30.0),
                      image: DecorationImage(
                          image: NetworkImage(
                            '${a["results"][i]["url"]}',
                          ),
                          fit: BoxFit.cover)),
                  child: Column(children: [
                    SizedBox(
                      width: 250,
                      height: 250,
                      child: InkWell(
                        splashColor:
                            Color.fromARGB(255, 121, 33, 243).withAlpha(30),
                        onTap: () {
                          Navigator.of(context)
                              .push(MaterialPageRoute(builder: (content) {
                            return ArticlesView(
                                product: Product(a["results"][i]["id"],
                                    a["results"][i]["name"]),
                                savedItem: widget.savedItem);
                          }));
                        },
                        child: SizedBox(
                          width: 250,
                          height: 250,
                          child: Text('${a["results"][i]["name"]}'),
                        ),
                      ),
                    ),
                  ])));

          Widget newObj = Card(
            child: SizedBox(
              width: 250,
              height: 250,
              child: InkWell(
                splashColor: Color.fromARGB(255, 121, 33, 243).withAlpha(30),
                onTap: () {
                  Navigator.of(context)
                      .push(MaterialPageRoute(builder: (content) {
                    return ArticlesView(
                        product: Product(
                            a["results"][i]["id"], a["results"][i]["name"]),
                        savedItem: widget.savedItem);
                  }));
                },
                child: SizedBox(
                  width: 250,
                  height: 250,
                  child: Text('${a["results"][i]["name"]}'),
                ),
              ),
            ),
          );
          widget.wW.add(obj);
        });
      }
      return [];
    }
    return [];
  }

  @override
  void initState() {
    super.initState();
    fetchCategoryList();
    log("index " + widget.state.toString());
    log("ntm fd____________________________________________________________________p");
  }

  @override
  Widget build(BuildContext context) {
    // List<Widget> wL = setCatalogWidget(context);
    // fetchCategoryList();

    return Scaffold(
      appBar: AppBar(
        toolbarHeight: Platform.isAndroid ? 0 : 50,
        title: new Text(widget.categorie.getCategoryName()),
        actions: [
          ButtonBar(
            children: [
              ElevatedButton(
                  onPressed: () {
                    widget.f;
                    log("wid : " + widget.state.toString());
                    widget.state = {"state": 0};
                    setState(() {
                      log("state b4 : " + widget.state.toString());
                      log("state after : " + widget.state.toString());
                    });
                  },
                  child: Text("Retour"))
            ],
          )
        ],
      ),
      body: Center(
        child: ResponsiveGridList(
            minItemWidth: 250,
            minItemsPerRow:
                1, // The minimum items to show in a single row. Takes precedence over minItemWidth
            maxItemsPerRow: 1,
            children: widget.wW),
      ),
      bottomNavigationBar: Text(widget.savedItem.toString()),
    );
  }
}

class ArticlesView extends StatefulWidget {
  ArticlesView({super.key, required this.product, required this.savedItem});
  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final Product product;

  final Set<String> savedItem;

  final List<Widget> wW = [];

  @override
  State<ArticlesView> createState() => _ArticlesViewState();
}

class _ArticlesViewState extends State<ArticlesView> {
  @override
  void initState() {
    super.initState();
    fetchArticleList();
  }

  Future<List<Product>> fetchArticleList() async {
    final response = await http.get(Uri.parse(
        'http://cashm-LoadB-ZPP2BA9ENVKM-e390742801ec8946.elb.eu-west-3.amazonaws.com:8000/api/articles/?product_id=${widget.product.getProductID()}'));

    if (response.statusCode == 200) {
      var a = jsonDecode(response.body);
      for (var i = 0; i < a["results"].length; i++) {
        Widget obj = Container(
            alignment: Alignment.center,
            child: Container(
                width: 250.0,
                height: 250.0,
                decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(30.0),
                    image: DecorationImage(
                        image: NetworkImage(
                          '${a["results"][i]["url"]}',
                        ),
                        fit: BoxFit.cover)),
                child: Column(children: [
                  SizedBox(
                    width: 250,
                    height: 250,
                    child: InkWell(
                      splashColor: Colors.blue.withAlpha(30),
                      child: SizedBox(
                          width: 250,
                          height: 250,
                          child: Column(
                            children: [
                              IconButton(
                                  icon: Icon(
                                    widget.savedItem
                                            .contains(a["results"][i]["name"])
                                        ? Icons.favorite
                                        : Icons.favorite_border,
                                    color: widget.savedItem
                                            .contains(a["results"][i]["name"])
                                        ? Colors.red
                                        : null,
                                    semanticLabel: widget.savedItem
                                            .contains(a["results"][i]["name"])
                                        ? 'Remove from saved'
                                        : 'Save',
                                  ),
                                  onPressed: () {
                                    setState(() {
                                      debugPrint(widget.savedItem
                                          .contains(a["results"][i]["name"])
                                          .toString());

                                      if (widget.savedItem
                                          .contains(a["results"][i]["name"])) {
                                        widget.savedItem
                                            .remove(a["results"][i]["name"]);
                                      } else {
                                        widget.savedItem
                                            .add(a["results"][i]["name"]);
                                      }
                                      debugPrint(widget.savedItem
                                          .contains(a["results"][i]["name"])
                                          .toString());
                                    });
                                  }),
                              Text("${a["results"][i]["name"]}")
                            ],
                          )),
                    ),

                    //child: Center(child: Text('${itemList[i]}')),
                  )
                ])));

        Widget newObj = Card(
          child: SizedBox(
            width: 250,
            height: 250,
            child: InkWell(
              splashColor: Colors.blue.withAlpha(30),
              child: SizedBox(
                  width: 250,
                  height: 250,
                  child: Column(
                    children: [
                      IconButton(
                          icon: Icon(
                            widget.savedItem.contains(a["results"][i]["name"])
                                ? Icons.favorite
                                : Icons.favorite_border,
                            color: widget.savedItem
                                    .contains(a["results"][i]["name"])
                                ? Colors.red
                                : null,
                            semanticLabel: widget.savedItem
                                    .contains(a["results"][i]["name"])
                                ? 'Remove from saved'
                                : 'Save',
                          ),
                          onPressed: () {
                            setState(() {
                              debugPrint(widget.savedItem
                                  .contains(a["results"][i]["name"])
                                  .toString());

                              if (widget.savedItem
                                  .contains(a["results"][i]["name"])) {
                                widget.savedItem
                                    .remove(a["results"][i]["name"]);
                              } else {
                                widget.savedItem.add(a["results"][i]["name"]);
                              }
                              debugPrint(widget.savedItem
                                  .contains(a["results"][i]["name"])
                                  .toString());
                            });
                          }),
                      Text("${a["results"][i]["name"]}")
                    ],
                  )),
            ),

            //child: Center(child: Text('${itemList[i]}')),
          ),
        );
        setState(() {
          widget.wW.add(obj);
        });
      }
    }
    return [];
    // Widget newObj = Card(
    //           child: SizedBox(
    //             width: 250,
    //             height: 250,
    //             child: InkWell(
    //               splashColor: Colors.blue.withAlpha(30),
    //               child: SizedBox(
    //                   width: 250,
    //                   height: 250,
    //                   child: Column(
    //                     children: [
    //                       IconButton(
    //                           icon: Icon(
    //                             widget.savedItem.contains(
    //                                     articleFetch[i].getArticleName())
    //                                 ? Icons.favorite
    //                                 : Icons.favorite_border,
    //                             color: widget.savedItem.contains(
    //                                     articleFetch[i].getArticleName())
    //                                 ? Colors.red
    //                                 : null,
    //                             semanticLabel: widget.savedItem.contains(
    //                                     articleFetch[i].getArticleName())
    //                                 ? 'Remove from saved'
    //                                 : 'Save',
    //                           ),
    //                           onPressed: () {
    //                             setState(() {
    //                               debugPrint(widget.savedItem
    //                                   .contains(
    //                                       articleFetch[i].getArticleName())
    //                                   .toString());
    //                               if (widget.savedItem.contains(
    //                                   articleFetch[i].getArticleName())) {
    //                                 widget.savedItem.remove(
    //                                     articleFetch[i].getArticleName());
    //                               } else {
    //                                 widget.savedItem
    //                                     .add(articleFetch[i].getArticleName());
    //                               }
    //                             });
    //                           }),
    //                       Text("${item}")
    //                     ],
    //                   )),
    //             ),

    //             //child: Center(child: Text('${itemList[i]}')),
    //           ),
    //         );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: new Text(widget.product.getProductName()),
      ),
      body: Center(
        child: ResponsiveGridList(
            minItemWidth: 250,
            minItemsPerRow:
                2, // The minimum items to show in a single row. Takes precedence over minItemWidth
            maxItemsPerRow: 5,
            children: widget.wW),
      ),
      bottomNavigationBar: Text(widget.savedItem.toString()),
    );
  }
}

class PannierView extends StatefulWidget {
  PannierView({super.key, required this.savedItem});
  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final Set<String> savedItem;

  @override
  State<PannierView> createState() => _PannieriewState();
}

class _PannieriewState extends State<PannierView> {
  @override
  void initState() {
    super.initState();

    // fetchArticleList();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: new Text("Pannier"),
      ),
      body: Center(
        child: Text('${widget.savedItem.toString()}'),
      ),
      bottomNavigationBar: Text(""),
    );
  }
}
