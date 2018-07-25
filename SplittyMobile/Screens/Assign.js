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
// import {header} from 'react-native-elements';

//creating a class, this class inherits from compnent which is from react lib^^
//export
export default class Assign extends Component {

  render() {//spec
    return (
      <View>
      { /*
      <Header
      placement="left"
      leftComponent={{ icon: 'menu', color: '#FFF' }}
      centerComponent={{ text: 'MY TITLE', style: { color: '#fff' } }}
      rightComponent={{ icon: 'home', color: '#fff' }}
      />
      */}
      </View>

    );
  }

}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
    backgroundColor: 'white',
    justifyContent: 'flex-end',
    alignItems: 'center'
  },
});
