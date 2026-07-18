// dart format off
import 'package:flutter/material.dart';
import '../models/user_model.dart';
import '../api_services/user_services.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

  bool _isLoading = false;

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _usuarioController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;

  @override
  void dispose() {
    _usuarioController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
  

  //De momento voy a dejar esto sin implementar
  @override
  Widget build(BuildContext context) {
    throw UnimplementedError(); 
  }

}