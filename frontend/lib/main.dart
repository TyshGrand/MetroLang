import 'package:flutter/material.dart';
import 'package:frontend/styles/theme.dart';
import 'package:frontend/views/sidebar_view.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MetroLang',
      debugShowCheckedModeBanner: false,
      theme: MetroLangTheme.darkTheme,
      home:  SideBarView(title: 'MetroLang')
    );
  }
}