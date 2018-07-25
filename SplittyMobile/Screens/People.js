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

//creating a class, this class inherits from compnent which is from react lib^^
//export
export default class People extends Component {

  render() {//spec
    return (
      <View style={styles.container}>

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
