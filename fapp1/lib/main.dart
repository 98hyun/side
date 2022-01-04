import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:marquee/marquee.dart';

// run main.dart
void main() => runApp(MyApp());

// color set
List<Color> getColor(String setname) {
  List<Color> colorset1 = [Colors.red, Colors.yellow];
  List<Color> colorset2 = [Color(0xffEDE574), Color(0xffE1F5C4)];
  List<Color> colordefault = [Colors.greenAccent, Colors.blueAccent];
  if (setname == "Set1") {
    return colorset1;
  } else if (setname == "Set2") {
    return colorset2;
  } else {
    return colordefault;
  }
}

// myapp
class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'First App',
      home: SecondPage(),
    );
  }
}

// led
class FirstPage extends StatelessWidget {
  final String text;
  final Shader shader;
  double speed = 100.0;
  FirstPage(
      {Key? key, required this.shader, required this.text, required this.speed})
      : super(key: key);
  @override
  Widget build(BuildContext context) {
    SystemChrome.setPreferredOrientations([
      // DeviceOrientation.portraitUp,
      DeviceOrientation.landscapeLeft,
      DeviceOrientation.landscapeRight,
    ]);
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
          elevation: 0,
          toolbarHeight: 40,
          backgroundColor: Colors.black,
          leading: IconButton(
              icon: Icon(Icons.arrow_back),
              onPressed: () {
                Navigator.pop(context, false);
              })),
      body: Marquee(
        text: text,
        style: TextStyle(fontSize: 80, foreground: Paint()..shader = shader),
        velocity: speed,
      ),
    );
  }
}

// custom text,color
class SecondPage extends StatefulWidget {
  const SecondPage({Key? key}) : super(key: key);

  @override
  _SecondPageState createState() => _SecondPageState();
}

class _SecondPageState extends State<SecondPage> {
  final _textController = TextEditingController();

  List setsname = ["Set1", "Set2"];
  var setname = "Set1";
  String usermind = "what's on your mind? ";
  double _n = 100.0;

  void add() {
    setState(() {
      _n += 1.0;
    });
  }

  void minus() {
    setState(() {
      if (_n != 0) _n -= 1.0;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Flexible(
              child: Container(
                height: 100,
                margin: EdgeInsets.fromLTRB(0, 0, 0, 30),
                decoration: BoxDecoration(
                    color: Colors.black,
                    borderRadius: BorderRadius.all(Radius.circular(20))),
                child: Center(
                    child: Marquee(
                  text: usermind,
                  style: TextStyle(
                      fontSize: 40,
                      foreground: Paint()
                        ..shader = LinearGradient(colors: getColor(setname))
                            .createShader(
                                Rect.fromLTWH(0.0, 20.0, 150.0, 20.0))),
                  velocity: _n,
                )),
              ),
            ),
            Flexible(
              child: TextField(
                controller: _textController,
                onChanged: (value) => setState(() {
                  usermind = _textController.text;
                }),
                decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    hintText: "what's on your mind?",
                    suffixIcon: IconButton(
                        onPressed: () {
                          _textController.clear();
                        },
                        icon: Icon(Icons.clear))),
              ),
            ),
            Flexible(
              child: DropdownButton(
                alignment: Alignment.center,
                value: setname,
                items: setsname
                    .map((name) => DropdownMenuItem(
                          child: Text(name, textAlign: TextAlign.center),
                          value: name,
                        ))
                    .toList(),
                onChanged: (value) {
                  setState(() {
                    setname = value.toString();
                  });
                },
              ),
            ),
            Flexible(
                child: Center(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  FloatingActionButton(
                    heroTag: null,
                    onPressed: add,
                    child: Icon(
                      Icons.add,
                      color: Colors.black,
                    ),
                    backgroundColor: Colors.white,
                  ),
                  Text(
                    _n.toStringAsFixed(1),
                    style: TextStyle(fontSize: 13),
                  ),
                  FloatingActionButton(
                    heroTag: null,
                    onPressed: minus,
                    child: Icon(
                      Icons.remove,
                      color: Colors.black,
                    ),
                    backgroundColor: Colors.white,
                  )
                ],
              ),
            )),
            Flexible(
              child: ElevatedButton(
                child: Text('Apply'),
                onPressed: () async {
                  //We change to landscape before going to another page!
                  SystemChrome.setPreferredOrientations([
                    DeviceOrientation.landscapeLeft,
                    DeviceOrientation.landscapeRight
                  ]);

                  await Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (context) => FirstPage(
                              shader: LinearGradient(colors: getColor(setname))
                                  .createShader(
                                      Rect.fromLTWH(0.0, 20.0, 150.0, 20.0)),
                              text: usermind,
                              speed: _n,
                            )),
                  );
                  //We wait for the second screen to pop from anywhere
                  SystemChrome.setPreferredOrientations([
                    DeviceOrientation.portraitDown,
                    DeviceOrientation.portraitUp
                  ]);
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
