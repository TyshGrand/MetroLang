import 'package:flutter/material.dart';
import 'package:frontend/styles/colors.dart';

class MetroLangTheme {

  static ThemeData darkTheme = ThemeData(

    colorScheme: ColorScheme.fromSeed(seedColor: MetroLangColors.primary),
    useMaterial3: true,
    textTheme: TextTheme(
      titleLarge: TextStyle(
        color: MetroLangColors.mainTitle,
        fontSize: 40,
      ),
      headlineLarge: TextStyle(
        color: MetroLangColors.mainTitle,
        fontSize: 16
      ),
      headlineMedium: TextStyle(
        color: MetroLangColors.mainTitle,
        fontSize: 14
      ),
      headlineSmall: TextStyle(
        color: MetroLangColors.hintText,
        fontSize: 14
      )
    )
  );
}