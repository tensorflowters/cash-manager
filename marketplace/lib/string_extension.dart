import 'package:flutter_secure_storage/flutter_secure_storage.dart';

extension StringExtension on String {
  String capitalize() {
    return "${this[0].toUpperCase()}${this.substring(1).toLowerCase()}";
  }

  String replace() {
    const char = ['{', '}', '[', ']', '.,'];

    String input = this;
      for (int i = 0; i < char.length; i++) {
        input = input.replaceAll(char[i], "");
      }
    return input;
  }
}
