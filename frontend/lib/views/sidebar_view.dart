import 'package:collapsible_sidebar/collapsible_sidebar.dart';
import 'package:collapsible_sidebar/collapsible_sidebar/collapsible_item.dart';
import 'package:flutter/material.dart';
import 'package:frontend/views/widgets/metrolang_appbar.dart';

import '../styles/colors.dart';
import 'history_screen.dart';
import 'home_screen.dart';

class SideBarView extends StatefulWidget {
  const SideBarView({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<SideBarView> createState() => _SideBarViewState();
}

class _SideBarViewState extends State<SideBarView> {
  late List<CollapsibleItem> _items;
  bool _isCollapsed = true;
  late PageController _pageController;

  List<CollapsibleItem> _generateSideBarItems() {
    return [CollapsibleItem(text: "Home",
        icon: Icons.home,
        isSelected: true,
        onPressed: () =>_navigateToPage(0)),
    CollapsibleItem(text: "History",
        icon: Icons.history,
        onPressed: () =>_navigateToPage(1)),
  ];
  }

  @override
  initState() {
    super.initState();
    _pageController = PageController();
    _items = _generateSideBarItems();
  }

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      backgroundColor: MetroLangColors.mainBackground,


      appBar: metroLangAppBar(context, widget.title, ()=>setState(() {
        _isCollapsed = !_isCollapsed;
      })),
      drawer: metroLangDrawer(context),
      body: Row(
        children: [
          CollapsibleSidebar(
              items: _items,
              isCollapsed: _isCollapsed,
              showTitle: false,
              selectedIconColor: MetroLangColors.primary,
              unselectedIconColor: MetroLangColors.hintText,
              showToggleButton: false,
              borderRadius: 0,
              topPadding: 0,
              screenPadding: 0,
              sidebarBoxShadow: [],
              body: Container()),
          Expanded(child: PageView(
            controller: _pageController,
            children: const [
              HomeScreen(),
              HistoryScreen()
            ],
          )),
        ],
      ),
    );
  }

  _navigateToPage(int i) {
    setState(() {
      _pageController.jumpToPage(i);

      // _pageController.animateToPage(i,  duration: Duration(milliseconds: 300),
      //   curve: Curves.easeInOut,);
    });

  }
}
