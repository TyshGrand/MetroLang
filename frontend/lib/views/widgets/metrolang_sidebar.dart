import 'package:collapsible_sidebar/collapsible_sidebar/collapsible_item.dart';
import 'package:flutter/cupertino.dart';

class MetroLangSideBar extends StatefulWidget {
  const MetroLangSideBar({super.key});

  @override
  State<MetroLangSideBar> createState() => _MetroLangSideBarState();
}

class _MetroLangSideBarState extends State<MetroLangSideBar> {
  late List<CollapsibleItem> _items;
  bool _isCollapsed = true;
  late PageController _pageController;

  @override
  Widget build(BuildContext context) {
    return const Placeholder();
  }
}
