<template lang='html'>
<div id="main-wrapper">
  <router-view></router-view>
</div>
</template>
<script>
export default {

}
</script>
<style >
div#main-wrapper{
  width: 800px;
  margin: auto;
  font-size: 20px;
}

div#main-wrapper .title{
  text-align: center;    
  font-size: 20px;
}

div#main-wrapper p.content {
    margin-left: 25px;
    margin-right: 20px;
    margin-bottom: 20px;
    font-size: 15px
}
</style>
