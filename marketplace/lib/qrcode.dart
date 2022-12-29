// ignore_for_file: unnecessary_new

import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:qr_code_scanner/qr_code_scanner.dart';
import 'dart:developer';
import 'package:marketplace/article_pop_up.dart';
import 'package:marketplace/Article.dart';
import 'package:marketplace/main.dart';
import 'dart:io';
import 'package:http/http.dart' as http;

class QRViewExample extends StatefulWidget {
  const QRViewExample({Key? key}) : super(key: key);
  @override
  State<StatefulWidget> createState() => _QRViewExampleState();
}

class _QRViewExampleState extends State<QRViewExample> {
  var valueText = "scan code";
  Barcode? result;
  QRViewController? controller;
  final GlobalKey qrKey = GlobalKey(debugLabel: 'QR');

  // In order to get hot reload to work we need to pause the camera if the platform
  // is android, or resume the camera if the platform is iOS.
  @override
  void reassemble() {
    super.reassemble();
    if (Platform.isAndroid) {
      controller!.pauseCamera();
    }
    controller!.resumeCamera();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: <Widget>[
          Container(
            height: MediaQuery.of(context).size.height - 83,
            child: _buildQrView(context),
          )
        ],
      ),
    );
  }

  Widget _buildQrView(BuildContext context) {
    // For this example we check how width or tall the device is and change the scanArea and overlay accordingly.
    var scanArea = (MediaQuery.of(context).size.width < 400 ||
            MediaQuery.of(context).size.height < 400)
        ? 150.0
        : 300.0;
    // To ensure the Scanner view is properly sizes after rotation
    // we need to listen for Flutter SizeChanged notification and update controller
    return QRView(
      key: qrKey,
      onQRViewCreated: _onQRViewCreated,
      overlay: QrScannerOverlayShape(
          borderColor: Colors.red,
          borderRadius: 10,
          borderLength: 30,
          borderWidth: 10,
          cutOutSize: scanArea),
      onPermissionSet: (ctrl, p) => _onPermissionSet(context, ctrl, p),
    );
  }

  void _onQRViewCreated(QRViewController controller) {
    setState(() {
      this.controller = controller;
    });

    Widget _buildPopupDialog(BuildContext context, bool state) {
      return new AlertDialog(
        title: (state
            ? const Text('Confirmation d\'ajout !')
            : const Text('Erreur...')),
        content: new Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            (state
                ? const Text("Votre article à bien été ajouté au panier !")
                : const Text(
                    'Cette article n\'existe pas, veuillez en scanner un autre')),
          ],
        ),
        actions: <Widget>[
          new ElevatedButton(
            onPressed: () {
              controller.resumeCamera();
              Navigator.of(context).pop("close");
            },
            child: const Text('Fermer'),
          ),
        ],
      );
    }

    controller.scannedDataStream.listen((scanData) {
      var ok = 0;
      setState(() {
        result = scanData;
        /* _RandomWordsState._currentIndex = 2;
        debugPrint('movieTitle: ${_RandomWordsState._currentIndex}');

        _RandomWordsState.scanArticleId = result!.code.toString(); */
        var response = http
            .get(Uri.parse(
                '${dotenv.env['PATH_HOST']!}/api/articles/${result!.code.toString()}'))
            .then(
              (value) => {
                controller.pauseCamera(),
                if (value.statusCode == 200)
                  {
                    // ignore: use_build_context_synchronously
                    Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) => MyWidget(
                                  result!.code.toString(),
                                ))).then((value) => {
                          log((value.toString() == "Ok").toString()),
                          if (value.toString() == "Ok")
                            {
                              showDialog(
                                context: context,
                                builder: (BuildContext context) =>
                                    _buildPopupDialog(context, true),
                              )
                            }
                        }),
                  }
                else if (value.statusCode == 404)
                  {
                    showDialog(
                      context: context,
                      builder: (BuildContext context) =>
                          _buildPopupDialog(context, false),
                    ),
                  }
                else
                  {
                    throw Error(),
                  }
              },
            );
      });
    });
  }

  void _onPermissionSet(BuildContext context, QRViewController ctrl, bool p) {
    log('${DateTime.now().toIso8601String()}_onPermissionSet $p');
    if (!p) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('no Permission')),
      );
    }
  }

  @override
  void dispose() {
    controller?.dispose();
    super.dispose();
  }
}
