import 'package:awesome_snackbar_content/awesome_snackbar_content.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'signup_screen.dart';
import 'home.dart';
import 'dart:convert';
import "string_extension.dart";
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class LoginScreen extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => InitState();
}

class InitState extends State<LoginScreen> {

  final storage = new FlutterSecureStorage();

  @override
  Widget build(BuildContext) {
    return initWidget();
  }

  Widget initWidget() {
    TextEditingController Username = new TextEditingController();
    TextEditingController Password = new TextEditingController();

    loginAPI(String Username, Password) async {
      final body = {
        "username": Username,
        "password": Password
      };

      Response response = await post(Uri.parse("http://127.0.0.1:8000/api/login"),
        headers: {
          "Content-type": "application/json",
        },
        body: json.encode(body),
      );
      var result = jsonDecode(response.body.toString());
      if (response.statusCode == 202) {
        ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              elevation: 0,
              behavior: SnackBarBehavior.floating,
              backgroundColor: Colors.transparent,
              content: AwesomeSnackbarContent(
                title: 'Welcom $Username!',
                message:
                'You\'ve Successfully Logged In.',
                contentType: ContentType.success,
              ),
            ));
        Navigator.push(context, MaterialPageRoute(
          builder: (context) => Home(),
        ));
      //  print(result['user']['id']);
        await storage.write(key: "userId", value: result['user']['id'].toString());
        await storage.write(key: "accessToken", value: result['access']);
        await storage.write(key: "refreshToken", value: result['refresh']);
      } else {
        print(result.toString().replace());
        ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              elevation: 0,
              behavior: SnackBarBehavior.floating,
              backgroundColor: Colors.transparent,
              content: AwesomeSnackbarContent(
                title: 'Error !',
                message: result.toString().replace().capitalize(),
                contentType: ContentType.warning,
              ),
            ));
      }

    }

    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          children: [
            Container(
              height: 300,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.only(bottomLeft: Radius.circular(90)),
                color: Color(0xffF5591F),
                gradient: LinearGradient(
                  colors: [(new Color(0xffF5501F)), (new Color(0xffF2861E))],
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter
                )
              ),
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Container(
                      margin: EdgeInsets.only(top: 50),
                      child: Image.asset("images/app_logo.png"),
                        height: 200,
                        width: 200,
                    ),
                    Container(
                      margin: EdgeInsets.only(right: 20, top: 20),
                        alignment: Alignment.bottomRight,
                      child: Text(
                        "Login",
                        style: TextStyle(
                          fontSize: 20,
                          color: Colors.white
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
                boxShadow: [BoxShadow(
                  offset: Offset(0, 10),
                  blurRadius: 50,
                  color: Color(0xffEEEEEE)
                )],
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
                  hintText: "Enter Username",
                  enabledBorder: InputBorder.none,
                  focusedBorder: InputBorder.none
                ),
              ),
            ),

            Container(
              margin: EdgeInsets.only(left: 20, right: 20, top: 20),
              padding: EdgeInsets.only(left: 20, right: 20),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(50),
                color: Colors.grey[200],
                boxShadow: [BoxShadow(
                  offset: Offset(0, 10),
                  blurRadius: 50,
                  color: Color(0xffEEEEEE)
                )],
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
                  hintText: "Enter Password",
                  enabledBorder: InputBorder.none,
                  focusedBorder: InputBorder.none
                ),
              ),
            ),

            Container(
              margin: EdgeInsets.only(top: 20, right: 20),
                alignment: Alignment.centerRight,
              child: GestureDetector(
                child: Text("Forget Password"),
                onTap: () => {

                },
              ),
            ),
        GestureDetector(
          onTap: () => {
          loginAPI(Username.text, Password.text)
          },
          child: Container(
            margin: EdgeInsets.only(left: 20, right: 20, top: 70),
            padding: EdgeInsets.only(left: 20, right: 20),
            alignment: Alignment.center,
            height: 54,
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [(new Color(0xffF5591F)), (new Color(0xffF2861E))],
                begin: Alignment.centerLeft,
                end: Alignment.centerRight
              ),
              borderRadius: BorderRadius.circular(50),
              boxShadow: [BoxShadow(
                  offset: Offset(0, 10),
                  blurRadius: 50,
                  color: Color(0xffEEEEEE)
              )],
            ),
            child: Text(
              "LOGIN",
              style: TextStyle(
                color: Colors.white
              ),
            ),
          ),
        ),
            Container(
              margin: EdgeInsets.only(top: 10),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text("Don't Have Account ?"),
                  GestureDetector(
                    onTap: () => {
                      Navigator.push(context, MaterialPageRoute(
                          builder: (context) => SignUpScreen()
                      ))

                    },
                    child: Text(
                      " Register Now",
                      style: TextStyle(
                        color: Color(0xffF5591F)
                      ),
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