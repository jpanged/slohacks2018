'use strict';
import React, { Component } from 'react';
import {
  AppRegistry,
  Dimensions,
  StyleSheet,
  Text,
  TouchableOpacity,
  View
} from 'react-native';
import { RNCamera } from 'react-native-camera';
import Assign from './Screens/Assign';
import Camera from './Screens/Camera';
import People from './Screens/People';
import Results from './Screens/Results';
import {createStackNavigator} from 'react-navigation';// this is a lib for multiple screens

//Basically just the router
// makes all its children injecting stuff-> under navigation
const SimpleStack = createStackNavigator(
  {
    //lets the router know that these screens exist (in a stack)
    Camera: {
      screen: Camera,
    },
    Assign: {
      screen: Assign,//the val is matching ur imports
    },
    People: {

      screen: People,
    },
    Results:{
      screen: Results,
    }
  },
  {
    initialRouteName: 'Camera',
  }
);

export default SimpleStack; //:)
