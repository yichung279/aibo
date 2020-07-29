import Vue from 'vue'
import App from './App.vue'
import 'semantic-ui-offline/semantic.min.css'
import Vlf from 'vlf'
import localforage from 'localforage'

Vue.use(Vlf, localforage)

new Vue({
  el: '#app',
  render: h => h(App),
})
