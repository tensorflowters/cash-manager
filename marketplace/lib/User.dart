class User {
  late String _username;
  late String _email;
  late int _userid;

  User() {
    _userid = -1;
    _username = "";
    _email = "";
  }

  setUser(User u) {
    _userid = u._userid;
    _username = u._username;
    _email = u._email;
  }

  void setEmail(String email) {
    _email = email;
  }

  void setUsername(String username) {
    _username = username;
  }

  void setUserID(int userID) {
    _userid = userID;
  }

  int getUserID() {
    return _userid;
  }
}
