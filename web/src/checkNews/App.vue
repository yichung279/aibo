<template lang='pug'>
#app.flex-container.content-center
  .flex-item.flex-container.flex-vertical.margin
    table.ui.celled.table
      thead
        tr
          th URL
          th Collected time
          th Checked time
          th Published time
          th Poster
      tbody
        tr(v-for="value in news", :class="{ checked: value.checked }")
          td
            .ui.checkbox
              input(type='checkbox', :disabled='value.checked', :value='value.url', v-model='checkedNews')
              label
                a(:href='value.url') {{ value.url }}
          td {{ value.collect_time }}
          td {{ value.checked_time }}
          td {{ value.published_time }}
          td
            .ui.label {{ value.poster }}
    .ui.button(@click='publish()') Save
</template>

<script>
import axios from 'axios'
import Swal from 'sweetalert2'

export default {
  async mounted() {
    let resopnse = await axios.get('/news/30')
    const news = resopnse.data
    // mock
    // const news = [{published_time:null,checked: true, checked_time: "2020-07-17T15:45:25.240321",collect_time:"2020-07-17T15:45:25.240321",poster:"yiz",published:null,url:"https://facebook.com",_id:1},{published_time:null,collect_time:"2020-07-17T15:45:26.675134",poster:"yiz",published:null,url:"https://amazon.com",_id:2},{published_time:null,collect_time:"2020-07-17T15:45:29.723983",poster:"yiz",published:null,url:"https://netflix.com",_id:3}]
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
	  Swal.fire({
		title: 'News\' have been saved',
		icon: 'success',
        onAfterClose: function(){
          location.reload()
        }
	  })
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

tr.checked
  background: #f0ffcc!important

</style>
