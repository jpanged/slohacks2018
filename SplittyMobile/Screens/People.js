'use strict';
import React, { Component } from 'react';
import {
  AppRegistry,
  Dimensions,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  FlatList,
  Image,
  TextInput,
  KeyboardAvoidingView,
  Keyboard
} from 'react-native';
const trash = require('../Images/trash.png');
const plus = require('../Images/plus.png');
import { SafeAreaView } from 'react-navigation';
const isIPhoneX = Dimensions.get("window").height === 812;


const colors = ["#6CE6C1","#8594E8","#6CC0E6","#E594FF","#F1FF94"]



//creating a class, this class inherits from compnent which is from react lib^^
//export
export default class People extends Component {
  static navigationOptions = ({ navigation }) => {
    return {
      title: navigation.getParam('otherParam', 'A Nested Details Screen'),
    }
  }

  componentDidMount () {
    this.keyboardWillShowListener = Keyboard.addListener('keyboardWillShow', this._keyboardWillShow);
    this.keyboardWillHideListener = Keyboard.addListener('keyboardWillHide', this._keyboardWillHide);
  }

  componentWillUnmount () {
    this.keyboardWillShowListener.remove();
    this.keyboardWillHideListener.remove();
  }

  _keyboardWillShow = () => {
    this.setState({marginBottom: 16})
  }

  _keyboardWillHide = () => {
    this.setState({marginBottom: Dimensions.get('window').height === 812 ? 40 : 16})
  }

  state = {
    people: [{key: 'Abd', name: 'Abdallah AbuHashem', color: '#6CE6C1'},
             {key: 'Ros', name: 'Rosanne Hu', color: '#8594E8'}],
    newName: "",
    marginBottom: Dimensions.get('window').height === 812 ? 40 : 16
  }

  deleteUser = (key) => {
    var newList = this.state.people.slice();
    var idx = -1;
    for(var i = 0; i < newList.length; i++) {
      if (newList[i].key === key) {
        idx = i;
        break;
      }
    }
    if (idx != -1) {
      newList.splice(idx, 1);
    }
    this.setState({people: newList});
  }

  renderName = (item) => {
    return (
      <View style={styles.itemContainer}>
        <View style={styles.nameContainer}>
          <View style={[styles.initialsView, {backgroundColor: item.color}]}>
            <Text style={styles.bubbleText}> {item.key} </Text>
          </View>
          <Text style={styles.bubbleText}>  {item.name} </Text>
        </View>
        <TouchableOpacity onPress={() => this.deleteUser(item.key)}>
          <Image source={trash} style={styles.trash} />
        </TouchableOpacity>
      </View>
    )

  }

  addName = () => {
    if (this.state.newName === "") return;
    var newList = this.state.people.slice();
    newList.push({key: this.state.newName.substring(0,3), name: this.state.newName, color: colors[newList.length]});
    this.setState({people: newList, newName: ""});
  }

  render() {//spec
    return (
      <KeyboardAvoidingView
        style={styles.container}
        behavior="padding"
        keyboardVerticalOffset ={isIPhoneX ? 85 : 65}>
        <FlatList
          data={this.state.people}
          style={styles.list}
          renderItem={({item}) => this.renderName(item)}
        />
        <View style={[styles.addContainer, {marginBottom: this.state.marginBottom}]}>
          <TextInput
            style={styles.addName}
            placeholder={"Add a name..."}
            placeholderTextColor={"#BDBDBD"}
            value = {this.state.newName}
            onChangeText={(text) => this.setState({newName: text})}
          />
          <TouchableOpacity onPress={() => this.addName()}>
            <Image style={styles.add} source={plus}/>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
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
  list: {
    flex: 1,
    width: '100%',
    paddingRight: 16,
    paddingLeft: 16
  },
  itemContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: 20,
    paddingBottom: 20,
    borderBottomWidth: 0.5,
    borderBottomColor: '#BDBDBD'
  },
  initialsView: {
    width: 55,
    height: 55,
    borderRadius: 27.5,
    borderWidth: 1,
    borderColor: '#9f9f9f',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 10
  },
  bubbleText: {
    fontFamily: "System",
    fontSize: 17,
    fontWeight: "500",
    color: "#4E4E4E"
  },
  nameContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  trash: {
    width: 31,
    height: 35
  },
  addContainer: {
    width: '100%',
    flexDirection: 'row',
    paddingRight: 16,
    paddingLeft: 16,
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: Dimensions.get('window').height === 812 ? 40 : 16
  },
  add: {
    width: 30,
    height: 30
  },
  addName: {
    flex: 1,
    paddingLeft: 8,
    borderBottomWidth: 0.5,
    borderBottomColor: '#BDBDBD',
    marginRight: 10
  }
});
