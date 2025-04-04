import 'package:flutter/material.dart';

import '../../styles/colors.dart';

AppBar metroLangAppBar(context, String title, void Function() onMenuPressed) {
  return AppBar(
// TRY THIS: Try changing the color here to a specific color (to
// Colors.amber, perhaps?) and trigger a hot reload to see the AppBar
// change color while the other colors stay the same.
    backgroundColor: MetroLangColors.primary,
// Here we take the value from the MyHomePage object that was created by
// the App.build method, and use it to set our appbar title.
    title: Text(
      title,
      style: Theme.of(context).textTheme.titleLarge,
    ),
    leading: Builder(
      builder: (context) {
        return IconButton(
          icon: const Icon(Icons.menu),
          color: MetroLangColors.mainTitle,
          onPressed: onMenuPressed
        );
      },
    ),
  );
}

Drawer metroLangDrawer(context) {
  return Drawer(
    child: ListView(
// Important: Remove any padding from the ListView.
      padding: EdgeInsets.zero,
      children: [
        DrawerHeader(
          decoration: const BoxDecoration(color: MetroLangColors.primary),
          child: Text(
            'Drawer Header',
            style: Theme.of(context).textTheme.headlineMedium,
          ),
        ),
        ListTile(
          title: const Text('Item 1'),
          onTap: () {
// Update the state of the app.
// ...
          },
        ),
        ListTile(
          title: const Text('Item 2'),
          onTap: () {
// Update the state of the app.
// ...
          },
        ),
      ],
    ),
  );
}
