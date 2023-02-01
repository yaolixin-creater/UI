<template>
  <div>
    <head-top></head-top>
    <img class="images" src="../assets/img/my_wx.png" />
  </div>
</template>
<script>
import headTop from '@/components/headTop'
export default {
  data () {
    return {
      src: ''
    }
  },
  components: {
    headTop
  }
}
</script>
<style lang="less" scoped>
@import "../style/mixin";
.images {
  width: 100%;
  /*height: 40%;*/
  margin: 0% 0% 0% 0%;
}
</style>
