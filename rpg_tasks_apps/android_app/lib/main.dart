import 'package:flutter/material.dart';
import 'screens/inicio_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(title: 'RPG Tasks', debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: const Color.fromARGB(255, 221, 218, 170), brightness: Brightness.light)),
      home: const InicioScreen(), //LLeva a la pantalla de Inicio de la app
    );
  }
}
