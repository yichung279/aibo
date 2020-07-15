<template lang='pug'>
#app.flex-container.content-center
  .flex-item.flex-container.flex-vertical.padding
    .ui.vertical.menu
      .item(v-for="url in urls")
        .ui.checkbox
          input(type='checkbox', :value='url', v-model='checkedUrls')
          label
            a(:href='url')  {{ url }}
    .ui.button(@click='publish()') Publish
</template>

<script>
import axios from 'axios'

export default {
  async mounted() {
    // let resopnse = await axios.get('/urls/')
    // console.log(resopnse.data)
    // this.urls=resopnse.data
    this.urls=['facebook.com', 'amazon.com', 'netflix.com', 'google.com']
  },

  data(){return{
    urls: [],
    checkedUrls: []
  }},

  methods:{
    async publish(){
      await axios.post('/messages/', this.checkedUrls)
    }
  }
}
</script>

<style lang="sass">
.flex-container
  display: flex
.content-center
  justify-content: center
.flex-vertical
  flex-direction: column
.padding
  padding: 3rem

</style>
