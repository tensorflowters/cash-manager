import 'package:awesome_snackbar_content/awesome_snackbar_content.dart';
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:http/http.dart';
import 'dart:convert';
import "string_extension.dart";
import 'package:flutter_secure_storage/flutter_secure_storage.dart';


class Home extends StatefulWidget {
  @override
  State<StatefulWidget> createState() => InitState();
}

class InitState extends State<Home> {

  final storage = const FlutterSecureStorage();


  @override
  Widget build(BuildContext) {
    return initWidget();
  }


  Widget initWidget() {

    TextEditingController Username = new TextEditingController();
    TextEditingController FirstName = new TextEditingController();
    TextEditingController LastName = new TextEditingController();
    TextEditingController Email = new TextEditingController();
    TextEditingController Password = new TextEditingController();
    TextEditingController ConfirmPassword = new TextEditingController();
    var confirmPass;


    getUser() async {
      String? userId = await storage.read(key: "userId");
      String? accessToken = await storage.read(key: "accessToken");

      Response response = await get(
        Uri.parse("${dotenv.env['PATH_HOST']!}/api/authenticated/users/" + "$userId"),
        headers: {
          "Content-type": "application/json",
          "Authorization": "Bearer " + "$accessToken"
        },
      );
      var result = jsonDecode(response.body.toString());

      if (response.statusCode == 200) {
        /*  ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            elevation: 0,
            behavior: SnackBarBehavior.floating,
            backgroundColor: Colors.transparent,
            content: AwesomeSnackbarContent(
              title: 'Password Changed',
              message:
              'You\'ve Successfully Changed your password.',
              contentType: ContentType.success,
            ),
          ));*/
        return response.body.toString();
      } else {
        //   print(result.toString().replace());
        /*  ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            elevation: 0,
            behavior: SnackBarBehavior.floating,
            backgroundColor: Colors.transparent,
            content: AwesomeSnackbarContent(
              title: 'Error !',
              message: result.toString().replace().capitalize(),
              contentType: ContentType.warning,
            ),
          ));*/
        return response.statusCode;
      }
    }

    changePassword(String Password, ConfirmPassword) async {

      String? userId = await storage.read(key: "userId");
      String? accessToken = await storage.read(key: "accessToken");
      final body = {
        "password": Password,
      };

      if (Password == ConfirmPassword) {
        Response response = await patch(
          Uri.parse("${dotenv.env['PATH_HOST']!}/api/authenticated/users/" + "$userId" + "/set_password"),
          headers: {
            "Content-type": "application/json",
            "Authorization": "Bearer " + "$accessToken",
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
                  title: 'Password Changed',
                  message:
                  'You\'ve Successfully Changed your password.',
                  contentType: ContentType.success,
                ),
              ));
          return response.body.toString();
        } else {
          //   print(result.toString().replace());
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
          return response.statusCode;
        }
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              elevation: 0,
              behavior: SnackBarBehavior.floating,
              backgroundColor: Colors.transparent,
              content: AwesomeSnackbarContent(
                title: 'Error !',
                message: "Les mots de passe doivent être identique.",
                contentType: ContentType.warning,
              ),
            ));
      }
    }

    return Scaffold(
      body: FutureBuilder(
        future: getUser(),
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            // You can access the response data here
            var data = snapshot.data;
            var userinfo = jsonDecode(data.toString());
            print(userinfo);
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
                              child: Image.asset("images/profile.png"),
                              height: 150,
                              width: 150,
                            ),
                            Container(
                              margin: EdgeInsets.only(right: 20, top: 20),
                              alignment: Alignment.bottomRight,
                              child: Text(
                                "Profile",
                                style: TextStyle(
                                    fontSize: 20,
                                    color: Colors.white
                                ),
                              ),
                            ),
                            Container(
                              margin: EdgeInsets.only(right: 20, top: 20),
                              alignment: Alignment.bottomRight,
                              child: Text(
                                userinfo['username'],
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
                        readOnly: true,
                        controller: FirstName,
                        cursorColor: Color(0xffF5591F),
                        decoration: InputDecoration(
                            icon: Icon(
                              Icons.person,
                              color: Color(0xffF5591F),
                            ),
                            hintText: userinfo['first_name'],
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
                        readOnly: true,
                        controller: LastName,
                        cursorColor: Color(0xffF5591F),
                        decoration: InputDecoration(
                            icon: Icon(
                              Icons.person,
                              color: Color(0xffF5591F),
                            ),
                            hintText: userinfo['last_name'],
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
                        readOnly: true,
                        controller: Email,
                        cursorColor: Color(0xffF5591F),
                        decoration: InputDecoration(
                            icon: Icon(
                              Icons.email,
                              color: Color(0xffF5591F),
                            ),
                            hintText: userinfo['email'],
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
                      child: TextFormField(
                        validator: (String? value) {
                          confirmPass = value;
                          if (value!.isEmpty) {
                            return "Please Enter New Password";
                          } else if (value.length < 8) {
                            return "Password must be atleast 8 characters long";
                          } else {
                            return null;
                          }
                        },
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
                      child: TextFormField(
                        validator: (String? value) {
                          if (value!.isEmpty) {
                            return "Please Re-Enter New Password";
                          } else if (value.length < 8) {
                            return "Password must be atleast 8 characters long";
                          } else if (value != confirmPass) {
                            return "Password must be same as above";
                          } else {
                            return null;
                          }
                        },
                        controller: ConfirmPassword,
                        obscureText: true,
                        cursorColor: Color(0xffF5591F),
                        decoration: InputDecoration(
                            icon: Icon(
                              Icons.vpn_key,
                              color: Color(0xffF5591F),
                            ),
                            hintText: "Enter New Password",
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
                        changePassword(Password.text, ConfirmPassword.text),
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
                          "Change Password",
                          style: TextStyle(color: Colors.white),
                        ),
                      ),
                    ),


                  ],
                ),
              ),
            );
          } else if (snapshot.hasError) {
            return Text("${snapshot.error}");
          }
          // Show a loading indicator while waiting for the response
          return CircularProgressIndicator();
        },
      ),
    );
  }
}