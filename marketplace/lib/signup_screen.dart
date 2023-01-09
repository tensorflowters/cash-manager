import 'dart:ffi';

import 'package:flutter/material.dart';
import 'dart:async';
import 'dart:convert';
import 'package:awesome_snackbar_content/awesome_snackbar_content.dart';
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:http/http.dart' as http;
import 'package:marketplace/string_extension.dart';
import 'login_screen.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';


class SignUpScreen extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => InitState();
}

class InitState extends State<SignUpScreen> {

  final storage = new FlutterSecureStorage();
  TextEditingController Username = new TextEditingController();
  TextEditingController FirstName = new TextEditingController();
  TextEditingController LastName = new TextEditingController();
  TextEditingController Email = new TextEditingController();
  TextEditingController Password = new TextEditingController();


  Future<String?> accesToken() async {
    // Create an instance of the 'FlutterSecureStorage' object
    final storage = new FlutterSecureStorage();
    // Use the 'await' operator to wait for the 'Future' to complete
    String? accessToken = await storage.read(key: "accessToken");

    // Return the 'accessToken' as the value of the function
    return accessToken;
  }

  displayError(List $response) {
  print($response);
  }

  postData(String Username, Password, FirstName, LastName, Email) async {

    final body = {
      "username": Username,
      "password": Password,
      "first_name": FirstName,
      "last_name": LastName,
      "email": Email
    };

      final response =
      await http.post(Uri.parse("${dotenv.env['PATH_HOST']!}/api/register"),
        headers: {
          "Content-type": "application/json",
        },
        body: json.encode(body),
      );

    var result = jsonDecode(response.body);
   // print(result);
    if (response.statusCode == 201) {
      print(result);
      ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              elevation: 0,
              behavior: SnackBarBehavior.floating,
              backgroundColor: Colors.transparent,
              content: AwesomeSnackbarContent(
                title: 'Congratulations!',
                message:
                'Your account has been created successfully, you can now Log in',
                contentType: ContentType.success,
              ),
            ));
        Navigator.push(context, MaterialPageRoute(
          builder: (context) => LoginScreen(),
         ));
        } else {
 //     print("access " + "$accesToken()");
    //  String? accessToken = await storage.read(key: "accessToken");
    //  String? refreshToken = await storage.read(key: "refreshToken");
     // print("$accessToken" + "$refreshToken");
     // displayError(result);
      ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                elevation: 0,
                behavior: SnackBarBehavior.floating,
                backgroundColor: Colors.transparent,
                content: AwesomeSnackbarContent(
                  title: result['message'],
                  message: result['detail'].toString().replace().capitalize(),
                  contentType: ContentType.warning,
                ),
              ));
    }


    }

  @override
  Widget build(BuildContext context) {
    return initWidget();
  }

  Widget initWidget() {
    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          children: [
            Container(
              height: 250,
              decoration: BoxDecoration(
                  borderRadius:
                  BorderRadius.only(bottomLeft: Radius.circular(90)),
                  gradient: LinearGradient(colors: [
                    (new Color(0xffF5592F)),
                    (new Color(0xffF2861E))
                  ], begin: Alignment.topCenter, end: Alignment.bottomCenter)),
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Container(
                      margin: EdgeInsets.only(top: 70),
                      child: Image.asset("images/app_logo.png"),
                      height: 135,
                      width: 200,
                    ),
                    Container(
                      margin: EdgeInsets.only(right: 20, top: 20),
                      alignment: Alignment.bottomRight,
                      child: Text(
                        "Register",
                        style: TextStyle(
                          fontSize: 20,
                          color: Colors.white,
                        ),
                      ),
                    )
                  ],
                ),
              ),
            ),

            Container(
              margin: EdgeInsets.only(left: 20, right: 20, top: 70),
              padding: EdgeInsets.only(left: 20, right: 20),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(50),
                color: Colors.grey[200],
                boxShadow: [
                  BoxShadow(
                      offset: Offset(0, 10),
                      blurRadius: 50,
                      color: Color(0xffEEEEEE))
                ],
              ),
              alignment: Alignment.center,
              child: TextField(
                controller: Username,
                cursorColor: Color(0xffF5591F),
                decoration: InputDecoration(
                    icon: Icon(
                      Icons.person,
                      color: Color(0xffF5591F),
                    ),
                    hintText: "Username",
                    enabledBorder: InputBorder.none,
                    focusedBorder: InputBorder.none),
              ),
            ),

            Container(
              margin: EdgeInsets.only(left: 20, right: 200, top: 20),
              padding: EdgeInsets.only(left: 20, right: 20),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(50),
                color: Colors.grey[200],
                boxShadow: [
                  BoxShadow(
                      offset: Offset(0, 10),
                      blurRadius: 50,
                      color: Color(0xffEEEEEE))
                ],
              ),
              alignment: Alignment.center,
              child: TextField(
                controller: FirstName,
                cursorColor: Color(0xffF5591F),
                decoration: InputDecoration(
                    icon: Icon(
                      Icons.person,
                      color: Color(0xffF5591F),
                    ),
                    hintText: "First Name",
                    enabledBorder: InputBorder.none,
                    focusedBorder: InputBorder.none),
              ),
            ),

            Container(
              margin: EdgeInsets.only(left: 200, right: 20),
              transform: Matrix4.translationValues(0.0, -48, 0.0),
              padding: EdgeInsets.only(left: 20, right: 20),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(50),
                color: Colors.grey[200],
                boxShadow: [
                  BoxShadow(
                      offset: Offset(0, 10),
                      blurRadius: 50,
                      color: Color(0xffEEEEEE))
                ],
              ),
              alignment: Alignment.center,
              child: TextField(
                controller: LastName,
                cursorColor: Color(0xffF5591F),
                decoration: InputDecoration(
                    icon: Icon(
                      Icons.person,
                      color: Color(0xffF5591F),
                    ),
                    hintText: "Last Name",
                    enabledBorder: InputBorder.none,
                    focusedBorder: InputBorder.none),
              ),
            ),

            Container(
              margin: EdgeInsets.only(left: 20, right: 20),
              padding: EdgeInsets.only(left: 20, right: 20),
              transform: Matrix4.translationValues(0.0, -15, 0.0),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(50),
                color: Colors.grey[200],
                boxShadow: [
                  BoxShadow(
                      offset: Offset(0, 10),
                      blurRadius: 50,
                      color: Color(0xffEEEEEE))
                ],
              ),
              alignment: Alignment.center,
              child: TextField(
                controller: Email,
                cursorColor: Color(0xffF5591F),
                decoration: InputDecoration(
                    icon: Icon(
                      Icons.email,
                      color: Color(0xffF5591F),
                    ),
                    hintText: "Email",
                    enabledBorder: InputBorder.none,
                    focusedBorder: InputBorder.none),
              ),
            ),

            Container(
              margin: EdgeInsets.only(left: 20, right: 20, top: 20),
              padding: EdgeInsets.only(left: 20, right: 20),
              transform: Matrix4.translationValues(0.0, -15, 0.0),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(50),
                color: Colors.grey[200],
                boxShadow: [
                  BoxShadow(
                      offset: Offset(0, 10),
                      blurRadius: 50,
                      color: Color(0xffEEEEEE))
                ],
              ),
              alignment: Alignment.center,
              child: TextField(
                controller: Password,
                obscureText: true,
                cursorColor: Color(0xffF5591F),
                decoration: InputDecoration(
                    icon: Icon(
                      Icons.vpn_key,
                      color: Color(0xffF5591F),
                    ),
                    hintText: "Password",
                    enabledBorder: InputBorder.none,
                    focusedBorder: InputBorder.none),
              ),
            ),

            //  floatingActionButton: FloatingActionButton(
            //    onPressed: postData,
            //   backgroundColor: Colors.green,
            //   child: const Icon(Icons.navigation),
            //  ),

            GestureDetector(
              onTap: () => {
                postData(Username.text, Password.text, FirstName.text,
                    LastName.text, Email.text)
              },
              child: Container(
                margin: EdgeInsets.only(left: 20, right: 20, top: 20),
                padding: EdgeInsets.only(left: 20, right: 20),
                alignment: Alignment.center,
                height: 54,
                decoration: BoxDecoration(
                  gradient: LinearGradient(colors: [
                    (new Color(0xffF5591F)),
                    (new Color(0xffF2861E))
                  ], begin: Alignment.centerLeft, end: Alignment.centerRight),
                  borderRadius: BorderRadius.circular(50),
                  boxShadow: [
                    BoxShadow(
                        offset: Offset(0, 10),
                        blurRadius: 50,
                        color: Color(0xffEEEEEE))
                  ],
                ),
                child: Text(
                  "REGISTER",
                  style: TextStyle(color: Colors.white),
                ),
              ),
            ),

            Container(
              margin: EdgeInsets.only(top: 10),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text("Already Member ?"),
                  GestureDetector(
                    onTap: () => {Navigator.pop(context)},
                    child: Text(
                      " Login Now",
                      style: TextStyle(color: Color(0xffF5591F)),
                    ),
                  )
                ],
              ),
            )
          ],
        ),
      ),
    );
  }
}
