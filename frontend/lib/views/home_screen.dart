import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../styles/colors.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return           Container(
      padding: EdgeInsets.all(20),
      // Center is a layout widget. It takes a single child and positions it
      // in the middle of the parent.
      child: Column(

        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: <Widget>[
          Expanded(
            child: Center(
              child: Text(
                'Welcome to MetroLang, your personal AI assistant to help you get the data you want',
                style: Theme.of(context).textTheme.headlineMedium,),
            ),
          ),
          TextFormField(

            style: Theme.of(context).textTheme.headlineLarge,

            decoration: InputDecoration(
              hintText: 'Ask you questions here',
              hintStyle: Theme.of(context).textTheme.headlineSmall,
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(25.0),
                borderSide: BorderSide(
                  color: MetroLangColors.primary,
                ),
              ),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(25.0),
                borderSide: BorderSide(
                  color: MetroLangColors.hintText,
                  width: 2.0,
                ),
              ),
            ),
          ),
        ],
      ),
    );

  }
}
