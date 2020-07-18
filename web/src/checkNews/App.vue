<template lang='pug'>
#app.flex-container.content-center
  .flex-item.flex-container.flex-vertical.margin
    .ui.vertical.menu.fluid
      .item(v-for="value in news")
        .ui.checkbox
          input(type='checkbox', :value='value.url', v-model='checkedNews')
          label
            a(:href='value.url')  {{ value.url }}
        .ui.label {{ value.poster }}
    .ui.button(@click='publish()') Publish
</template>

<script>
import axios from 'axios'

export default {
  async mounted() {
    let resopnse = await axios.get('/news/5')
    const news=resopnse.data
    // mock
    // const news = [{published_time:null,collect_time:"2020-07-17T15:45:25.240321",poster:"yiz",published:null,url:"https://facebook.com",_id:1},{published_time:null,collect_time:"2020-07-17T15:45:26.675134",poster:"yiz",published:null,url:"https://amazon.com",_id:2},{published_time:null,collect_time:"2020-07-17T15:45:29.723983",poster:"yiz",published:null,url:"https://netflix.com",_id:3}]
    news.forEach((value, i) => {
      this.$set(this.news, i, value)
    })
  },

  data(){return{
    news: [],
    checkedNews: []
  }},

  methods:{
    publish(){
      axios.post('/checkedNews/', this.checkedNews)
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
.margin
  margin: 2rem

</style>
