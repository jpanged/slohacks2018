'use strict';
import React, { Component } from 'react';
import {
  AppRegistry,
  Dimensions,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  CameraRoll
} from 'react-native';
import { RNCamera } from 'react-native-camera';
import ImgToBase64 from 'react-native-image-base64';

//creating a class, this class inherits from compnent which is from react lib^^
//export
export default class Camera extends Component {

  static navigationOptions = ({navigation}) => { //curly brackets gotta match
    return {
      header: null, // we changing the default options bc it looks weird
    }
  }

  //constructor
  //componentWillMount
  //render
  //componentDidMount

  uploadPhoto(PicturePath) {

    ImgToBase64.getBase64String(PicturePath)
      .then(base64String => {
        var result = fetch('http://10.105.73.133:8000/shopperHelper/addReceipt', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'text/html',
          },
          body: 'data=' + base64String
        });
      });
  // .then(response => checkStatus(response))
  // .then(response => response.json())
  // .catch(e => { throw e; });
  //
  // return result;


    // const data = new FormData();
    // data.append('name', 'testName'); // you can append anyone.
    // data.append('photo', {
    //   uri: PicturePath,
    //   type: 'image/jpeg', // or photo.type
    //   name: 'testPhotoName'
    // });
    //
    // ImgToBase64.getBase64String(PicturePath)
    //   .then(base64String => {
    //     console.log(base64String);
    //     fetch('http://10.105.73.133:8000/api', {body: base64String}).then(res => {
    //       console.log(res)
    //     });
    //   });

  }

  render() {//special function is calle when router wants to know what to render

    return (
      <View style={styles.container}>
        <RNCamera
            ref={ref => {
              this.camera = ref;
            }}
            style = {styles.preview}
            type={RNCamera.Constants.Type.back}
            flashMode={RNCamera.Constants.FlashMode.off}
            permissionDialogTitle={'Permission to use camera'}
            permissionDialogMessage={'We need your permission to use your camera phone'}
        />
        <TouchableOpacity
            onPress={this.takePicture.bind(this)}
            style = {styles.capture}
        />
      </View>
    );
  }

  takePicture = async function() {
    if (this.camera) {
      const options = { quality: 0.5, base64: true };
      const data = await this.camera.takePictureAsync(options)
      console.log(data.uri);
      CameraRoll.saveToCameraRoll(data.uri);
      //send whole image to sever.
      // this.uploadPhoto(data.uri);
      this.props.navigation.navigate('People');//props and static
        }
  };
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
    backgroundColor: 'black',
    justifyContent: 'flex-end',
    alignItems: 'center'
  },
  preview: {
    position: 'absolute',
    height: Dimensions.get('window').height,
    width: Dimensions.get('window').width,
    justifyContent: 'flex-end',
    alignItems: 'center'
  },
  capture: {
    backgroundColor: 'transparent',
    width: 80,
    height: 80,
    borderRadius: 40,
    borderColor: '#A8A8A8',
    borderWidth: 7,
    margin: 40
  }
});
