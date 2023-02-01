<template>
  <div class="menu_page fillcontain">
    <el-row style="height: 100%;">
      <el-col :span="4" class="col-menu">
        <el-menu
          :default-active="defaultActive"
          router
          :unique-opened="true"
          background-color="#006699"
          text-color="#FFFFFF"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="home">
            <i class="el-icon-menu"></i>首页
          </el-menu-item>
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-s-grid"></i>UI自动化
            </template>
            <el-menu-item class="el-icon-s-marketing" index="backCaseList">&ensp;UI用例列表</el-menu-item>
            <el-menu-item class="el-icon-s-data" index="backReport">&ensp;UI测试报告</el-menu-item>
            <el-menu-item class="el-icon-edit" index="backParamAdd">&ensp;UI用例新增</el-menu-item>
            <el-menu-item class="el-icon-edit-outline" index="backParamList">&ensp;UI参数配置</el-menu-item>
            <el-menu-item class="el-icon-document-copy" index="backstepmod">&ensp;UI复用步骤修改</el-menu-item>
            <el-menu-item class="el-icon-menu" index="groupManagement">&ensp;UI分组管理</el-menu-item>
            <el-menu-item class="el-icon-setting" index="envManagement">&ensp;UI环境管理</el-menu-item>
            <el-menu-item class="el-icon-document" index="help">&ensp;UI帮助文档</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-col>
      <el-col :span="20" style="height: 100%; overflow: auto;">
        <router-view></router-view>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  data () {
    return {}
  },
  methods: {},
  computed: {
    defaultActive: function () {
      return this.$route.path.replace('/', '')
    }
  }
}
</script>

<style lang="less" scoped>
@import "../style/mixin";
.col-menu {
  background-color: #006699;
  min-height: 100%;
}
</style>
