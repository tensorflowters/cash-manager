import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:marketplace/Article.dart';
import 'package:marketplace/Product.dart';
import 'package:marketplace/login_screen.dart';
import 'package:responsive_grid_list/responsive_grid_list.dart';
import 'package:http/http.dart' as http;
import 'User.dart';
import 'Category.dart';
import 'dart:developer';
import 'dart:convert';

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

List<Widget> widgetItems = [];

void main() {
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
  Future<List<Product>> fetchCategoryList() async {
    //fetch ici
    final response = await http.get(Uri.parse(
        'http://cashm-loadb-6c77i08jb3gn-3d2b8e5c5d258b73.elb.eu-west-3.amazonaws.com:8000/api/categories/'));
    if (response.statusCode == 200) {
      log(response.body.toString());
      var a = jsonDecode(response.body);

      for (var i = 0; i < a["results"].length; i++) {
        setState(() {
          widget.categoryList
              .add(Category(a["results"][i]["id"], a["results"][i]["name"]));
        });
      }
      return [];
    }
    return [];
  }

  @override
  void initState() {
    super.initState();
    Future<List<Product>> pL = fetchCategoryList();
    log(pL.toString());
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
        primarySwatch: Colors.blue,
      ),
     home: LoginScreen(),
        //
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
  List<Category> categoryList;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  List<Widget> setWidgets(BuildContext context) {
    List<Widget> wL = [];
    for (var i = 0; i < widget.categoryList.length; i++) {
      Widget newObj = Card(
        child: SizedBox(
          width: 250,
          height: 250,
          child: InkWell(
            splashColor: Colors.blue.withAlpha(30),
            onTap: () {
              Navigator.of(context).push(MaterialPageRoute(builder: (content) {
                return Catalogue(
                    categorie: widget.categoryList[i],
                    savedItem: widget.savedItem);
              }));
              //Navigator.pushNamed(context, '/${itemList[i]}');
            },
            child: SizedBox(
              width: 250,
              height: 250,
              child: Text('${widget.categoryList[i].getCategoryName()}'),
            ),
          ),

          //child: Center(child: Text('${itemList[i]}')),
        ),
      );
      wL.add(newObj);
    }
    return wL;
  }

  int _selectedIndex = 0;

  void _onItemTapped(int index) {
    setState(() {
      widget.selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      body: Center(
        child: ResponsiveGridList(
            minItemWidth: 250,
            minItemsPerRow:
                2, // The minimum items to show in a single row. Takes precedence over minItemWidth
            maxItemsPerRow: 5,
            children: setWidgets(context)),
      ),
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
            String where = "";
            if (value == 0) {
              where = "/";
            } else if (value == 1) {
              where = "/";
            } else if (value == 2) {
              where = "/";
            } else {
              where = "/";
            }
            if (value == 3) {
              setState(() {
                widget.user.setUserID(12);
              });
              Navigator.of(context).push(MaterialPageRoute(builder: (content) {
                return Text('TEST');
              }));
            }
            _onItemTapped(value);
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
  Catalogue({super.key, required this.categorie, required this.savedItem});
  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final Category categorie;

  final Set<String> savedItem;

  @override
  State<Catalogue> createState() => _CatalogueState();
}

class _CatalogueState extends State<Catalogue> {
  List<Widget> createWid(Future<List<Product>> catalogueItems) {
    List<Widget> wL = [];
    catalogueItems.then((value) => () {
          for (var i = 0; i < value.length; i++) {
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
                          product: value[i], savedItem: widget.savedItem);
                    }));
                    //Navigator.pushNamed(context, '/${itemList[i]}');
                  },
                  child: SizedBox(
                    width: 250,
                    height: 250,
                    child: Text('${value[i].getProductName()}'),
                  ),
                ),

                //child: Center(child: Text('${itemList[i]}')),
              ),
            );
            wL.add(newObj);
          }
          return wL;
        });
    return wL;
  }

  List<Widget> setCatalogWidget(BuildContext context) {
    //widget.categorie;
    log("fdp");
    createWid(widget.categorie.getProductList());
    log("fdp2");
    return createWid(widget.categorie.getProductList());

    //return createWid([Product(1, "Product 1"), Product(2, "Product 2")]);
  }

  @override
  Widget build(BuildContext context) {
    List<Widget> wL = setCatalogWidget(context);
    return Scaffold(
      appBar: AppBar(
        title: new Text(widget.categorie.getCategoryName()),
      ),
      body: Center(
        child: ResponsiveGridList(
            minItemWidth: 250,
            minItemsPerRow:
                2, // The minimum items to show in a single row. Takes precedence over minItemWidth
            maxItemsPerRow: 5,
            children: wL),
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

  @override
  State<ArticlesView> createState() => _ArticlesViewState();
}

class _ArticlesViewState extends State<ArticlesView> {
  List<Widget> createWid() {
    Future<List<Article>> articleList = widget.product.getArticleList();

    articleList.then((value) => () {
          List<Article> articleFetch = value;
          List<Widget> wL = [];

          for (var i = 0; i < articleFetch.length; i++) {
            var item = articleFetch[i].getArticleName();
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
                                widget.savedItem.contains(
                                        articleFetch[i].getArticleName())
                                    ? Icons.favorite
                                    : Icons.favorite_border,
                                color: widget.savedItem.contains(
                                        articleFetch[i].getArticleName())
                                    ? Colors.red
                                    : null,
                                semanticLabel: widget.savedItem.contains(
                                        articleFetch[i].getArticleName())
                                    ? 'Remove from saved'
                                    : 'Save',
                              ),
                              onPressed: () {
                                setState(() {
                                  debugPrint(widget.savedItem
                                      .contains(
                                          articleFetch[i].getArticleName())
                                      .toString());
                                  if (widget.savedItem.contains(
                                      articleFetch[i].getArticleName())) {
                                    widget.savedItem.remove(
                                        articleFetch[i].getArticleName());
                                  } else {
                                    widget.savedItem
                                        .add(articleFetch[i].getArticleName());
                                  }
                                });
                              }),
                          Text("${item}")
                        ],
                      )),
                ),

                //child: Center(child: Text('${itemList[i]}')),
              ),
            );
            wL.add(newObj);
          }

          log("value :");
        });
    List<Widget> wL = [];

    return wL;
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
            children: createWid()),
      ),
      bottomNavigationBar: Text(widget.savedItem.toString()),
    );
  }
}
