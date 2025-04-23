import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';
import 'package:location/location.dart' as gps;
import 'package:geocoding/geocoding.dart' as geo;

import 'dart:typed_data';
import 'dart:convert';
import 'dart:io';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Vizhi AI',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: BluetoothApp(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class BluetoothApp extends StatefulWidget {
  @override
  _BluetoothAppState createState() => _BluetoothAppState();
}

class _BluetoothAppState extends State<BluetoothApp> {
  BluetoothConnection? connection;
  Socket? socket;
  String status = " Connecting to Vizhi AI...";

  @override
  void initState() {
    super.initState();
    connectToBackendSocket();
    autoConnectToBluetooth();
  }

  void connectToBackendSocket() async {
    try {
      socket = await Socket.connect('192.168.80.245', 8000);
      print(' Connected to Python backend!');
    } catch (e) {
      print(' Could not connect to backend: $e');
    }
  }

  void autoConnectToBluetooth() async {
    try {
      String targetAddress = "64:B7:08:D2:ED:CA"; //
      connection = await BluetoothConnection.toAddress(targetAddress);
      setState(() {
        status = " Connected to Vizhi AI";
      });
      print('Connected to the device');
      startSendingGPS();
    } catch (e) {
      print('Error: $e');
      setState(() {
        status = " Connection Failed";
      });
    }
  }

  void startSendingGPS() async {
    gps.Location location = gps.Location();

    bool serviceEnabled = await location.serviceEnabled();
    if (!serviceEnabled) {
      serviceEnabled = await location.requestService();
      if (!serviceEnabled) return;
    }

    gps.PermissionStatus permissionGranted = await location.hasPermission();
    if (permissionGranted == gps.PermissionStatus.denied) {
      permissionGranted = await location.requestPermission();
      if (permissionGranted != gps.PermissionStatus.granted) return;
    }

    location.onLocationChanged.listen((gps.LocationData currentLocation) async {
      double lat = currentLocation.latitude ?? 0.0;
      double lon = currentLocation.longitude ?? 0.0;

      List<geo.Placemark> placemarks =
      await geo.placemarkFromCoordinates(lat, lon);
      geo.Placemark place = placemarks[0];

      String address = [
        place.name,
        place.street,
        place.subLocality,
        place.locality,
        place.subAdministrativeArea,
        place.administrativeArea,
        place.postalCode,
        place.country
      ].where((e) => e != null && e.isNotEmpty).join(', ');

      Map<String, dynamic> gpsData = {
        "lat": lat,
        "lon": lon,
        "address": address,
      };

      String message = jsonEncode(gpsData);
      print("Sending: $message");

      // Send to ESP32 via Bluetooth
      if (connection != null && connection!.isConnected) {
        connection!.output.add(Uint8List.fromList((message + "\n").codeUnits));
        await connection!.output.allSent;
      }

      // Send to Python backend
      if (socket != null) {
        socket!.write(message + "\n");
        print(" Sent to Python backend");
      }
    });
  }

  @override
  void dispose() {
    connection?.dispose();
    socket?.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: Text(
          status,
          style: TextStyle(color: Colors.greenAccent, fontSize: 24),
        ),
      ),
    );
  }
}
